#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../src")
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from pymongo import MongoClient
from config import Config


class Test1:

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

        server = smtplib.SMTP('localhost', 10025)
        server.ehlo()
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)

    @staticmethod
    def readMail(u):
        client = MongoClient(Config.getMongoURL())
        db = client[Config.getDB()]
        posts = db.posts

        for post in posts.find({"X-Original-To": "joe.test.0@example.com"}):
            print(post)

    @staticmethod
    def genMails(count):
        for i in range(count):
            u = "joe.test."+str(i)+"@example.com"
            Test1.sendMail(u)


user="joe.test@example.com"
Test1.genMails(1000)
Test1.readMail(user)
