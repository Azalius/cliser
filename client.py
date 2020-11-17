#!/usr/bin/env python3

import socket
import time
import numpy as np
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=65432,
                    help='Wich port to connect to')
parser.add_argument('-ip', type=str, default='127.0.0.1',
                    help='The address of the server')
parser.add_argument('-ata', '--accept_time_avg', type=float, default=0.001,
                    help='The average timeframe where awnser are accepted')
parser.add_argument('-atv', '--accept_time_variation', type=float, default=0.0005,
                    help='The standard deviation of accepted timeframe')
parser.add_argument('-w', '--wait_time', type=float, default=0.1,
                    help='How much to wait between connections')

args = parser.parse_args()
current_milli_time = lambda: time.time()

def get_time_max():
    """ Get a random time, the max time that the request can take """
    while True:
        aRet = np.random.normal(args.accept_time_avg, args.accept_time_variation)
        if aRet>0.0: #we only want positive value
            return aRet

nb_try = 0
nb_ok = 0

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        nb_try += 1
        cur_time = current_milli_time()
        s.connect((args.ip, args.port))
        s.sendall(bytes(str(nb_try), 'ascii')) #we send a value to the server
        data = int(s.recv(1024).decode("ascii")) #& receive an awnser

        max_acceptable_time = get_time_max()
        done_time = current_milli_time() - cur_time
        if(done_time < max_acceptable_time):#we check wether or not the server was fast enough
            nb_ok += 1

    time.sleep(args.wait_time)
    prcent_ok = int((30*nb_ok)/nb_try)
    out_str = "#"*prcent_ok +" "*(30-prcent_ok) #we make a display of the value
    token = "V" if done_time < max_acceptable_time else "X"
    sys.stdout.write("\r["+out_str+"]"+str(nb_ok)+"/"+str(nb_try)+" "+token+" "+str(done_time*1000)+ " for max "+str(max_acceptable_time*1000))
    sys.stdout.flush()
