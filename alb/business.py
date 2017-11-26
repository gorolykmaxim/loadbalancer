class BusinessProcessError(Exception):
    """Base class for an business layer exceptions."""
    pass


class UnknownAttributeError(BusinessProcessError):
    """Attribute with the specified name was not found.

    Error, raised when an attribute with the specified name was not found.

    """
    def __init__(self, attribute_name):
        """Constructor of the UnknownAttributeError.

        Args:
            attribute_name (str): Name of the attribute.

        """
        message = "Unknown attribute: '{}'".format(attribute_name)
        super(UnknownAttributeError, self).__init__(message)


class UnknownNodeAttributeError(BusinessProcessError):
    """Attribute with the specified name was not found.

    Error, raised when an attribute with the specified name was not found in the specified node.

    """
    def __init__(self, node_name, attribute_name):
        """Constructor of the UnknownNodeAttributeError.

        Args:
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        """
        message = "Node with name '{}' has no attribute '{}'".format(node_name, attribute_name)
        super(UnknownNodeAttributeError, self).__init__(message)


class UnknownNodeFromGroupAttributeError(BusinessProcessError):
    """Attribute with the specified name was not found.

    Error, raised when an attribute with the specified name was not found in the node of the specified node group.

    """
    def __init__(self, group_name, node_name, attribute_name):
        """Constructor of the UnknownNodeFromGroupAttributeError.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        """
        message = "Node from group '{}' with name '{}' has no attribute '{}'".format(group_name, node_name,
                                                                                     attribute_name)
        super(UnknownNodeFromGroupAttributeError, self).__init__(message)


class UnknownNodeError(BusinessProcessError):
    """Node with the specified name was not found."""
    def __init__(self, node_name):
        """Constructor of the UnknownNodeError.

        Args:
            node_name (str): Name of the node.

        """
        super(UnknownNodeError, self).__init__("Unknown node: '{}'".format(node_name))


class UnknownNodeFromGroupError(BusinessProcessError):
    """Node with the specified name was not found in the specified group."""
    def __init__(self, group_name, node_name):
        """Constructor of the UnknownNodeFromGroupError.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.

        """
        message = "There is no node with the name '{}' in the group '{}'".format(node_name, group_name)
        super(UnknownNodeFromGroupError, self).__init__(message)


class UnknownNodeGroupError(BusinessProcessError):
    """Node group with the specified name was not found."""
    def __init__(self, group_name):
        """Constructor of the UnknownNodeGroupError.

        Args:
            group_name (str): Name of the group.

        """
        message = "Node group with the name '{}' does not exist".format(group_name)
        super(UnknownNodeGroupError, self).__init__(message)


class AttributeAlreadyExistsError(BusinessProcessError):
    """Attribute with the specified name already exists."""
    def __init__(self, attribute_name):
        """Constructor of the AttributeAlreadyExistsError.

        Args:
            attribute_name (str): Name of the attribute.

        """
        message = "Attribute with the name '{}' already exists".format(attribute_name)
        super(AttributeAlreadyExistsError, self).__init__(message)


class NodeAttributeAlreadyExistsError(BusinessProcessError):
    """The node already the attribute with the specified name."""
    def __init__(self, node_name, attribute_name):
        """Constructor of the NodeAttributeAlreadyExistsError.

        Args:
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        """
        message = "Node '{}' already has an attribute, called '{}'".format(node_name, attribute_name)
        super(NodeAttributeAlreadyExistsError, self).__init__(message)


class NodeFromGroupAttributeAlreadyExistsError(BusinessProcessError):
    """The node from the node group already has an attribute with the specified name."""
    def __init__(self, group_name, node_name, attribute_name):
        """Constructor of the NodeFromGroupAttributeAlreadyExistsError.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        """
        message = "Node '{}' from the group '{}' already has an attribute, called '{}'".format(node_name, group_name,
                                                                                               attribute_name)
        super(NodeFromGroupAttributeAlreadyExistsError, self).__init__(message)


class NodeAlreadyExistsError(BusinessProcessError):
    """Node with the specified name already exists."""
    def __init__(self, node_name):
        """Constructor of the NodeAlreadyExistsError.

        Args:
            node_name (str): Name of the node.

        """
        super(NodeAlreadyExistsError, self).__init__("Node '{}' already exists".format(node_name))


