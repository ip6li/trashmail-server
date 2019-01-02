#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import redis
import json


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
        r = redis.Redis(host="172.17.0.2", port=6379, db=0)
        res = json.loads(r.get(u))
        s = json.dumps(res, indent=4, sort_keys=True)
        print (s)

    @staticmethod
    def gen10Mails():
        for i in range(10):
            u = "joe.test."+str(i)+"@example.com"
            Test1.sendMail(u)


user="joe.test@example.com"
Test1.gen10Mails()
Test1.readMail(user)
