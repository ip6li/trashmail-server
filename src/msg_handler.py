from logger import Logger
from storage import Storage


class MsgHandler:
    async def handle_DATA(self, server, session, envelope):
        try:
            Logger.debug("begin store message")
            storage = Storage()
            storage.store_msg(session.peer, envelope.mail_from, envelope.rcpt_tos, envelope.content)
            Logger.debug("end store message")
        except Exception as err:
            return '500 Could not process your message ' + str(err)
        return '250 OK'