class NodeFromGroupAlreadyExists(BusinessProcessError):
    """Specified node group already contains a node with the specified name."""
    def __init__(self, group_name, node_name):
        """Constructor of the NodeFromGroupAlreadyExists.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.

        """
        message = "Group '{}' already has a node, called '{}'".format(group_name, node_name)
        super(NodeFromGroupAlreadyExists, self).__init__(message)


class Attribute(object):
    """An attribute of the Node.

    Attributes:
        __value (float): Current value of the Attribute.
        __weight (float): Static weight of the Attribute's value.

    """
    def __init__(self, value, weight):
        """Constructor of the Attribute.

        Args:
            value (float): Current value of the Attribute.
            weight (float): Static weight of the Attribute.

        """
        self.__value = float(value)
        self.__weight = float(weight)

    @property
    def value(self):
        """Return the value of the Attribute.

        Returns:
            float: current value of the Attribute.

        """
        return self.__value

    @value.setter
    def value(self, value):
        """Set current value of the Attribute.

        Args:
            value (float): Current value of the Attribute.

        """
        self.__value = float(value)

    @property
    def weight(self):
        """Return the static weight of the Attribute.

        Returns:
            float: static weight of the Attribute.

        """
        return self.__weight

    @weight.setter
    def weight(self, value):
        """Set static weight of the Attribute.

        Args:
            value (float): Static weight of the Attribute.

        """
        self.__weight = float(value)

    @property
    def current_weight(self):
        """Return current weight of the Attribute based on its current value and static weight.

        Returns:
            float: Current weight of the Attribute.

        """
        return self.__value * self.__weight


class Node(object):
    """A node of the cluster.

    Attributes:
        host (str): Host, on which node accepts incoming messages.
        __port (int): Port, on which node accepts incoming messages.
        __attributes (dict): Named list of attributes of the node.

    """
    def __init__(self, host, port):
        """Constructor of the Node.

        Args:
            host (str): Host of the node.
            port (int): Port of the node.

        """
        self.host = host
        self.__port = int(port)
        self.__attributes = {}

    @property
    def port(self):
        """Return the port number, on which Node listens for incoming messages.

        Returns:
            int: Port of the Node.

        """
        return self.__port

    @port.setter
    def port(self, value):
        """Set the listening port of the Node.

        Args:
            value (int): Port of the Node.

        """
        self.__port = int(value)

    def get_attributes(self):
        """Return a named list of attributes of the Node.

        Returns:
            dict: Attributes of the node.

        """
        attributes = {}
        for name, attribute in self.__attributes.items():
            attributes[name] = {
                'value': attribute.value,
                'weight': attribute.weight
            }
        return attributes

    def get_attribute(self, name):
        """Return a specified attribute of the Node.

        Args:
            name (str): Name of the attribute.

        Returns:
            dict: Attribute of the Node with the specified name.

        Raises:
            UnknownAttributeError: If the attribute with the specified name was not found.

        """
        try:
            attribute = self.__attributes[name]
            return {
                'value': attribute.value,
                'weight': attribute.weight
            }
        except KeyError:
            raise UnknownAttributeError(name)

    def add_attribute(self, name, value, weight):
        """Add an attribute to the Node.

        Args:
            name (str): Name of the new attribute.
            value (float): Current value of the attribute.
            weight (float): Static weight of the attribute.

        Raises:
            AttributeAlreadyExists: If Node already has an attribute with the specified name.

        """
        if name in self.__attributes:
            raise AttributeAlreadyExistsError(name)
        self.__attributes[name] = Attribute(value, weight)

    def update_attribute(self, name, value=None, weight=None):
        """Update an attribute information of the Node.

        Args:
            name (str): Name of the attribute.
            value (float): Current value of the attribute.
            weight (float): Static weight of the attribute.

        Raises:
            UnknownAttributeError: If the attribute with the specified name was not found.

        """
        try:
            attribute = self.__attributes[name]
            attribute.value = value or attribute.value
            attribute.weight = weight or attribute.weight
        except KeyError:
            raise UnknownAttributeError(name)

    def remove_attribute(self, name):
        """Remove the attribute of the Node.

        Args:
            name (str): Name of the attribute.

        Raises:
            UnknownAttributeError: If the attribute with the specified name was not found.

        """
        try:
            self.__attributes.pop(name)
        except KeyError:
            raise UnknownAttributeError(name)

    @property
    def weight(self):
        """Return overall weight of the Node based on its attributes.

        Returns:
            float: Overall weight of the Node.

        """
        return sum([attribute.current_weight for attribute in self.__attributes.values()])


