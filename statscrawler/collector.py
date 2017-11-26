class CollectingError(Exception):
    """Error, that may occur during an attribute value collection attempt."""
    def __init__(self, metric_name, host, error):
        """Constructor of the CollectingError.

        Args:
            metric_name (str): Name of the attribute.
            host (str): Host of the node.
            error (Exception): Instance of the original error.

        """
        message = "Failed to collect a {} for the '{}' - {}".format(metric_name, host, error)
        super(CollectingError, self).__init__(message)


class Collector(object):
    """A base collector class.

    Executes a command, that returns a value of the attribute, that is collected by the collector,
    using an CommandExecutor instance.

    Attributes:
        _command (str): A command, that prints a value of the attribute in the STDOUT.
        _metric_name (str): Name of the metric that is being measured by the collector.

    """
    _command = None
    _metric_name = None

    def __init__(self, executor):
        """Constructor of the Collector.

        Args:
            executor (CommandExecutor): A command executor, that will be used to execute commands remotely.

        """
        self.__executor = executor

    async def collect(self, host):
        """Collect and return a value of the corresponding attribute of the specified host.

        Note: awaitable method.

        Args:
            host (str): Host of the remote node.

        Returns:
            str: Value of the attribute.

        Raises:
            CollectingError: If an error occurs during collection attempt.

        """
        try:
            data = await self.__executor.execute(host, self._command)
            return data.strip()
        except Exception as e:
            raise CollectingError(self._metric_name, host, e)


class CPULoad(Collector):
    """A collector of the CPU load.

    Collects a percentage of the CPU load at the current moment.

    """
    _command = "grep 'cpu' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
    _metric_name = "CPU load"


class MemoryLoad(Collector):
    """A collector of the memory load.

    Collects a size of RAM, that is free at the moment.

    """
    _command = "free | grep 'Mem' | awk '{print $7}'"
    _metric_name = "free memory"
