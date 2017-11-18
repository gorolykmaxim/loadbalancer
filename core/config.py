import os


class Config(object):

    def __init__(self, option_prefix=''):
        self.__option_prefix = option_prefix

    def get_attribute(self, name):
        return os.environ.get(name.upper(), None)
