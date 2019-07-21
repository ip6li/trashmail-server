import logging.handlers
from config import Config


class Logger:

    __appname = "lmtp-server"

    @staticmethod
    def init():
        syslog = logging.getLogger(Logger.__appname)
        syslog.setLevel(Config.getLoglevel())
        logging.basicConfig(
            format='%(name)s: %(levelname)s %(message)s',
            level=Config.getLoglevel()
        )

    @staticmethod
    def debug(msg):
        logging.debug(msg)

    @staticmethod
    def info(msg):
        logging.info(msg)

    @staticmethod
    def warn(msg):
        logging.warning(msg)

    @staticmethod
    def crit(msg):
        logging.critical(msg)

    @staticmethod
    def getAppName():
        return Logger.__appname
