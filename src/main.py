#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pwd
import grp
import signal
import threading
import lmtp
from config import Config
from server import Server
from logger import Logger


def delpid():
    try:
        os.remove(lockFileName)
    except OSError as err:
        Logger.info('someone already deleted ' + lockFileName + ": " + err.strerror)


def sigterm_handler(signum, frame):
    if Server.getServer() is not None:
        Server.getServer().close()
    if Server.getThreadLock() is not None:
        Server.getThreadLock().release()

    Logger.info('webservice.server shutdown')
    sys.exit()


def sigint_handler(signum, frame):
    if Server.getServer() is not None:
        Server.getServer().close()

    Logger.info(Logger.getAppName() + ' shutdown')
    sys.exit()


def initial_program_setup_user():
    Logger.info(Logger.getAppName() + ' startup')


def initial_program_setup_root():
    if cadmGid == 0:
        print("I am not willing to run in group root")
        sys.exit(1)
    if cadmUid == 0:
        print("I am not willing to run as root")
        sys.exit(1)

    try:
        os.mkdir(lockFileDir)
        os.chown(lockFileDir, cadmUid, cadmGid)
    except FileExistsError:
        Logger.info(lockFileDir + " already exists")
    except OSError as err:
        print("cannot mkdir " + lockFileDir + " {0}\n)".format(err))

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigint_handler)


def reload():
    Logger.info('webservice.server reload')


def do_main_program():
    Server.setThreadLock(threading.Lock())
    Server.setServer(lmtp.runServer())


runUser = Config.getRunUser()
runGrp = Config.getRunGrp()

lockFileDir = Config.getLockFileDir()
lockFileName = lockFileDir + '/server.pid'

if not os.path.isdir(lockFileDir):
    os.mkdir(lockFileDir)
pidFile = open(lockFileName, "w", encoding="utf-8")
pidFile.write(str(os.getpid()))
pidFile.close()

cadmUid = pwd.getpwnam(runUser).pw_uid
cadmHome = pwd.getpwnam(runUser).pw_dir
cadmGid = grp.getgrnam(runGrp).gr_gid

Logger.init()

initial_program_setup_root()
initial_program_setup_user()

do_main_program()
