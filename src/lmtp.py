from smtpd import SMTPChannel, SMTPServer
import asyncore
import sys
from threading import Thread
from server import Server
from storage import Storage
from config import Config
from logger import Logger


class LMTPChannel(SMTPChannel):
    # LMTP "LHLO" command is routed to the SMTP/ESMTP command
    def smtp_LHLO(self, arg):
        self.smtp_HELO(arg)


class LMTPServer(SMTPServer):
    def __init__(self, localaddr, remoteaddr):
        try:
            SMTPServer.__init__(self, localaddr, remoteaddr)
        except Exception as err:
            Logger.crit("Cannot init LMTP server: " + str(err))
            sys.exit(1)

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        Logger.debug("processing message")
        Storage.storeMsg(peer, mailfrom, rcpttos, data, **kwargs)
        return

    def process_message_(self, peer, mailfrom, rcpttos, data, **kwargs):
        try:
            t = Thread(
                target=self.process_message,
                args=(peer, mailfrom, rcpttos, data,)
            )
            t.start()
        except Exception as err:
            Logger.warn("Cannot start thread in process_message: " + str(err))

    def handle_accept(self):
        conn, addr = self.accept()
        channel = LMTPChannel(self, conn, addr)
        Server.setChannel(channel)


def runServer():
    try:
        lmtpServer = LMTPServer((Config.getBind(), Config.getPort()), None)
        asyncore.loop()
    except Exception as err:
        Logger.crit("Cannot start LMTP server: " + str(err))
        sys.exit(1)

    return lmtpServer
