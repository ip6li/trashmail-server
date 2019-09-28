#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import asyncio
from logger import Logger
from eml import Eml
from msg_handler import MsgHandler


def usage():
    print("usage: postfix-plugin.py ${client_address} ${client_hostname} ${sender} ${recipient} ...\n")


if len(sys.argv) < 5:
    usage()
    exit(1)


eml = Eml()
eml.peer = sys.argv[1]
eml.hostname = sys.argv[2]
eml.mail_from = sys.argv[3]

eml.rcpt_tos = []
rcpt_count = 4
while rcpt_count < len(sys.argv):
    eml.rcpt_tos.append(sys.argv[rcpt_count])
    rcpt_count = rcpt_count + 1

log = Logger(__name__)
eml.content = bytes("".join(sys.stdin.readlines()), "utf-8")

msg_handler = MsgHandler()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(msg_handler.handle_DATA(eml))
