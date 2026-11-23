#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Albatros API

REST interface for Albatros

@category   Utility
@version    $ID: 1.1.1, 2016-05-05 17:00:00 CST $;
@author     KMR
@licence    GNU GPL v.3
"""

import os, yaml
import time, sys
import atexit, signal
from api import interface
from flask import Flask, request, jsonify, redirect


class Daemon:
    """
    Minimal UNIX double-fork daemon with a pidfile and start/stop/restart.
    Python 3 replacement for the Py2-only "daemon.Daemon" recipe (Sander Marechal)
    this script previously imported.
    """
    def __init__(self, pidfile):
        self.pidfile = pidfile

    def daemonize(self):
        if os.fork() > 0:
            sys.exit(0)
        os.chdir('/')
        os.setsid()
        os.umask(0)
        if os.fork() > 0:
            sys.exit(0)

        sys.stdout.flush()
        sys.stderr.flush()
        with open(os.devnull, 'rb') as si, open(os.devnull, 'ab') as so:
            os.dup2(si.fileno(), sys.stdin.fileno())
            os.dup2(so.fileno(), sys.stdout.fileno())
            os.dup2(so.fileno(), sys.stderr.fileno())

        atexit.register(self.delpid)
        with open(self.pidfile, 'w') as f:
            f.write("{}\n".format(os.getpid()))

    def delpid(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)

    def getpid(self):
        try:
            with open(self.pidfile) as f:
                return int(f.read().strip())
        except (IOError, ValueError):
            return None

    def start(self):
        if self.getpid():
            sys.stderr.write("pidfile {} already exists. Daemon already running?\n".format(self.pidfile))
            sys.exit(1)
        self.daemonize()
        self.run()

    def stop(self):
        pid = self.getpid()
        if not pid:
            sys.stderr.write("pidfile {} does not exist. Daemon not running?\n".format(self.pidfile))
            return
        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except ProcessLookupError:
            self.delpid()

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        raise NotImplementedError


class AlbatrosDaemon(Daemon):
    def __init__(self, pidfile='/tmp/albatros.pid'):
        super(AlbatrosDaemon, self).__init__(pidfile)

    def run(self):
        fa = FlaskApp()
        fa.run()

class FlaskApp:
    DIR = os.path.dirname(os.path.realpath(__file__))
    conf = yaml.safe_load(open("{}/flask.cfg".format(DIR)))
    app = Flask(__name__)

    address_interface = interface.interface()
    def run(self):
        @self.app.route('search')
        def search():
            return address_interface.search()

        @self.app.route('get')
        def get():
            return address_interface.get()

        self.app.run(host=self.conf['HOST'], port=self.conf['PORT'])

if __name__ == "__main__":
    daemon = AlbatrosDaemon()

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