class NodeGroup(object):
    """Group of nodes, that serve the same service.

    Attributes:
        __nodes (dict): Named list of nodes of the NodeGroup.

    """
    def __init__(self):
        """Constructor of the NodeGroup."""
        self.__nodes = {}

    def get_nodes_list(self):
        """Return the list of nodes of the NodeGroup.

        Returns:
            list: List of nodes.

        """
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
        """Return named list of node of the NodeGroup.

        Returns:
            dict: Named list of nodes.

        """
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
        """Return information about the node of the NodeGroup.

        Args:
            name (str): Name of the node to return.

        Returns:
            dict: Node of the NodeGroup, that has a specified name.

        Raises:
            UnknownNodeError: If the node with the specified name was not found.

        """
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
        """Add a node to the NodeGroup.

        Args:
            name (str): Name of the new node.
            host (str): Host of the node.
            port (int): Port of the node.

        Raises:
            NodeAlreadyExistsError: If Node with the specified node already exists in the NodeGroup.

        """
        if name in self.__nodes:
            raise NodeAlreadyExistsError(name)
        self.__nodes[name] = Node(host, port)

    def update_node(self, name, host=None, port=None):
        """Update an information of the node from the NodeGroup.

        Args:
            name (str): Name of the node.
            host (str): Host of the node.
            port (int): Port of the node.

        Raises:
            UnknownNodeError: If the node with the specified name was not found.

        """
        try:
            node = self.__nodes[name]
            node.host = host or node.host
            node.port = port or node.port
        except KeyError:
            raise UnknownNodeError(name)

    def remove_node(self, name):
        """Remove the node from the NodeGroup.

        Args:
            name (str): Name of the node.

        Raises:
            UnknownNodeError: If the node with the specified name was not found.

        """
        try:
            self.__nodes.pop(name)
        except KeyError:
            raise UnknownNodeError(name)

    def get_node_attributes(self, node_name):
        """Return named list of node attributes.

        Args:
            node_name (str): Name of the node.

        Returns:
            dict: Named list of attributes.

        Raises:
            UnknownNodeError: If the node with the specified name was not found.

        """
        try:
            return self.__nodes[node_name].get_attributes()
        except KeyError:
            raise UnknownNodeError(node_name)

    def get_node_attribute(self, node_name, attribute_name):
        """Return information about the attribute of the node.

        Args:
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        Returns:
            dict: Attribute of the node.

        Raises:
            UnknownNodeError: If the node with the specified name was not found.
            UnknownNodeAttributeError: If the node does not have a specified attribute.

        """
        try:
            node = self.__nodes[node_name]
            return node.get_attribute(attribute_name)
        except KeyError:
            raise UnknownNodeError(node_name)
        except UnknownAttributeError:
            raise UnknownNodeAttributeError(node_name, attribute_name)

    def add_node_attribute(self, node_name, attribute_name, value, weight):
        """Add an attribute to the Node.

        Args:
            node_name (str): Name of the node.
            attribute_name (str): Name of the new attribute.
            value (float): Current value of the attribute.
            weight (float): Static weight of the attribute.

        Raises:
            UnknownNodeError: If the node with the specified name was not found.
            NodeAttributeAlreadyExistsError: If the node already has an attribute with the specified name.

        """
        try:
            node = self.__nodes[node_name]
            node.add_attribute(attribute_name, value, weight)
        except KeyError:
            raise UnknownNodeError(node_name)
        except AttributeAlreadyExistsError:
            raise NodeAttributeAlreadyExistsError(node_name, attribute_name)

    def update_node_attribute(self, node_name, attribute_name, value=None, weight=None):
        """Update an information of the attribute of the node.

        Args:
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.
            value (float): Current value of the attribute.
            weight (float): Static weight of the attribute.

        Raises:
            UnknownNodeError: If the node with the specified name was not found.
            UnknownNodeAttributeError: If the node does not have an attribute with the specified name.

        """
        try:
            node = self.__nodes[node_name]
            node.update_attribute(attribute_name, value, weight)
        except KeyError:
            raise UnknownNodeError(node_name)
        except UnknownAttributeError:
            raise UnknownNodeAttributeError(node_name, attribute_name)

    def remove_node_attribute(self, node_name, attribute_name):
        """Remove the attribute of the node.

        Args:
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        Raises:
            UnknownNodeError: If the node with the specified name was not found.
            UnknownNodeAttributeError: If the node does not have an attribute with the specified name.

        """
        try:
            node = self.__nodes[node_name]
            node.remove_attribute(attribute_name)
        except KeyError:
            raise UnknownNodeError(node_name)
        except UnknownAttributeError:
            raise UnknownNodeAttributeError(node_name, attribute_name)


