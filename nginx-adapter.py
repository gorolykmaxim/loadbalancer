import asyncio
import subprocess

import aiofiles
from japronto import Application
from nginx import dumps, Upstream, Key, loads

from core.config import Config


class Nginx(object):
    """An interface to the nginx server.

    Attributes:
        __reload_command (str): Command, that reloads nginx server.
        __upstream_path (str): Path to the nginx configuration file, that contains upstreams.

    """
    def __init__(self, reload_command, upstream_path):
        """Constructor of the Nginx.

        Args:
            reload_command (str): Command, that reloads nginx server.
            upstream_path (str): Path to the nginx configuration file, that contains upstreams.

        """
        self.__reload_command = reload_command
        self.__upstream_path = upstream_path

    async def update_upstream(self, name, servers):
        """Update specified upstream in the configuration file and reload nginx server.

        Note: awaitable method.

        Args:
            name (str): Name of the upstream.
            servers (list): List of servers and their weights, that belong to the upstream.

        """
        await self.__update_upstream(name, servers)
        self.__reload()

    async def __update_upstream(self, name, servers):
        """Update specified upstream in the configuration file.

        Note: awaitable method.

        Args:
            name (str): Name of the upstream.
            servers (list): List of servers and their weights, that belong to the upstream.

        """
        async with aiofiles.open(self.__upstream_path, mode='r+') as f:
            conf = loads(await f.read())
            try:
                conf.remove(*conf.filter('Upstream', name))
            except ValueError:
                pass
            upstream = Upstream(name, *[Key('server', '{url} weight={weight}'.format(**server)) for server in servers])
            conf.add(upstream)
            await f.seek(0)
            await f.truncate()
            await f.write(dumps(conf))

    def __reload(self):
        """Reload nginx server."""
        subprocess.Popen(self.__reload_command.split(' '))


class NginxAdapter(object):
    """nginx-adapter service root class.

    Listens to incoming HTTP requests, transforms received node groups into upstreams and passes them to Nginx.

    Attributes:
        __config (Config): Configuration of the application.
        __nginx (Nginx): Interface of the Nginx server.
        __application (Application): HTTP server.

    """
    def __init__(self):
        """Constructor of the NginxAdapter."""
        self.__config = Config()
        upstream_path = self.__config.get_attribute('upstream_path') or '/etc/nginx/upstream.conf'
        notify_nginx_command = self.__config.get_attribute('notify_nginx_command') or 'service nginx reload'
        self.__nginx = Nginx(reload_command=notify_nginx_command, upstream_path=upstream_path)
        self.__application = Application()

    def __handle_error(self, request, exception):
        """Respond to the request with a 500 Internal server error and a reason, taken from the specified exception
        message.

        Args:
            request (Request): Instance of the HTTP request.
            exception (Exception): The original error.

        Returns:
            Response: HTTP response to the specified request.

        """
        return request.Response(code=500, text=str(exception))

    async def __handle_request(self, request):
        """Process incoming HTTP request and return a response to it.

        Args:
            request (Request): Instance of the HTTP request.

        Returns:
            Response: HTTP response to the specified request.

        """
        group_name = request.match_dict['group_name']
        nodes = request.json['nodes']
        await self.__handle_update(group_name, nodes)
        return request.Response()

    async def __handle_update(self, name, nodes):
        """Transform specified node group into the upstream and pass it to the Nginx.

        Args:
            name (str): Name of the node group.
            nodes (list): List of the nodes and their weights.

        """
        servers = self.__adapt_nodes_list(nodes)
        await self.__nginx.update_upstream(name, servers)

    def __adapt_nodes_list(self, nodes):
        """Return an upstream representation of the specified list of nodes.

        Args:
            nodes (list): List of nodes to transform.

        Returns:
            list: List of upstream nodes.

        """
        size = len(nodes)
        nodes = sorted(nodes, key=lambda k: k['weight'])
        return [self.__adapt_node(node, i, size) for i, node in enumerate(nodes)]

    def __adapt_node(self, node, position, list_size):
        """Return an upstream representation of the specified node.

        Args:
            node (dict): Node information.
            position (int): Position of the node in the ordered list.
            list_size (int): Size of the entire list of nodes.

        Returns:
            dict: Upstream representation of the node.

        """
        return {
            'url': '{host}:{port}'.format(host=node['host'], port=node['port']),
            'weight': int(position / list_size * 100) + 1
        }

    def main(self):
        """Entry-point of the NginxAdapter. Setup and run the HTTP server."""
        self.__application.add_error_handler(Exception, self.__handle_error)

        async def handler(request):
            return await self.__handle_request(request)

        self.__application.router.add_route(pattern='/node_group/{group_name}',
                                            handler=handler, method='POST')
        host = self.__config.get_attribute('host') or '0.0.0.0'
        port = self.__config.get_attribute('port') or 5001
        self.__application.run(host=host, port=port)


if __name__ == '__main__':
    NginxAdapter().main()
