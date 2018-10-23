# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import socket
import select

import random

class BaseServer(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.backlog = 10
        self.bufsize = 4096

    def deal_msg(self, sock, msg, readfds):# 要求に対する動作をかく
        pass


    def run(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        readfds = set([server_sock])
        try:
            #server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_sock.bind( (self._host, self._port) )
            server_sock.listen(self.backlog)

            while True:
                rready, wready, xready = select.select(readfds, [], [])
                for sock in rready:
                    if sock is server_sock:
                        conn, address = server_sock.accept()
                        readfds.add(conn)
                    else:
                        msg = sock.recv(self.bufsize)
                        self.deal_msg(sock, msg, readfds)

        finally:
            for sock in readfds:
                sock.close()
        return
