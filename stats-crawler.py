import asyncio

import asyncssh

from core.api import AdvancedLoadbalancerAPI
from core.config import Config


class CommandExecutionError(Exception):

    def __init__(self, code, stderr):
        message = "Process exited with code {}. Error log:\n{}".format(code, stderr)
        super(CommandExecutionError, self).__init__(message)


class CommandExecutor(object):

    def __init__(self, username, password):
        if username is None:
            raise Exception("USERNAME parameter was not specified")
        if password is None:
            raise Exception("PASSWORD parameter was not specified")
        self.__username = username
        self.__password = password

    async def execute(self, host, command):
        async with asyncssh.connect(host, username=self.__username, password=self.__password) as connection:
            result = await connection.run(command)
            if result.exit_status == 0:
                return result.stdout
            else:
                raise CommandExecutionError(result.exit_status, result.stderr)


class Collector(object):
    _command = None
    _metric_name = None

    def __init__(self, executor):
        self.__executor = executor

    async def collect(self, host):
        try:
            data = await self.__executor.execute(host, self._command)
            return data.strip()
        except Exception as e:
            message = "Failed to collect a {} for the '{}' - {}".format(self._metric_name, host, e)
            print(message)


class CPULoad(Collector):
    _command = "grep 'cpu' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
    _metric = "CPU load"


class MemoryLoad(Collector):
    _command = "free | grep 'Mem' | awk '{print $7}'"
    _metric = "free memory"


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
        print("Trying to collect '{}' of the '{}' from group '{}'...".format(attribute, node, group))
        value = await collector.collect(host)
        await self.__api.update_attribute(group, node, attribute, value=value)
        print("Successfully collected '{}' of the '{}' from group '{}'.".format(attribute, node, group))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(StatsCrawler().main())
