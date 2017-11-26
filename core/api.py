from aiohttp import ClientSession


class APIError(Exception):
    """Error, that occurs during communication with REST API."""
    pass


class Resource(object):
    """An interface to the REST API."""
    async def get(self, url):
        """Execute a GET request on the specified url.

        Note: awaitable method.

        Args:
            url (str): URL of the request.

        Returns:
            dict: Body of the response.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        async with ClientSession() as session:
            async with session.get(url=url) as response:
                if response.status < 200 or response.status > 399:
                    raise APIError(await response.text())
                return await response.json()

    async def post(self, url, body):
        """Execute a POST request on the specified url with a specified body.

        Note: awaitable method.

        Args:
            url (str): URL of the request.
            body (dict): Body of the request.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        async with ClientSession() as session:
            async with session.post(url=url, json=body) as response:
                if response.status < 200 or response.status > 399:
                    raise APIError(await response.text())

    async def put(self, url, body):
        """Execute a PUT request on the specified url with a specified body.

        Note: awaitable method.

        Args:
            url (str): URL of the request.
            body (dict): Body of the request.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        async with ClientSession() as session:
            async with session.put(url=url, json=body) as response:
                if response.status < 200 or response.status > 399:
                    raise APIError(await response.text())

    async def delete(self, url):
        """Execute a DELETE request on the specified url.

        Note: awaitable method.

        Args:
            url (str): URL of the request.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        async with ClientSession() as session:
            async with session.delete(url=url) as response:
                if response.status < 200 or response.status > 399:
                    raise APIError(await response.text())


class AdvancedLoadbalancerAPI(object):
    """An interface to the API of the ALB service.

    Attributes:
        __url (str): A base URL to the remote API.
        __node_group (str): URL to access all node groups.
        __node_groups (str): URL to access a specific node group.
        __nodes (str): URL to access all nodes of the specific group.
        __node (str): URL to access specific node of the specific group.
        __attributes (str): URL to access all attributes of the specific node.
        __attribute (str): URL to access specific attribute of the specific node.
        __resource (Resource): REST communication channel.

    """
    def __init__(self, url=None):
        """Constructor of the AdvancedLoadbalancerAPI.

        Args:
            url (str): Base URL of the remote API.

        """
        self.__url = url + '{}' if url is not None else 'http://localhost:5000{}'
        self.__node_groups = self.__url.format('/node_group')
        self.__node_group = self.__url.format('/node_group/{group_name}')
        self.__nodes = self.__url.format('/node_group/{group_name}/node')
        self.__node = self.__url.format('/node_group/{group_name}/node/{node_name}')
        self.__attributes = self.__url.format('/node_group/{group_name}/node/{node_name}/attribute')
        self.__attribute = self.__url.format('/node_group/{group_name}/node/{node_name}/attribute/{attribute_name}')
        self.__resource = Resource()

    async def get_node_groups(self):
        """Return all node groups.

        Note: awaitable method.

        Returns:
            dict: Named list of all node groups.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        return await self.__resource.get(url=self.__node_groups)

    async def get_node_group(self, group_name):
        """Return a node group with the specified name.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.

        Returns:
            dict: Information about a node group.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        return await self.__resource.get(url=self.__node_group.format(group_name=group_name))

    async def create_node_group(self, group_name):
        """Create a node group with the specified name.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        await self.__resource.post(url=self.__node_group.format(group_name=group_name), body={})

    async def remove_node_group(self, group_name):
        """Remove a node group with the specified name.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        await self.__resource.delete(url=self.__node_group.format(group_name=group_name))

    async def get_nodes(self, group_name):
        """Return all nodes of the specified group.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.

        Returns:
            dict: Named list of nodes.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        return await self.__resource.get(url=self.__nodes.format(group_name=group_name))

    async def get_node(self, group_name, node_name):
        """Return specific node of the specified group.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.

        Returns:
            dict: Information about the node.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        return await self.__resource.get(url=self.__node.format(group_name=group_name, node_name=node_name))

    async def create_node(self, group_name, node_name, host, port):
        """Create a node in the specified group.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            host (str): Host of the node.
            port (int): Port of the node.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        node = {'host': host, 'port': port}
        await self.__resource.post(self.__node.format(group_name=group_name, node_name=node_name), body=node)

    async def update_node(self, group_name, node_name, host=None, port=None):
        """Update an information about the node in the specified group.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            host (str): Host of the node.
            port (int): Port of the node.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        node = {}
        if host is not None:
            node['host'] = host
        if port is not None:
            node['port'] = port
        await self.__resource.put(self.__node.format(group_name=group_name, node_name=node_name), body=node)

    async def remove_node(self, group_name, node_name):
        """Remove the node in the specified group.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        await self.__resource.delete(self.__node.format(group_name=group_name, node_name=node_name))

    async def get_attributes(self, group_name, node_name):
        """Return all attributes of the specified node.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.

        Returns:
            dict: Named list of attributes.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        return await self.__resource.get(self.__attributes.format(group_name=group_name, node_name=node_name))

    async def get_attribute(self, group_name, node_name, attribute_name):
        """Return a specific attribute of the specified node.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        Returns:
            dict: Information about the attribute.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        return await self.__resource.get(self.__attribute.format(group_name=group_name, node_name=node_name,
                                                                 attribute_name=attribute_name))

    async def create_attribute(self, group_name, node_name, attribute_name, value, weight):
        """Add an attribute to the specified node.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.
            value (float): Current value of the attribute.
            weight (float): Static weight of the attribute.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        attribute = {'value': value, 'weight': weight}
        await self.__resource.post(self.__attribute.format(group_name=group_name, node_name=node_name,
                                                           attribute_name=attribute_name), body=attribute)

    async def update_attribute(self, group_name, node_name, attribute_name, value=None, weight=None):
        """Update an information about the attribute of the specified node.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.
            value (float): Current value of the attribute.
            weight (float): Static weight of the attribute.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        attribute = {}
        if value is not None:
            attribute['value'] = value
        if weight is not None:
            attribute['weight'] = weight
        await self.__resource.put(self.__attribute.format(group_name=group_name, node_name=node_name,
                                                          attribute_name=attribute_name), body=attribute)

    async def remove_attribute(self, group_name, node_name, attribute_name):
        """Remove an attribute of the node.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        Raises:
            APIError: If remote server responds with a non-200 OK code.

        """
        await self.__resource.delete(self.__attribute.format(group_name=group_name, node_name=node_name,
                                                             attribute_name=attribute_name))
