#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
from _datetime import datetime
from logger import Logger


# Register an handler for the timeout
def handler(signum, frame):
    raise Exception("function timeout: " + str(frame))


# This function *may* run for an indetermined time...
def loop_forever():
    import time
    hang_for = 30
    while True:
        Logger.info("hangs for " + str(hang_for) + " sec")
        time.sleep(hang_for)


# Register the signal function handler
signal.signal(signal.SIGALRM, handler)

# Define a timeout for your function
timeout_sec = 10
signal.alarm(timeout_sec)

try:
    Logger.info("start: " + str(datetime.now()))
    loop_forever()
except Exception as err:
    Logger.warn(err)

Logger.info("end: " + str(datetime.now()))

# Cancel the timer if the function returned before timeout
# (ok, mine won't but yours maybe will :)
signal.alarm(0)
