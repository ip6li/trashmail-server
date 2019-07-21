import sys
import time
from logger import Logger
from smtplib import LMTP
from config import Config


class Check:

    @staticmethod
    def run_checks():
        wait_time = 60
        Logger.debug("wait alive for " + str(wait_time) + "s")
        while True:
            time.sleep(wait_time)
            Check.__check_lmtp_server()
            Check.__test_mongodb()

    @staticmethod
    def __check_lmtp_server():
        with LMTP(host="127.0.0.1", port=10025) as lmtp:
            try:
                lmtp.noop()
                Logger.debug("alive")
            except Exception as err:
                Logger.crit("LMTPServerRunner::check_lmtp_server: Server is dead" + str(err))
                sys.exit(1)

    @staticmethod
    def __test_mongodb():
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure

        Logger.debug("Test MongoDB")
        try:
            client = MongoClient(host=Config.getMongoURL(), socketTimeoutMS=Config.getTimeout())
            client.server_info()
            client.close()
        except ConnectionFailure as err:
            Logger.crit("MongoDB is not available: " + str(err))
