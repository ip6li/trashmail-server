import time
import json
from storage_mongodb import Mongo
from parser import MailParser
from email.utils import parseaddr
from logger import Logger


class Storage:

    @staticmethod
    def print_msg(peer, mailfrom, rcpttos, data, **kwargs):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        print('Message               :', data)
        print("kwargs                :", kwargs)
        return

    def extract_rfc822(self, src):
        return parseaddr(src)[1]

    def store_msg(self, peer, mailfrom, rcpttos, data, **kwargs):
        headers = MailParser.parseMail(data)
        lower_rcpt_tos = []
        for rcpt in rcpttos:
            rcpt = rcpt.lower()
            lower_rcpt_tos.append(rcpt)

        timestamp = int(time.time())
        try:
            msg = {
                "timestamp": timestamp,
                "mailPeer": peer,
                "mailFrom": mailfrom,
                "mailTo": lower_rcpt_tos,
                "headers": headers.as_string(True),
                "data": data.decode('utf8').replace("'", '"'),
                "kwargs": kwargs
            }
        except Exception as err:
            Logger.crit("Cannot encode message to JSON object: " + str(err))
            raise err
        try:
            client = Mongo()
            post_id = client.insert(msg)
            Logger.debug("Saved message with post_id "+str(post_id))
            return True
        except Exception as err:
            Logger.warn("Cannot write message to database: " + str(err))
            raise err

    def to_json(self, data):
        return json.dumps(data)

