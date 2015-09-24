

class Plugin(object):

    name = None

    def pull(self):
        pass

    def push(self):
        pass


class Plugins(object):

    def __init__(self):
        self.__plugins__ = {}

    def register(self, plugin):
        self.__plugins__[plugin.name] = plugin

    def __getitem__(self, item):
        return self.__plugins__[item]


plugins = Plugins()
