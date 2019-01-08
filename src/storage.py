import time
import json
import hashlib
import re
from storage_mongodb import Mongo
from logger import Logger
from parser import MailParser
from email.utils import parseaddr


class Storage:

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
    def extractRFC822(src):
        return parseaddr(src)[1]

    @staticmethod
    def storeMsg(peer, mailfrom, rcpttos, data, **kwargs):
        headers = MailParser.parseMail(data)
        if headers["X-Original-To"] is not None:
            key = headers["X-Original-To"]
            Logger.debug("X-Original-To found")
        else:
            key = rcpttos
            Logger.debug("X-Original-To not found")
        print("key: ", key)
        try:
            timestamp = int(time.time())
            msg = {
                "X-Original-To": key,
                "timestamp": timestamp,
                "mailPeer": peer,
                "mailFrom": mailfrom,
                "mailTo": rcpttos,
                "headers": headers.as_string(True),
                "data": data.decode('utf8').replace("'", '"'),
                "kwargs": kwargs
            }

            res = Mongo.insert(msg)
            if res is not None:
                return True
            else:
                return False
        except Exception as err:
            print(err)

    @staticmethod
    def toJson(data):
        return json.dumps(data)
