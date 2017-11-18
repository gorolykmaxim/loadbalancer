import aiohttp


class ProxyError(Exception):

    def __init__(self, node_group, reason):
        message = "Failed to submit node group '{}' to the proxy: {}".format(node_group, reason)
        super(ProxyError, self).__init__(message)


class ProxyErrorResponse(Exception):

    def __init__(self, error):
        message = "Proxy responded with an error: '{}'".format(error)
        super(ProxyErrorResponse, self).__init__(message)


class Proxy(object):

    def __init__(self, url):
        self.__url = url or 'http://localhost:5001/node_group/{}'

    async def submit_node_group(self, name, node_list):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.__url.format(name), json={'nodes': node_list}) as response:
                    if 399 < response.status or response.status < 200:
                        raise ProxyErrorResponse(response.text)
        except Exception as e:
            raise ProxyError(name, str(e))


class IntegrationLayer(object):

    def __init__(self, proxy_url):
        self.__proxy = Proxy(proxy_url)

    async def submit_node_group_to_proxy(self, name, node_list):
        await self.__proxy.submit_node_group(name, node_list)