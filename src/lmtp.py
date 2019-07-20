import sys
from config import Config
from logger import Logger
import time
from msg_handler import MsgHandler
from lmtp_controller import LMTPController


class LMTPServerRunner:
    def __init__(self):
        try:
            Logger.info("firing up lmtp server")
            handler = MsgHandler()
            controller = LMTPController(handler, hostname=Config.getBind(), port=Config.getPort())
            # Run the event loop in a separate thread.
            controller.start()
            # Run forever
            self.check_lmtp_server()
            controller.stop()
        except Exception as err:
            Logger.crit("LMTPServerRunner::__init__Cannot init LMTP server: " + str(err))
            sys.exit(1)

    @staticmethod
    def check_lmtp_server():
        while True:
            print("alive")
            time.sleep(300)
            # should be improved by monitoring functions
