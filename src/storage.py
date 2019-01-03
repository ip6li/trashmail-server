import email
import time
import json
import hashlib
from storage_mongodb import Mongo


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
        parser = email.message_from_bytes(data)
        field = "X-Original-To"
        if field in parser:
            key = parser[field]
        else:
            return False

        timestamp = int(time.time())
        m = hashlib.sha256()
        m.update(str(timestamp).encode("utf8"))
        m.update(key.encode("utf8"))
        msg = {
            "id": m.hexdigest().encode("utf8"),
            "X-Original-To": key,
            "timestamp": timestamp,
            "mailPeer": peer,
            "mailFrom": mailfrom,
            "mailTo": rcpttos,
            "data": data.decode('utf8').replace("'", '"'),
            "headers": kwargs
        }

        res = Mongo.insert(msg)
        if res is not None:
            return True
        else:
            return False

    @staticmethod
    def toJson(data):
        return json.dumps(data)
