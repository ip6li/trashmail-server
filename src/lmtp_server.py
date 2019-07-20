from aiosmtpd.lmtp import LMTP as Server, syntax


class LMTPServer(Server):
    @syntax('PING [ignored]')
    async def smtp_PING(self, arg):
        await self.push('259 Pong')
