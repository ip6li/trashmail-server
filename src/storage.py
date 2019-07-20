import time
import json
from storage_mongodb import Mongo
from parser import MailParser
from email.utils import parseaddr
from logger import Logger


class Storage:

    @staticmethod
    def print_msg(peer, mailfrom, rcpttos, data):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        print('Message               :', data)
        return

    def extract_rfc822(self, src):
        return parseaddr(src)[1]

    def __decode_headers(self, headers_in):
        try:
            return headers_in.as_string(True)
        except Exception as err:
            Logger.crit("Storage::__decode_headers: " + str(err))

    def __decode_msg(self, data_in):
        try:
            return data_in.decode('utf8').replace("'", '"')
        except Exception as err:
            Logger.crit("Storage::__decode_msg: " + str(err))

    def store_msg(self, peer, mailfrom, rcpttos, data):
        headers = MailParser.parseMail(data)
        lower_rcpt_tos = []
        for rcpt in rcpttos:
            rcpt = rcpt.lower()
            lower_rcpt_tos.append(rcpt)

        timestamp = int(time.time())
        try:
            Logger.debug("begin parsing message")
            msg = {
                "timestamp": timestamp,
                "mailPeer": peer,
                "mailFrom": mailfrom,
                "mailTo": lower_rcpt_tos,
                "headers": self.__decode_headers(headers),
                "data": self.__decode_msg(data),
            }
            Logger.debug("end parsing message")
        except Exception as err:
            Logger.crit("Storage::store_msg: Cannot encode message to JSON object: " + str(err))
            raise err
        try:
            Logger.debug("begin store message")
            client = Mongo()
            post_id = client.insert(msg)
            Logger.debug("Storage::store_msg: Saved message with post_id "+str(post_id))
            Logger.debug("end store message")
            return True
        except Exception as err:
            Logger.warn("Storage::store_msg: Cannot write message to database: " + str(err))
            raise err

    def to_json(self, data):
        return json.dumps(data)

