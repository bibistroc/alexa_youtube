from ConfigParser import ConfigParser
import os


class LocalConfig:
    def __init__(self):
        self.__configs = {}
        config_path = os.path.join(os.path.dirname(__file__), '../', 'config.ini')

        self.__config = ConfigParser()
        self.__config.read(config_path)

    def __key_finder(self, section):
        if section in self.__configs:
            return self.__configs[section]
        else:
            return self.__read_config(section)

    def __read_config(self, section):
        try:
            options = self.__config.options(section)
            configs = {}
            for option in options:
                configs[option] = self.__config.get(section, option)

            self.__configs[section] = configs
        except:
            self.__configs[section] = None
        return self.__configs[section]

    def __getattr__(self, item):
        return self.__key_finder(item.lower())



