import sys
sys.path.insert(0, "../src")

from pymongo import MongoClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import Config


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

    @staticmethod
    def sendMail(u):
        fromaddr = "source@example.org"
        toaddr = "target@example.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Python email"
        msg['X-Original-To'] = u

        bodyPlain = "Python test mail"
        bodyHtml = "<html><body>Python html mail</body></html>"
        msg.attach(MIMEText(bodyPlain, 'plain'))
        msg.attach(MIMEText(bodyHtml, 'html'))

        server = smtplib.SMTP(Config.getBind(), Config.getPort())
        server.ehlo()
        text = msg.as_string()

        server.sendmail(fromaddr, toaddr, text)
