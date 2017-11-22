import asyncio
import subprocess

import aiofiles
from japronto import Application
from nginx import dump, Upstream, Key, load

from core.config import Config


class Nginx(object):

    def __init__(self, reload_command, upstream_path):
        self.__reload_command = reload_command
        self.__upstream_path = upstream_path

    async def update_upstream(self, name, servers):
        await self.__update_upstream(name, servers)
        self.__reload()

    async def __update_upstream(self, name, servers):
        async with aiofiles.open(self.__upstream_path, mode='rw') as f:
            conf = load(f)
            try:
                conf.remove(*conf.filter('Upstream', name))
            except ValueError:
                pass
            upstream = Upstream(name, *[Key('server', '{url} weight={weight}'.format(**server)) for server in servers])
            conf.add(upstream)
            dump(conf, f)

    def __reload(self):
        subprocess.Popen(self.__reload_command.split(' '))


class NginxAdapter(object):

    def __init__(self):
        self.__config = Config()
        upstream_path = self.__config.get_attribute('upstream_path') or '/etc/nginx/upstream.conf'
        notify_nginx_command = self.__config.get_attribute('notify_nginx_command') or 'service nginx reload'
        self.__nginx = Nginx(reload_command=notify_nginx_command, upstream_path=upstream_path)
        self.__application = Application()

    def __handle_error(self, request, exception):
        return request.Response(code=500, text=str(exception))

    def __handle_request(self, request):
        group_name = request.match_dict['group_name']
        nodes = request.json['nodes']
        self.__handle_update(group_name, nodes)
        return request.Response()

    def __handle_update(self, name, nodes):
        servers = self.__adapt_nodes_list(nodes)
        asyncio.ensure_future(self.__nginx.update_upstream(name, servers))

    def __adapt_nodes_list(self, nodes):
        size = len(nodes)
        nodes = sorted(nodes, key=lambda k: k['weight'])
        return [self.__adapt_node(node, i, size) for i, node in enumerate(nodes)]

    def __adapt_node(self, node, position, list_size):
        return {
            'url': '{host}:{port}'.format(host=node['host'], port=node['port']),
            'weight': int(position / list_size * 100) + 1
        }

    def main(self):
        self.__application.add_error_handler(Exception, self.__handle_error)
        self.__application.router.add_route(pattern='/node_group/{group_name}',
                                            handler=self.__handle_request, method='POST')
        host = self.__config.get_attribute('host') or '0.0.0.0'
        port = self.__config.get_attribute('port') or 5001
        self.__application.run(host=host, port=port)


if __name__ == '__main__':
    NginxAdapter().main()
