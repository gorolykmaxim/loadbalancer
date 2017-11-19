class BusinessProcessError(Exception):
    pass


class UnknownAttributeError(BusinessProcessError):

    def __init__(self, attribute_name):
        message = "Unknown attribute: '{}'".format(attribute_name)
        super(UnknownAttributeError, self).__init__(message)


class UnknownNodeAttributeError(BusinessProcessError):

    def __init__(self, node_name, attribute_name):
        message = "Node with name '{}' has no attribute '{}'".format(node_name, attribute_name)
        super(UnknownNodeAttributeError, self).__init__(message)


class UnknownNodeFromGroupAttributeError(BusinessProcessError):

    def __init__(self, group_name, node_name, attribute_name):
        message = "Node from group '{}' with name '{}' has no attribute '{}'".format(group_name, node_name,
                                                                                     attribute_name)
        super(UnknownNodeFromGroupAttributeError, self).__init__(message)


class UnknownNodeError(BusinessProcessError):

    def __init__(self, node_name):
        super(UnknownNodeError, self).__init__("Unknown node: '{}'".format(node_name))


class UnknownNodeFromGroupError(BusinessProcessError):

    def __init__(self, group_name, node_name):
        message = "There is no node with the name '{}' in the group '{}'".format(node_name, group_name)
        super(UnknownNodeFromGroupError, self).__init__(message)


class UnknownNodeGroupError(BusinessProcessError):

    def __init__(self, group_name):
        message = "Node group with the name '{}' does not exist".format(group_name)
        super(UnknownNodeGroupError, self).__init__(message)


class AttributeAlreadyExistsError(BusinessProcessError):

    def __init__(self, attribute_name):
        message = "Attribute with the name '{}' already exists".format(attribute_name)
        super(AttributeAlreadyExistsError, self).__init__(message)


class NodeAttributeAlreadyExistsError(BusinessProcessError):

    def __init__(self, node_name, attribute_name):
        message = "Node '{}' already has an attribute, called '{}'".format(node_name, attribute_name)
        super(NodeAttributeAlreadyExistsError, self).__init__(message)


class NodeFromGroupAttributeAlreadyExistsError(BusinessProcessError):

    def __init__(self, group_name, node_name, attribute_name):
        message = "Node '{}' from the group '{}' already has an attribute, called '{}'".format(node_name, group_name,
                                                                                               attribute_name)
        super(NodeFromGroupAttributeAlreadyExistsError, self).__init__(message)


class NodeAlreadyExistsError(BusinessProcessError):

    def __init__(self, node_name):
        super(NodeAlreadyExistsError, self).__init__("Node '{}' already exists".format(node_name))


class NodeFromGroupAlreadyExists(BusinessProcessError):

    def __init__(self, group_name, node_name):
        message = "Group '{}' already has a node, called '{}'".format(group_name, node_name)
        super(NodeFromGroupAlreadyExists, self).__init__(message)


class Attribute(object):

    def __init__(self, value, weight):
        self.__value = float(value)
        self.__weight = float(weight)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = float(value)

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = float(value)

    @property
    def current_weight(self):
        return self.__value * self.__weight


class Node(object):

    def __init__(self, host, port):
        self.host = host
        self.__port = int(port)
        self.__attributes = {}

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = int(value)

    def get_attributes(self):
        attributes = {}
        for name, attribute in self.__attributes.items():
            attributes[name] = {
                'value': attribute.value,
                'weight': attribute.weight
            }
        return attributes

    def get_attribute(self, name):
        try:
            attribute = self.__attributes[name]
            return {
                'value': attribute.value,
                'weight': attribute.weight
            }
        except KeyError:
            raise UnknownAttributeError(name)

    def add_attribute(self, name, value, weight):
        if name in self.__attributes:
            raise AttributeAlreadyExistsError(name)
        self.__attributes[name] = Attribute(value, weight)

    def update_attribute(self, name, value=None, weight=None):
        try:
            attribute = self.__attributes[name]
            attribute.value = value or attribute.value
            attribute.weight = weight or attribute.weight
        except KeyError:
            raise UnknownAttributeError(name)

    def remove_attribute(self, name):
        try:
            self.__attributes.pop(name)
        except KeyError:
            raise UnknownAttributeError(name)

    @property
    def weight(self):
        return sum([attribute.current_weight for attribute in self.__attributes.values()])


