from smtpd import SMTPChannel, SMTPServer
import asyncore
from threading import Thread
from server import Server
from storage import Storage


class LMTPChannel(SMTPChannel):
    # LMTP "LHLO" command is routed to the SMTP/ESMTP command
    def smtp_LHLO(self, arg):
        self.smtp_HELO(arg)


class LMTPServer(SMTPServer):
    def __init__(self, localaddr, remoteaddr):
        SMTPServer.__init__(self, localaddr, remoteaddr)

    def process_message_thread(self, peer, mailfrom, rcpttos, data, **kwargs):
        #Storage.printMsg(peer, mailfrom, rcpttos, data, **kwargs)
        Storage.storeMsg(peer, mailfrom, rcpttos, data, **kwargs)
        return

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        t = Thread(target=self.process_message_thread, args=(peer, mailfrom, rcpttos, data,))
        t.start()


    def handle_accept(self):
        conn, addr = self.accept()
        channel = LMTPChannel(self, conn, addr)
        Server.setChannel(channel)


def runServer():
    lmtpServer = LMTPServer(('localhost', 10025), None)
    asyncore.loop()

    return lmtpServer
