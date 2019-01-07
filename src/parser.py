from email.parser import BytesParser
from email.policy import default


class MailParser:

    @staticmethod
    def parseMail(body):

        return BytesParser(policy=default).parsebytes(body)
