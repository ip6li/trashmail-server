class RedisConfig:
    config = {
        "host": None,
        "port": 0
    }

    @staticmethod
    def setRedisServer (host, port):
        RedisConfig.config["host"] = host
        RedisConfig.config["port"] = port

    @staticmethod
    def getRedisServer():
        return RedisConfig.config
