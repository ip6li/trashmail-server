import sys
import time
from custom_cb import retry_auto_reconnect
from logger import Logger
from smtplib import LMTP
from config import Config
from pymongo import MongoClient


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
        with LMTP(host=Config.getBind(), port=Config.getPort()) as lmtp:
            try:
                lmtp.noop()
                Logger.debug("alive")
            except Exception as err:
                Logger.crit("LMTPServerRunner::check_lmtp_server: Server is dead" + str(err))
                sys.exit(1)

    @staticmethod
    @retry_auto_reconnect
    def __test_mongodb():
        Logger.debug("Test MongoDB")

        client = MongoClient(host=Config.getMongoURL(), socketTimeoutMS=Config.getTimeout())
        client.server_info()
        client.close()
