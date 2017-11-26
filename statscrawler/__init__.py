import asyncio

from core.api import AdvancedLoadbalancerAPI
from core.config import Config
from statscrawler.collector import CPULoad, MemoryLoad, CollectingError
from statscrawler.remote import CommandExecutor


class StatsCrawler(object):
    """stats-crawler service root class.

    StatsCrawler periodically collects information about attributes of the nodes of cluster
    and sends that information to the ALB.
    Supported attribute names are:
    - cpu
    - memory

    Attributes:
        __config (Config): Configuration of the application.
        __api (AdvancedLoadbalancerAPI): API of the ALB service.
        __interval (int): An interval between crawling attempts.
        __collectors (dict): Map, where each key corresponds to a specific attribute name and the value is a
            corresponding Collector instance, that can crawl specified attribute.

    """
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
        """Entry-point of the StatsCrawler. Get all node groups from the ALB, try to find nodes with known attribute
        names, try to collect their values using a corresponding collector and supply collected values back to the ALB.
        Repeat after a specified interval of time.

        Note: awaitable method.

        """
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
        """Collect a value of the specified attribute for the specified host and submit it to the ALB
        In case of failure an error message will be printed.

        Note: awaitable method.

        Args:
            collector (Collector): Instance of the Collector to collect the specified attribute.
            group (str): Name of the group.
            node (str): Name of the node.
            attribute (str): Name of the attribute.
            host (str): Host of the remote node.

        """
        try:
            print("Trying to collect '{}' of the '{}' from group '{}'...".format(attribute, node, group))
            value = await collector.collect(host)
            await self.__api.update_attribute(group, node, attribute, value=value)
            print("Successfully collected '{}' of the '{}' from group '{}'.".format(attribute, node, group))
        except CollectingError as e:
            print(e)