class NodeGroupRepository(object):
    """Repository of NodeGroups.

    Keeps named list of NodeGroups, and provides an interface to modify it.

    Attributes:
        __node_groups (dict): Named list of NodeGroups.

    """
    def __init__(self):
        """Constructor of the NodeGroupRepository."""
        self.__node_groups = {}

    def get_node_group(self, name):
        """Return the NodeGroup with the specified name.

        Args:
            name (str): Name of the NodeGroup.

        Returns:
            NodeGroup: NodeGroup with the specified name.

        Raises:
            UnknownNodeGroupError: If there is no NodeGroup with the specified name.

        """
        try:
            return self.__node_groups[name]
        except KeyError:
            raise UnknownNodeGroupError(name)

    def get_node_groups(self):
        """Return a named list of all NodeGroups.

        Returns:
            dict: Named list of all NodeGroups.

        """
        return self.__node_groups

    def save(self, name, node_group):
        """Save a NodeGroup with a specified name in the NodeGroupRepository.

        Args:
            name (str): Name of the NodeGroup.
            node_group (NodeGroup): NodeGroup to save.

        """
        self.__node_groups[name] = node_group

    def remove(self, name):
        """Remove a NodeGroup from the NodeGroupRepository.

        Args:
            name (str): Name of the NodeGroup.

        Raises:
            UnknownNodeGroupError: If there is no NodeGroup with the specified name.

        """
        try:
            self.__node_groups.pop(name)
        except KeyError:
            raise UnknownNodeGroupError(name)


