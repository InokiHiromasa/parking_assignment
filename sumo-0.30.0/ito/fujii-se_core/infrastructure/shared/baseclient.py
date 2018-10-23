# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import socket
from contextlib import closing

class BaseClient(object):
    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        self._cmd = ""
        self._res = ""

    def _op_app(self, cmd):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with closing(sock):
            sock.connect( (self._addr, self._port) )
            sock.send( str(cmd) )
            self._res = sock.recv(1024)

    def send_information(self, info):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with closing(sock):
            sock.connect( (self._addr, self._port) )
            sock.send( str(info) )
            #self._res = sock.recv(1024)

    def interpreter(self):
        pass

    def event_handler(self):
        pass

    def get_cmd(self):
        return self._cmd

    def get_result(self):
        return self._res

    def run(self):
        self._op_app(self._cmd)
        self.interpreter()
