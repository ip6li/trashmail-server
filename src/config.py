import configparser
import pwd
import grp
import getpass
import os
from logger import Logger


class Config:
    __runUser = getpass.getuser()
    __runGrp = grp.getgrnam(__runUser).gr_name
    __config = None

    @staticmethod
    def __getItem(s):
        if Config.__config is None:
            Config.initConfig()
        return Config.__config["DEFAULT"][s]

    @staticmethod
    def createConfig(filename, config):
        with open(filename, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def initConfig():
        Config.__config = Config.__loadConfig()

    @staticmethod
    def __loadConfig():
        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            'mongo_url': 'mongodb://127.0.0.1:27017/',
            'mongo_db': 'trashmail-lmtp',
            'max_age': 60,
            'lockFileDir': '/tmp/lmtp-server',
            'bind': '127.0.0.1',
            'port': 10025,
            'timeout': 10000
        }
        config_file = pwd.getpwnam(Config.__runUser).pw_dir + "/.trashmail/lmtp-server.ini"
        if os.path.isfile(config_file):
            config.read(config_file)
        else:
            with open(config_file, 'w') as configfile:
                config.write(configfile)

        log = Logger(__name__)
        for section in config:
            for i in config[section]:
                log.debug(i + ": " + config[section][i])

        return config

    @staticmethod
    def getMongoURL():
        return Config.__getItem("mongo_url")

    @staticmethod
    def getDB():
        return Config.__getItem("mongo_db")

    @staticmethod
    def getMaxAge():
        return Config.__getItem("max_age")

    @staticmethod
    def getTimeout():
        return int(Config.__getItem("timeout"))
