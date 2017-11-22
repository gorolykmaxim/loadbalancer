class CollectingError(Exception):

    def __init__(self, metric_name, host, error):
        message = "Failed to collect a {} for the '{}' - {}".format(metric_name, host, error)
        super(CollectingError, self).__init__(message)


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
            raise CollectingError(self._metric_name, host, e)


class CPULoad(Collector):
    _command = "grep 'cpu' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
    _metric_name = "CPU load"


class MemoryLoad(Collector):
    _command = "free | grep 'Mem' | awk '{print $7}'"
    _metric_name = "free memory"
