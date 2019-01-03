class Config:

    __mongo_url = 'mongodb://localhost:27017/'
    __db = 'trashmail-lmtp'
    __max_age = 60
    __runUser = "cf"
    __runGrp = "cf"
    __lockFileDir = '/tmp/lmtp-server'
    __bind = "127.0.0.1"
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
