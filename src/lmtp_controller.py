from aiosmtpd.controller import Controller
from lmtp_server import LMTPServer


class LMTPController(Controller):
    def factory(self):
        return LMTPServer(self.handler)
