from storage import Storage


class MsgHandler:
    async def handle_DATA(self, server, session, envelope):
        try:
            storage = Storage()
            storage.store_msg(session.peer, envelope.mail_from, envelope.rcpt_tos, envelope.content)
        except Exception as err:
            return '500 Could not process your message ' + str(err)
        return '250 OK'