class NodeGroup(object):

    def __init__(self):
        self.__nodes = {}

    def get_nodes_list(self):
        nodes = []
        for node in self.__nodes.values():
            node_info = {
                'host': node.host,
                'port': node.port,
                'weight': node.weight
            }
            nodes.append(node_info)
        return nodes

    def get_nodes(self):
        nodes = {}
        for name, node in self.__nodes.items():
            nodes[name] = {
                'host': node.host,
                'port': node.port,
                'weight': node.weight,
                'attributes': node.get_attributes()
            }
        return nodes

    def get_node(self, name):
        try:
            node = self.__nodes[name]
            return {
                'host': node.host,
                'port': node.port,
                'weight': node.weight,
                'attributes': node.get_attributes()
            }
        except KeyError:
            raise UnknownNodeError(name)

    def add_node(self, name, host, port):
        if name in self.__nodes:
            raise NodeAlreadyExistsError(name)
        self.__nodes[name] = Node(host, port)

    def update_node(self, name, host=None, port=None):
        try:
            node = self.__nodes[name]
            node.host = host or node.host
            node.port = port or node.port
        except KeyError:
            raise UnknownNodeError(name)

    def remove_node(self, name):
        try:
            self.__nodes.pop(name)
        except KeyError:
            raise UnknownNodeError(name)

    def get_node_attributes(self, node_name):
        try:
            return self.__nodes[node_name].get_attributes()
        except KeyError:
            raise UnknownNodeError(node_name)

    def get_node_attribute(self, node_name, attribute_name):
        try:
            node = self.__nodes[node_name]
            return node.get_attribute(attribute_name)
        except KeyError:
            raise UnknownNodeError(node_name)
        except UnknownAttributeError:
            raise UnknownNodeAttributeError(node_name, attribute_name)

    def add_node_attribute(self, node_name, attribute_name, value, weight):
        try:
            node = self.__nodes[node_name]
            node.add_attribute(attribute_name, value, weight)
        except KeyError:
            raise UnknownNodeError(node_name)
        except AttributeAlreadyExistsError:
            raise NodeAttributeAlreadyExistsError(node_name, attribute_name)

    def update_node_attribute(self, node_name, attribute_name, value=None, weight=None):
        try:
            node = self.__nodes[node_name]
            node.update_attribute(attribute_name, value, weight)
        except KeyError:
            raise UnknownNodeError(node_name)
        except UnknownAttributeError:
            raise UnknownNodeAttributeError(node_name, attribute_name)

    def remove_node_attribute(self, node_name, attribute_name):
        try:
            node = self.__nodes[node_name]
            node.remove_attribute(attribute_name)
        except KeyError:
            raise UnknownNodeError(node_name)
        except UnknownAttributeError:
            raise UnknownNodeAttributeError(node_name, attribute_name)


class NodeGroupRepository(object):

    def __init__(self):
        self.__node_groups = {}

    def get_node_group(self, name):
        try:
            return self.__node_groups[name]
        except KeyError:
            raise UnknownNodeGroupError(name)

    def get_node_groups(self):
        return self.__node_groups

    def save(self, name, node_group):
        self.__node_groups[name] = node_group

    def remove(self, name):
        try:
            self.__node_groups.pop(name)
        except KeyError:
            raise UnknownNodeGroupError(name)


class BusinessLayerFacade(object):

    def __init__(self, integration_layer):
        self.__integration_layer = integration_layer
        self.__node_group_repository = NodeGroupRepository()

    async def get_node_groups(self):
        node_groups = self.__node_group_repository.get_node_groups()
        groups = {}
        for name, node_group in node_groups.items():
            groups[name] = {'nodes': node_group.get_nodes()}
        return groups

    async def get_node_group(self, group_name):
        node_group = self.__node_group_repository.get_node_group(group_name)
        return {'nodes': node_group.get_nodes()}

    async def create_node_group(self, group_name):
        node_group = NodeGroup()
        self.__node_group_repository.save(group_name, node_group)

    async def remove_node_group(self, group_name):
        self.__node_group_repository.remove(group_name)
        await self.__integration_layer.submit_node_group_to_proxy(group_name, [])

    async def get_nodes(self, group_name):
        node_group = self.__node_group_repository.get_node_group(group_name)
        return node_group.get_nodes()

    async def get_node(self, group_name, node_name):
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            return node_group.get_node(node_name)
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)

    async def create_node(self, group_name, node_name, host, port):
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.add_node(node_name, host, port)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except NodeAlreadyExistsError:
            raise NodeFromGroupAlreadyExists(group_name, node_name)

    async def update_node(self, group_name, node_name, host=None, port=None):
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.update_node(node_name, host, port)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)

    async def remove_node(self, group_name, node_name):
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.remove_node(node_name)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)

    async def get_node_attributes(self, group_name, node_name):
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            return node_group.get_node_attributes(node_name)
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)

    async def get_node_attribute(self, group_name, node_name, attribute_name):
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            return node_group.get_node_attribute(node_name, attribute_name)
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)
        except UnknownNodeAttributeError:
            raise UnknownNodeFromGroupAttributeError(group_name, node_name, attribute_name)

    async def create_node_attribute(self, group_name, node_name, attribute_name, value, weight):
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.add_node_attribute(node_name, attribute_name, value, weight)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)
        except NodeAttributeAlreadyExistsError:
            raise NodeFromGroupAttributeAlreadyExistsError(group_name, node_name, attribute_name)

    async def update_node_attribute(self, group_name, node_name, attribute_name, value=None, weight=None):
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.update_node_attribute(node_name, attribute_name, value, weight)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)
        except UnknownNodeAttributeError:
            raise UnknownNodeFromGroupAttributeError(group_name, node_name, attribute_name)

    async def remove_node_attribute(self, group_name, node_name, attribute_name):
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.remove_node_attribute(node_name, attribute_name)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)
        except UnknownNodeAttributeError:
            raise UnknownNodeFromGroupAttributeError(group_name, node_name, attribute_name)
