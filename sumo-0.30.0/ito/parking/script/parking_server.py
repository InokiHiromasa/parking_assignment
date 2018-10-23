#!/usr/bin/env python

from __future__ import print_function
import socket
import select

import random

slots = {'P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10', 'P11', 'P12'}
reserved_slots = set()

def main():
    host = '127.0.0.1'
    port = 4000
    backlog = 10
    bufsize = 4096
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    readfds = set([server_sock])
    try:
        server_sock.bind( (host, port) )
        server_sock.listen(backlog)

        while True:
            rready, wready, xready = select.select(readfds, [], [])
            for sock in rready:
                if sock is server_sock:
                    conn, address = server_sock.accept()
                    readfds.add(conn)
                else:
                    msg = sock.recv(bufsize)
                    if len(msg) == 0:
                        sock.close()
                        readfds.remove(sock)

                    elif msg == 'rsrv':
                        r_slot = reserveSlot()
                        print(reserved_slots)
                        sock.send(r_slot)
                    else:
                        releaseSlot(msg)
                        print(reserved_slots)
                        

    finally:
        for sock in readfds:
            sock.close()
    return

def reserveSlot():
    free_list = list( slots - reserved_slots )

    if len(free_list) < 1:
        return 'full'
    else:
        r_slot = random.choice(free_list)
        reserved_slots.add(r_slot)
        return r_slot

def releaseSlot(slot):
    reserved_slots.discard(slot)
    return


if __name__ == '__main__':
    main()
