#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import atexit
import pwd
import grp
import signal
import threading
import logging.handlers
import lmtp
from server import Server
from redisconfig import RedisConfig


DEBUG = True
# DEBUG = False

runUser = "cf"
runGrp = "cf"


if DEBUG:
    lockFileDir = '/tmp/lmtp-server'
else:
    lockFileDir = '/var/run/lmtp-server'

lockFileName = lockFileDir + '/server.pid'

cadmUid = pwd.getpwnam(runUser).pw_uid
cadmHome = pwd.getpwnam(runUser).pw_dir
cadmGid = grp.getgrnam(runGrp).gr_gid

syslog = logging.getLogger('webservice.server')
syslog.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address='/dev/log')
formatter = logging.Formatter('%(name)s: %(levelname)s %(message)s')
handler.setFormatter(formatter)
syslog.addHandler(handler)

RedisConfig.setRedisServer("172.17.0.2", 6379)


def delpid():
    try:
        os.remove(lockFileName)
    except OSError as err:
        syslog.info('someone already deleted ' + lockFileName + ": " + err.strerror)


def sigterm_handler(signum, frame):
    if Server.getServer() is not None:
        Server.getServer().close()
    if Server.getThreadLock() is not None:
        Server.getThreadLock().release()

    syslog.info('webservice.server shutdown')
    sys.exit()


def sigint_handler(signum, frame):
    if Server.getServer() is not None:
        Server.getServer().close()

    syslog.info('webservice.server shutdown')
    sys.exit()


def initial_program_setup_user():
    global syslog
    syslog.info('webservice.server startup')


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
    syslog.info('webservice.server reload')


def do_main_program():
    Server.setThreadLock(threading.Lock())
    Server.setServer(lmtp.runServer())


def do_main_daemon():
    # see http://www.jejik.com/files/examples/daemon3x.py
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
            syslog.info("first fork daemon")
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
            syslog.info("second fork daemon")
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
