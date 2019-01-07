import logging.handlers


class Logger:

    __appname = "lmtp-server"

    @staticmethod
    def init():
        syslog = logging.getLogger(Logger.__appname)
        syslog.setLevel(logging.DEBUG)
        logging.basicConfig(format='%(name)s: %(levelname)s %(message)s', level=logging.DEBUG)

    @staticmethod
    def alt_init():
        syslog = logging.getLogger('webservice.server')
        syslog.setLevel(logging.DEBUG)
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        syslog.addHandler(handler)

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
