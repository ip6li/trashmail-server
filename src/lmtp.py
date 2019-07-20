import sys
from config import Config
from logger import Logger
import time
from msg_handler import MsgHandler
from lmtp_controller import LMTPController
from smtplib import LMTP


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
        wait_time = 60
        while True:
            Logger.debug("wait alive for " + str(wait_time) + "s")
            time.sleep(wait_time)
            with LMTP(host="127.0.0.1", port=10025) as smtp:
                try:
                    smtp.noop()
                    Logger.debug("alive")
                except Exception as err:
                    Logger.crit("LMTPServerRunner::check_lmtp_server: Server is dead" + str(err))
                    sys.exit(1)
