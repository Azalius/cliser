#!/usr/bin/env python3

import socket
import time

PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

def get_time_wait():
    """ Get a random time, the max time that the request can take """
    while True:
        aRet = np.random.normal(0.01, 0.008)
        if aRet>0.0: #we only want positive value
            return aRet


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('', PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                toSend = bytes(str(2*int(data)), 'ascii')

                conn.sendall(toSend)
