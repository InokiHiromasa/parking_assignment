#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import subprocess

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    from sumolib import checkBinary
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

PORT = 8873
PARK_SERVER_PORT = 400
parking = {}

def run():
    traci.init(PORT)
    step = 0

    while step < 1500:
        traci.simulationStep()

        for vehID in traci.vehicle.getIDList():
            if not (vehID in parking.keys()) and (traci.vehicle.getRoadID(vehID) == 'in'):
                reserveSlot(vehID)

            if (vehID in parking.keys()) and (traci.vehicle.getRoadID(vehID) == 'out'):
                releaseSlot(vehID)

            if traci.vehicle.isStopped(vehID):
                traci.vehicle.changeTarget(vehID, 'out')

        step += 1

    traci.close()


import argparse
def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nogui', action='store_true', default=False, help='run the commandline version of sumo')
    options = parser.parse_args()
    return options


import socket
from contextlib import closing
import random

def reserveSlot(vehID):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
        sock.connect( ('127.0.0.1', 4000) )
        sock.send(b'rsrv')
        slot = sock.recv(4096)

        if slot == 'full':
            return
        else:
            parking[vehID] = slot
            traci.vehicle.changeTarget(vehID, slot)
            traci.vehicle.setStop(vehID, slot, pos=7.0, duration=random.randint(150000, 300000))
            
    return

def releaseSlot(vehID):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with closing(sock):
        sock.connect( ('127.0.0.1', 4000) )
        slot = parking[vehID]
        sock.send(slot)
        del parking[vehID]



if __name__ == '__main__':
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    sumoProcess = subprocess.Popen([sumoBinary, '-c', '../data/parking.sumocfg', '--tripinfo-output', '../output/tripinfo.xml', '--remote-port', str(PORT)], stdout=sys.stdout, stderr=sys.stderr)

    run()
    sumoProcess.wait()
    
