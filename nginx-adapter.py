import subprocess

from japronto import Application
from nginx import dumpf, Upstream, Key, loadf

from core.config import Config


class NginxAdapter(object):

    def __init__(self):
        self.__config = Config()
        self.__upstream_path = self.__config.get_attribute('upstream_path') or '/etc/nginx/upstream.conf'
        self.__notify_nginx_command = self.__config.get_attribute('notify_nginx_command') or 'service nginx reload'
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
        self.__update_upstream(name, servers)
        self.__notify_nginx()

    def __adapt_nodes_list(self, nodes):
        size = len(nodes)
        nodes = sorted(nodes, key=lambda k: k['weight'])
        return [self.__adapt_node(node, i, size) for i, node in enumerate(nodes)]

    def __adapt_node(self, node, position, list_size):
        return {
            'url': '{host}:{port}'.format(host=node['host'], port=node['port']),
            'weight': int(position / list_size * 100) + 1
        }

    def __update_upstream(self, name, servers):
        conf = loadf(self.__upstream_path)
        try:
            conf.remove(*conf.filter('Upstream', name))
        except ValueError:
            pass
        upstream = Upstream(name, *[Key('server', '{url} weight={weight}'.format(**server)) for server in servers])
        conf.add(upstream)
        dumpf(conf, self.__upstream_path)

    def __notify_nginx(self):
        subprocess.call(self.__notify_nginx_command.split(' '))

    def main(self):
        self.__application.add_error_handler(Exception, self.__handle_error)
        self.__application.router.add_route(pattern='/node_group/{group_name}',
                                            handler=self.__handle_request, method='POST')
        host = self.__config.get_attribute('host') or '0.0.0.0'
        port = self.__config.get_attribute('port') or 5001
        self.__application.run(host=host, port=port)


if __name__ == '__main__':
    NginxAdapter().main()
