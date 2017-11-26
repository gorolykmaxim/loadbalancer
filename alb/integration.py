import aiohttp


class ProxyError(Exception):
    """Error in the attempt to submit a node group to the proxy."""
    def __init__(self, node_group, reason):
        """Constructor of the ProxyError.

        Args:
            node_group (str): Name of the group.
            reason (str): Reason of the error.

        """
        message = "Failed to submit node group '{}' to the proxy: {}".format(node_group, reason)
        super(ProxyError, self).__init__(message)


class ProxyErrorResponse(Exception):
    """Proxy responded with an error code."""
    def __init__(self, error):
        """Constructor of the ProxyErrorResponse.

        Args:
            error (Exception): The original exception.

        """
        message = "Proxy responded with an error: '{}'".format(error)
        super(ProxyErrorResponse, self).__init__(message)


class Proxy(object):
    """A proxy server interface.
    
    Notifies remote proxy about changes in the cluster configuration.
    
    Attributes:
        __url (str): URL of the proxy API.
    
    """
    def __init__(self, url):
        """Constructor of the Proxy.
        
        Args:
            url (str): URL of the proxy API.
        
        """
        self.__url = url or 'http://localhost:5001/node_group/{}'

    async def submit_node_group(self, name, node_list):
        """Submit a node group to the remote proxy.
        
        Note: awaitable method.
        
        Args:
            name (str): Name of the node group.
            node_list (list): List of nodes of the group.
            
        Raises:
            ProxyError: If an error occurred while trying to submit the group
        
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.__url.format(name), json={'nodes': node_list}) as response:
                    if 399 < response.status or response.status < 200:
                        raise ProxyErrorResponse(await response.text())
        except Exception as e:
            raise ProxyError(name, str(e))


class IntegrationLayer(object):
    """A facade of an integration layer.
    
    Attributes:
        __proxy (Proxy): A remote proxy server.
    
    """
    def __init__(self, proxy_url):
        """Constructor of the IntegrationLayer.
        
        Args:
            proxy_url (str): URL of the proxy API.
        
        """
        self.__proxy = Proxy(proxy_url)

    async def submit_node_group_to_proxy(self, name, node_list):
        """Submit a node group to the remote proxy.

        Note: awaitable method.

        Args:
            name (str): Name of the node group.
            node_list (list): List of nodes of the group.

        Raises:
            ProxyError: If an error occurred while trying to submit the group

        """
        await self.__proxy.submit_node_group(name, node_list)