class BusinessLayerFacade(object):
    """A facade of the business layer.

    An interface for business processes execution.

    Attributes:
        __integration_layer (IntegrationLayer): An integration layer of the application.
        __node_group_repository (NodeGroupRepository): Repository of NodeGroups.

    """
    def __init__(self, integration_layer):
        """Constructor of the BusinessLayerFacade.

        Args:
            integration_layer (IntegrationLayer): An integration layer of the application.

        """
        self.__integration_layer = integration_layer
        self.__node_group_repository = NodeGroupRepository()

    async def get_node_groups(self):
        """Return a named list of all NodeGroups.

        Note: awaitable method.

        Returns:
            dict: Named list of all NodeGroups.

        """
        node_groups = self.__node_group_repository.get_node_groups()
        groups = {}
        for name, node_group in node_groups.items():
            groups[name] = {'nodes': node_group.get_nodes()}
        return groups

    async def get_node_group(self, group_name):
        """Return the node group with the specified name.

        Note: awaitable method.

        Args:
            group_name (str): Name of the NodeGroup.

        Returns:
            dict: Node group with the specified name.

        Raises:
            UnknownNodeGroupError: If there is no node group with the specified name.

        """
        node_group = self.__node_group_repository.get_node_group(group_name)
        return {'nodes': node_group.get_nodes()}

    async def create_node_group(self, group_name):
        """Create a node group with the specified name.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.

        """
        node_group = NodeGroup()
        self.__node_group_repository.save(group_name, node_group)

    async def remove_node_group(self, group_name):
        """Remove a node group with the specified name and notify a proxy about it.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.

        Raises:
            ProxyError: If application was not able to notify a proxy.

        """
        self.__node_group_repository.remove(group_name)
        await self.__integration_layer.submit_node_group_to_proxy(group_name, [])

    async def get_nodes(self, group_name):
        """Return nodes of the specified NodeGroup.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.

        Returns:
            dict: Nodes from the specified group.

        Raises:
            UnknownNodeGroupError: If there is no node group with the specified name.

        """
        node_group = self.__node_group_repository.get_node_group(group_name)
        return node_group.get_nodes()

    async def get_node(self, group_name, node_name):
        """Return a specific node of the node group.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.

        Returns:
            dict: Node information.

        Raises:
            UnknownNodeGroupError: If there is no node group with the specified name.
            UnknownNodeFromGroupError: If there is no node in group with the specified name.

        """
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            return node_group.get_node(node_name)
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)

    async def create_node(self, group_name, node_name, host, port):
        """Create a node in the specified group and notify proxy about it.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            host (str): Host of the node.
            port (int): Port of the node.

        Raises:
            ProxyError: If application was not able to notify a proxy.
            UnknownNodeGroupError: If there is no node group with the specified name.
            NodeFromGroupAlreadyExists: If the node with the specified name already exists in the group.

        """
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.add_node(node_name, host, port)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except NodeAlreadyExistsError:
            raise NodeFromGroupAlreadyExists(group_name, node_name)

    async def update_node(self, group_name, node_name, host=None, port=None):
        """Update an information of the node from the specified group and notify proxy about it.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            host (str): Host of the node.
            port (int): Port of the node.

        Raises:
            ProxyError: If application was not able to notify a proxy.
            UnknownNodeGroupError: If there is no node group with the specified name.
            UnknownNodeFromGroupError: If there is no node with the specified name in the group.

        """
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.update_node(node_name, host, port)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)

    async def remove_node(self, group_name, node_name):
        """Remove a node from the specified node group and notify proxy about it.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.

        Raises:
            ProxyError: If application was not able to notify a proxy.
            UnknownNodeGroupError: If there is no node group with the specified name.
            UnknownNodeFromGroupError: If there is no node with the specified name in the group.

        """
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.remove_node(node_name)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)

    async def get_node_attributes(self, group_name, node_name):
        """Return a named list of attribute of the specified node.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.

        Returns:
            dict: Named list of attributes.

        Raises:
            UnknownNodeGroupError: If there is no node group with the specified name.
            UnknownNodeFromGroupError: If there is no node with the specified name in the group.

        """
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            return node_group.get_node_attributes(node_name)
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)

    async def get_node_attribute(self, group_name, node_name, attribute_name):
        """Return an information about a specific attribute of the node.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        Returns:
            dict: Information about the attribute.

        Raises:
            UnknownNodeGroupError: If there is no node group with the specified name.
            UnknownNodeFromGroupError: If there is no node with the specified name in the group.
            UnknownNodeFromGroupAttributeError: If node does not have a specified attribute.

        """
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            return node_group.get_node_attribute(node_name, attribute_name)
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)
        except UnknownNodeAttributeError:
            raise UnknownNodeFromGroupAttributeError(group_name, node_name, attribute_name)

    async def create_node_attribute(self, group_name, node_name, attribute_name, value, weight):
        """Add an attribute to the specified node and notify proxy about it.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.
            value (float): Current value of the attribute.
            weight (float): Static weight of the attribute.

        Raises:
            ProxyError: If application was not able to notify a proxy.
            UnknownNodeGroupError: If there is no node group with the specified name.
            UnknownNodeFromGroupError: If there is no node with the specified name in the group.
            NodeFromGroupAttributeAlreadyExistsError: If node already has an attribute with the specified name.

        """
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.add_node_attribute(node_name, attribute_name, value, weight)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)
        except NodeAttributeAlreadyExistsError:
            raise NodeFromGroupAttributeAlreadyExistsError(group_name, node_name, attribute_name)

    async def update_node_attribute(self, group_name, node_name, attribute_name, value=None, weight=None):
        """Update an information of the attribute of the specified node and notify proxy about it.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.
            value (float): Current value of the attribute.
            weight (float): Static weight of the attribute.

        Raises:
            ProxyError: If application was not able to notify a proxy.
            UnknownNodeGroupError: If there is no node group with the specified name.
            UnknownNodeFromGroupError: If there is no node with the specified name in the group.
            UnknownNodeFromGroupAttributeError: If node does not have a specified attribute.

        """
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.update_node_attribute(node_name, attribute_name, value, weight)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)
        except UnknownNodeAttributeError:
            raise UnknownNodeFromGroupAttributeError(group_name, node_name, attribute_name)

    async def remove_node_attribute(self, group_name, node_name, attribute_name):
        """Remove the attribute of the specified node and notify proxy about it.

        Note: awaitable method.

        Args:
            group_name (str): Name of the group.
            node_name (str): Name of the node.
            attribute_name (str): Name of the attribute.

        Raises:
            ProxyError: If application was not able to notify a proxy.
            UnknownNodeGroupError: If there is no node group with the specified name.
            UnknownNodeFromGroupError: If there is no node with the specified name in the group.
            UnknownNodeFromGroupAttributeError: If node does not have a specified attribute.

        """
        try:
            node_group = self.__node_group_repository.get_node_group(group_name)
            node_group.remove_node_attribute(node_name, attribute_name)
            await self.__integration_layer.submit_node_group_to_proxy(group_name, node_group.get_nodes_list())
        except UnknownNodeError:
            raise UnknownNodeFromGroupError(group_name, node_name)
        except UnknownNodeAttributeError:
            raise UnknownNodeFromGroupAttributeError(group_name, node_name, attribute_name)
