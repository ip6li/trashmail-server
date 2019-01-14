import sys
sys.path.insert(0, "../src")

from pymongo import MongoClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import Config
import time
from datetime import date


class Testlib:

    @staticmethod
    def getPosts():
        client = MongoClient(Config.getMongoURL())
        db = client[Config.getDB()]
        return db.posts

    @staticmethod
    def list(fromtime):
        posts = Testlib.getPosts()
        query = {"timestamp": {"$lt": fromtime}}
        for post in posts.find(query):
            print(post)

    def sendMail(self, to, cc, bcc):
        fromaddr = "source@example.org"
        msg = MIMEMultipart('alternative')
        msg['From'] = fromaddr
        smtp_to = None
        if to is not None:
            print ("type: ", type(to))
            if type(to) is list:
                s = ",".join(to)
            else:
                s = to
            msg['To'] = s
            print("msg{to]: " + msg['To'])
            smtp_to = to
        if cc is not None:
            msg['CC'] = cc
            if smtp_to is None:
                smtp_to = cc
        if bcc is not None and smtp_to is None:
            msg['To'] = "undisclosed recipients"
            smtp_to = bcc

        if to is None and cc is None and bcc is None:
            print("no recipients set, aborting")
            sys.exit(1)

        print(smtp_to)

        msg['Date'] = time.asctime( time.localtime(time.time()))
        msg['Subject'] = "Python email"

        bodyPlain = "Python test mail"
        bodyHtml = "<html><body>Python html mail</body></html>"
        msg.attach(MIMEText(bodyPlain, 'plain'))
        msg.attach(MIMEText(bodyHtml, 'html'))

        server = smtplib.SMTP(Config.getBind(), Config.getPort())
        server.ehlo()
        text = msg.as_string()

        server.sendmail(fromaddr, smtp_to, text)

        server.close()
        
