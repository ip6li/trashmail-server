class Server:
    server = None
    threadLock = None
    lmtpChannel = None
    redisServer = {
        "host": None,
        "port": 0
    }


    @staticmethod
    def setServer(server):
        Server.server = server

    @staticmethod
    def getServer():
        return Server.server

    @staticmethod
    def setThreadLock(threadLock):
        Server.threadLock = threadLock

    @staticmethod
    def getThreadLock():
        return Server.threadLock

    @staticmethod
    def setChannel (channel):
        Server.lmtpChannel = channel

    @staticmethod
    def getChannel ():
        return Server.lmtpChannel


