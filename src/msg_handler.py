import signal
from logger import Logger
from storage import Storage


def handler(signum, frame):
    raise OSError("function timeout (" + str(signum) + "): " + str(frame))


class MsgHandler:

    def __init__(self):
        # Register the signal function handler
        signal.signal(signal.SIGALRM, handler)
        self.__timeout_sec = 10
        self.__log = Logger(__name__)

    async def handle_DATA(self, eml):
        try:
            # Some shit may happen on storing message,
            # e.g. half broken MongoDB or connections
            # This solution will definitely return
            signal.alarm(self.__timeout_sec)
            self.store_msg(eml)
            signal.alarm(0)
            return '250 OK'
        except OSError as oserr:
            self.__log.crit("MsgHandler::handle_DATA: Timeout on: " + str(oserr))
            return '400 Could not process your message ' + str(oserr)
        except Exception as err:
            self.__log.warn("MsgHandler::handle_DATA: Failed to store message: " + str(err))
            return '400 Could not process your message ' + str(err)

    def store_msg(self, eml):
        self.__log.debug("MsgHandler::store_msg begin store message")
        storage = Storage()
        storage.store_msg(eml.peer, eml.mail_from, eml.rcpt_tos, eml.content)
        self.__log.debug("MsgHandler::store_msg end store message")
