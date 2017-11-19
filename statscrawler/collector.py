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
