#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import atexit
import pwd
import grp
import signal
import threading
import lmtp
from config import Config
from server import Server
from logger import Logger


DEBUG = True
#DEBUG = False

runUser = Config.getRunUser()
runGrp = Config.getRunGrp()

lockFileDir = Config.getLockFileDir()
lockFileName = lockFileDir + '/server.pid'

cadmUid = pwd.getpwnam(runUser).pw_uid
cadmHome = pwd.getpwnam(runUser).pw_dir
cadmGid = grp.getgrnam(runGrp).gr_gid

Logger.init()


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

    Logger.info(Config.getAppName() + ' shutdown')
    sys.exit()


def initial_program_setup_user():
    Logger.info(Config.getAppName() + ' startup')


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
    except OSError as err:
        print("cannot mkdir " + lockFileName + " {0}\n)".format(err))

    signal.signal(signal.SIGTERM, sigterm_handler)
    signal.signal(signal.SIGINT, sigint_handler)


def reload():
    Logger.info('webservice.server reload')


def do_main_program():
    Server.setThreadLock(threading.Lock())
    Server.setServer(lmtp.runServer())


def do_main_daemon():
    try:
        with open(lockFileName, 'r') as pf:
            pid = int(pf.read().strip())
    except IOError:
        pid = None

    if pid:
        message = "pidfile {0} already exist. Daemon already running?\n"
        sys.stderr.write(message.format(lockFileName))
        sys.exit(1)

    try:
        pid = os.fork()
        if pid > 0:
            Logger.info("first fork daemon")
            # exit first parent
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('fork #1 failed: {0}\n'.format(err))
        sys.exit(1)

    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            Logger.info("second fork daemon")
            sys.exit(0)
    except OSError as err:
        sys.stderr.write('fork #2 failed: {0}\n'.format(err))
        sys.exit(1)

    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open(os.devnull, 'a+')
    se = open(os.devnull, 'a+')

    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

    atexit.register(delpid)

    pid = str(os.getpid())
    try:
        with open(lockFileName, 'w+') as f:
            f.write(pid + '\n')
    except:
        sys.stderr.write('cannot open pid file')
        sys.exit(1)

    do_main_program()


initial_program_setup_root()
initial_program_setup_user()

if (DEBUG):
    do_main_program()
else:
    do_main_daemon()
