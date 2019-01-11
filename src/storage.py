import time
import json
from storage_mongodb import Mongo
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
        lowerRcptTos = []
        for rcpt in rcpttos:
            rcpt = rcpt.lower()
            lowerRcptTos.append(rcpt)
        try:
            timestamp = int(time.time())
            msg = {
                "timestamp": timestamp,
                "mailPeer": peer,
                "mailFrom": mailfrom,
                "mailTo": lowerRcptTos,
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
