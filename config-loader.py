import asyncio
import json

from core.api import AdvancedLoadbalancerAPI, APIError
from core.config import Config


GROUP_CREATION_FAILURE = "Failed to create a node group '{group}' - {reason}"
"""Group creation failure message template."""
NODE_CREATION_FAILURE = "Failed to create a node '{node}' in the group '{group}' - {reason}"
"""Node creation failure message template."""
ATTRIBUTE_CREATION_FAILURE = "Failed to add an attribute '{attribute}' to the node '{node}' " \
                             "of the group '{group}' - {reason}"
"""Attribute creation failure message template."""


class ConfigLoader(object):
    """config-loader service root class.

    Loads configuration from the specified JSON file and loads the configuration the ALB via its API.

    Attributes:
        __config (Config): Configuration of the application.
        __config_path (str): Path to the JSON configuration file.
        __api (AdvancedLoadbalancerAPI): API of the ALB.

    """
    def __init__(self):
        """Constructor of the ConfigLoader."""
        self.__config = Config()
        self.__config_path = self.__config.get_attribute('config_path') or './config.json'
        self.__api = AdvancedLoadbalancerAPI(self.__config.get_attribute('api_url'))

    async def main(self):
        """Entry-point of the ConfigLoader. Load configuration from the specified file and load it into the ALB
        using its API.

        Note: awaitable method.

        """
        print("Loading config...")
        config = self.__load_config()
        print("Loaded config successfully!")
        for group_name, group in config.items():
            try:
                print("Adding node group '{}'...".format(group_name))
                await self.__api.create_node_group(group_name)
            except APIError as e:
                print(GROUP_CREATION_FAILURE.format(group=group_name, reason=e))
                continue
            for node_name, node in group['nodes'].items():
                try:
                    print("Adding node '{}' to the group '{}'...".format(node_name, group_name))
                    await self.__api.create_node(group_name, node_name, node['host'], node['port'])
                except APIError as e:
                    print(NODE_CREATION_FAILURE.format(node=node_name, group=group_name, reason=e))
                    continue
                for attribute_name, attribute in node['attributes'].items():
                    try:
                        print("Adding attribute '{}' to the node '{}' of the group '{}'".format(attribute_name,
                                                                                                node_name, group_name))
                        await self.__api.create_attribute(group_name, node_name, attribute_name,
                                                          attribute['value'], attribute['weight'])
                    except APIError as e:
                        print(ATTRIBUTE_CREATION_FAILURE.format(attribute=attribute_name, node=node_name,
                                                                group=group_name, reason=e))
                        continue
        print("Configuration applied.")

    def __load_config(self):
        """Return configuration, that should be loaded into the ALB.

        Returns:
            dict: Configuration of the ALB.

        """
        with open(self.__config_path, 'r') as config:
            return json.load(config)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(ConfigLoader().main())
