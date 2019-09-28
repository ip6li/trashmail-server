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

    def __init__(self):
        self.__log = Logger(__name__)

    def extract_rfc822(self, src):
        return parseaddr(src)[1]

    def __decode_headers(self, headers_in):
        try:
            return headers_in.as_string(True)
        except Exception as err:
            self.__log.crit("Storage::__decode_headers: " + str(err))

    def __decode_msg(self, data_in):
        try:
            return data_in.decode('utf8').replace("'", '"')
        except Exception as err:
            self.__log.crit("Storage::__decode_msg: " + str(err))

    def store_msg(self, peer, mailfrom, rcpttos, data):
        for rcpt in rcpttos:
            rcpt = rcpt.lower()
            self.store_msg_to_user(peer, mailfrom, rcpt, data)

    def store_msg_to_user(self, peer, mailfrom, rcpt, data):
        headers = MailParser.parseMail(data)
        timestamp = int(time.time())
        try:
            self.__log.debug("begin parsing message")
            msg = {
                "timestamp": timestamp,
                "mailPeer": peer,
                "mailFrom": mailfrom,
                "mailTo": rcpt,
                "headers": self.__decode_headers(headers),
                "data": self.__decode_msg(data),
            }
            self.__log.debug("end parsing message")
        except Exception as err:
            self.__log.crit("Storage::store_msg: Cannot encode message to JSON object: " + str(err))
            raise err
        try:
            self.__log.debug("begin store message")
            client = Mongo()
            post_id = client.insert(msg)
            self.__log.info("Storage::store_msg: Saved message with post_id "+str(post_id))
            self.__log.debug("end store message")
            return True
        except Exception as err:
            self.__log.warn("Storage::store_msg: Cannot write message to database: " + str(err))
            raise err

    def to_json(self, data):
        return json.dumps(data)
