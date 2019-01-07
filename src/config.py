import configparser
import pwd
import grp
import getpass
import os


class Config:
    __mongo_url = 'mongodb://127.0.0.1:27017/'
    __db = 'trashmail-lmtp'
    __max_age = 60
    __runUser = getpass.getuser()
    __runGrp = grp.getgrnam(__runUser).gr_name
    __lockFileDir = '/tmp/lmtp-server'
    __bind = "127.0.0.1"
    __port = 10025

    @staticmethod
    def createConfig(filename, config):
        with open(filename, 'w') as configfile:
            config.write(configfile)

    @staticmethod
    def loadConfig():
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'mongo_url': 'mongodb://127.0.0.1:27017/',
            'mongo_db': 'trashmail-lmtp',
            'max_age': 60,
            'lockFileDir': '/tmp/lmtp-server',
            'bind': '127.0.0.1',
            'port': 10025
        }
        configFile = pwd.getpwnam(Config.__runUser).pw_dir + "/.trashmail/lmtp-server.ini"
        if os.path.isfile(configFile):
            config.read(configFile)
        else:
            with open(configFile, 'w') as configfile:
                config.write(configfile)

        for section in config:
            for i in config[section]:
                print(i + ": " + config[section][i])

    @staticmethod
    def getMongoURL():
        return Config.__mongo_url

    @staticmethod
    def getDB():
        return Config.__db

    @staticmethod
    def getMaxAge():
        return Config.__max_age

    @staticmethod
    def getRunUser():
        return Config.__runUser

    @staticmethod
    def getRunGrp():
        return Config.__runGrp

    @staticmethod
    def getLockFileDir():
        return Config.__lockFileDir

    @staticmethod
    def getBind():
        return Config.__bind

    @staticmethod
    def getPort():
        return Config.__port
