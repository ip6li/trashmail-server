import os


class Config:

    __mongo_url = 'mongodb://172.16.239.11:27017/'
    __db = 'trashmail-lmtp'
    __max_age = 60
    __runUser = "cf"
    if os.uname().sysname=="Darwin":
        __runGrp = "staff"
    else:
        __runGrp = "cf"
    __lockFileDir = '/tmp/lmtp-server'
    __bind = "192.168.1.202"
    __port = 10025


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

    @staticmethod
    def getAppName():
        return "lmtp-server"
