import asyncio
import json

from core.api import AdvancedLoadbalancerAPI, APIError
from core.config import Config


GROUP_CREATION_FAILURE = "Failed to create a node group '{group}' - {reason}"
NODE_CREATION_FAILURE = "Failed to create a node '{node}' in the group '{group}' - {reason}"
ATTRIBUTE_CREATION_FAILURE = "Failed to add an attribute '{attribute}' to the node '{node}' " \
                             "of the group '{group}' - {reason}"


class ConfigLoader(object):

    def __init__(self):
        self.__config = Config()
        self.__config_path = self.__config.get_attribute('config_path') or './config.json'
        self.__api = AdvancedLoadbalancerAPI(self.__config.get_attribute('api_url'))

    async def main(self):
        config = self.__load_config()
        for group_name, group in config.items():
            try:
                await self.__api.create_node_group(group_name)
            except APIError as e:
                print(GROUP_CREATION_FAILURE.format(group=group_name, reason=e))
                continue
            for node_name, node in group['nodes'].items():
                try:
                    await self.__api.create_node(group_name, node_name, node['host'], node['port'])
                except APIError as e:
                    print(NODE_CREATION_FAILURE.format(node=node_name, group=group_name, reason=e))
                    continue
                for attribute_name, attribute in node['attributes'].items():
                    try:
                        await self.__api.create_attribute(group_name, node_name, attribute_name,
                                                          attribute['value'], attribute['weight'])
                    except APIError as e:
                        print(ATTRIBUTE_CREATION_FAILURE.format(attribute=attribute_name, node=node_name,
                                                                group=group_name, reason=e))
                        continue

    def __load_config(self):
        with open(self.__config_path, 'r') as config:
            return json.load(config)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(ConfigLoader().main())
