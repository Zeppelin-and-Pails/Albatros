#!/usr/bin/env python
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
from api import interface
from daemon import daemon
from flask import Flask, request, jsonify, redirect

class AlbatrosDaemon(daemon.Daemon):
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
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
