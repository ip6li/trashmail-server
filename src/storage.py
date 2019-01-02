import redis
import email
from redisconfig import RedisConfig
import json


class Storage:
    redis = None

    @staticmethod
    def printMsg(peer, mailfrom, rcpttos, data, **kwargs):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        print('Message               :', data)
        print("kwargs                :", kwargs)
        return

    @staticmethod
    def storeMsg(peer, mailfrom, rcpttos, data, **kwargs):
        msg = {
            "mailPeer": peer,
            "mailFrom": mailfrom,
            "mailTo": rcpttos,
            "data": data.decode('utf8').replace("'", '"'),
            "headers": kwargs
        }

        parser = email.message_from_bytes(data)
        field = "X-Original-To"
        if field in parser:
            key = parser[field]
            print(field, ': ', key)
            Storage.storeAsJson(key, msg)
            return True
        else:
            return False

    @staticmethod
    def open():
        redisServerConfig = RedisConfig.getRedisServer()
        Storage.redis = redis.Redis(host=redisServerConfig["host"], port=redisServerConfig["port"], db=0)
        return Storage.redis is not None

    @staticmethod
    def close():
        # do nothing yet
        return

    @staticmethod
    def store(key, value):
        return Storage.redis.set(key, value)

    @staticmethod
    def storeAsJson(key, value):
        json_data = json.dumps(value)
        return Storage.redis.set(key, json_data)

    @staticmethod
    def read(key):
        return Storage.redis.get(key)

