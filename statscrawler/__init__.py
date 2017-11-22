import asyncio

from core.api import AdvancedLoadbalancerAPI
from core.config import Config
from statscrawler.collector import CPULoad, MemoryLoad, CollectingError
from statscrawler.remote import CommandExecutor


class StatsCrawler(object):

    def __init__(self):
        self.__config = Config()
        self.__api = AdvancedLoadbalancerAPI(self.__config.get_attribute('api_url'))
        self.__interval = int(self.__config.get_attribute('interval') or 10)
        command_executor = CommandExecutor(self.__config.get_attribute('username'),
                                           self.__config.get_attribute('password'))
        self.__collectors = {
            'cpu': CPULoad(command_executor),
            'memory': MemoryLoad(command_executor)
        }

    async def main(self):
        while True:
            print("Trying to obtain node groups...")
            node_groups = await self.__api.get_node_groups()
            print("Obtained node groups successfully!")
            for group_name, group in node_groups.items():
                for node_name, node in group['nodes'].items():
                    for attribute_name, attribute in node['attributes'].items():
                        collector = self.__collectors.get(attribute_name, None)
                        if self.__collectors.get(attribute_name, None) is not None:
                            print("Will try to collect '{}' of the '{}' from group '{}'.".format(attribute_name,
                                                                                                 node_name, group_name))
                            collection_task = self.__collect(collector, group_name, node_name, attribute_name,
                                                             node['host'])
                            asyncio.ensure_future(collection_task)
            await asyncio.sleep(self.__interval)

    async def __collect(self, collector, group, node, attribute, host):
        try:
            print("Trying to collect '{}' of the '{}' from group '{}'...".format(attribute, node, group))
            value = await collector.collect(host)
            await self.__api.update_attribute(group, node, attribute, value=value)
            print("Successfully collected '{}' of the '{}' from group '{}'.".format(attribute, node, group))
        except CollectingError as e:
            print(e)
