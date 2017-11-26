import os


class Config(object):
    """A configuration of an individual application.

    Attributes:
        __option_prefix (str): Prefix in the name of each option of the application.

    """
    def __init__(self, option_prefix=''):
        """Constructor of the Config.

        Args:
            option_prefix (str): Prefix in the name of each option of the application.

        """
        self.__option_prefix = option_prefix

    def get_attribute(self, name):
        """Return the value of the specified option.

        Args:
            name (str): Named of the option without a prefix in it.

        Returns:
            str: Value of the option. If there is no option with such name, None is returned instead.

        """
        return os.environ.get(name.upper(), None)
