from aiohttp import ClientSession


class APIError(Exception):
    pass


class Resource(object):

    async def get(self, url):
        async with ClientSession() as session:
            async with session.get(url=url) as response:
                if response.status < 200 or response.status > 399:
                    raise APIError(response.text)
                return await response.json()

    async def post(self, url, body):
        async with ClientSession() as session:
            async with session.post(url=url, json=body) as response:
                if response.status < 200 or response.status > 399:
                    raise APIError(response.text)

    async def put(self, url, body):
        async with ClientSession() as session:
            async with session.put(url=url, json=body) as response:
                if response.status < 200 or response.status > 399:
                    raise APIError(response.text)

    async def delete(self, url):
        async with ClientSession() as session:
            async with session.delete(url=url) as response:
                if response.status < 200 or response.status > 399:
                    raise APIError(response.text)


class AdvancedLoadbalancerAPI(object):

    def __init__(self, url=None):
        self.__url = url + '{}' if url is not None else 'http://localhost:5000{}'
        self.__node_groups = self.__url.format('/node_group')
        self.__node_group = self.__url.format('/node_group/{group_name}')
        self.__nodes = self.__url.format('/node_group/{group_name}/node')
        self.__node = self.__url.format('/node_group/{group_name}/node/{node_name}')
        self.__attributes = self.__url.format('/node_group/{group_name}/node/{node_name}/attribute')
        self.__attribute = self.__url.format('/node_group/{group_name}/node/{node_name}/attribute/{attribute_name}')
        self.__resource = Resource()

    async def get_node_groups(self):
        return await self.__resource.get(url=self.__node_groups)

    async def get_node_group(self, group_name):
        return await self.__resource.get(url=self.__node_group.format(group_name=group_name))

    async def create_node_group(self, group_name):
        await self.__resource.post(url=self.__node_group.format(group_name=group_name), body={})

    async def remove_node_group(self, group_name):
        await self.__resource.delete(url=self.__node_group.format(group_name=group_name))

    async def get_nodes(self, group_name):
        return await self.__resource.get(url=self.__nodes.format(group_name=group_name))

    async def get_node(self, group_name, node_name):
        return await self.__resource.get(url=self.__node.format(group_name=group_name, node_name=node_name))

    async def create_node(self, group_name, node_name, host, port):
        node = {'host': host, 'port': port}
        await self.__resource.post(self.__node.format(group_name=group_name, node_name=node_name), body=node)

    async def update_node(self, group_name, node_name, host=None, port=None):
        node = {}
        if host is not None:
            node['host'] = host
        if port is not None:
            node['port'] = port
        await self.__resource.put(self.__node.format(group_name=group_name, node_name=node_name), body=node)

    async def remove_node(self, group_name, node_name):
        await self.__resource.delete(self.__node.format(group_name=group_name, node_name=node_name))

    async def get_attributes(self, group_name, node_name):
        return await self.__resource.get(self.__attributes.format(group_name=group_name, node_name=node_name))

    async def get_attribute(self, group_name, node_name, attribute_name):
        return await self.__resource.get(self.__attribute.format(group_name=group_name, node_name=node_name,
                                                                 attribute_name=attribute_name))

    async def create_attribute(self, group_name, node_name, attribute_name, value, weight):
        attribute = {'value': value, 'weight': weight}
        await self.__resource.post(self.__attribute.format(group_name=group_name, node_name=node_name,
                                                           attribute_name=attribute_name), body=attribute)

    async def update_attribute(self, group_name, node_name, attribute_name, value=None, weight=None):
        attribute = {}
        if value is not None:
            attribute['value'] = value
        if weight is not None:
            attribute['weight'] = weight
        await self.__resource.put(self.__attribute.format(group_name=group_name, node_name=node_name,
                                                          attribute_name=attribute_name), body=attribute)

    async def remove_attribute(self, group_name, node_name, attribute_name):
        await self.__resource.delete(self.__attribute.format(group_name=group_name, node_name=node_name,
                                                             attribute_name=attribute_name))
