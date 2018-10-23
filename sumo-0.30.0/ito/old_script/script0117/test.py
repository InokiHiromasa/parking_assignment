#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import subprocess

# To use the library, the $SUMO_HOME/tools directory must be on the python load path.
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    from sumolib import checkBinary
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import json
import urllib2

jsonserver = "http://localhost:3000/"

def getTartgetGeo():
    lat = None
    lng = None
    try:
        url = jsonserver + 'points/3'
        r = urllib2.urlopen(url)
        item = json.loads(r.read())
        lat = item['lat']
        lng = item['lng']

    finally:
        r.close()
        return lat, lng


import traci
# the port used for communicating with a sumo instance
PORT = 8873

def run():
    """execute the TraCI control loop"""
    traci.init(PORT)
    step = 0

    vehID = "0.10"
    red = 0
    green = 0
    blue = 0

    # lat = 33.598421
    # lng = 130.221593
    # print('(lat, lng) = ', (lat, lng)  , '\033[K', file=sys.stderr)
    # (tx, ty) = traci.simulation.convertGeo(lng, lat, True)
    # print('(tx, ty) = ', (tx, ty), '\033[K')
    # print('Road : ', traci.simulation.convertRoad(tx, ty, False), '\033[K', file=sys.stderr)
    # print('Road : ', traci.simulation.convertRoad(lng, lat, True), '\033[K', file=sys.stderr)
    # print("*** *** *** *** *** ***", file=sys.stderr)

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        if vehID in traci.vehicle.getIDList():
            red = step % 128 + 128
            green = (step * 7) % 128 + 128
            blue = (step * 13) % 128 + 128 
#            traci.vehicle.setColor(vehID, (red, green, blue, 0))

            if traci.vehicle.getRoadID(vehID) == '84515125#3':
                traci.vehicle.setColor(vehID, (255, 0, 0, 0))
                t_lat, t_lng = getTartgetGeo()
                targetLane, _, _ = traci.simulation.convertRoad(t_lng, t_lat, True)
                traci.vehicle.changeTarget(vehID, targetLane)

#                traci.vehicle.changeTarget(vehID, '161947715#0')
#                traci.vehicle.setRouteID(vehID, "reroute01")

            distance = traci.vehicle.getDistance(vehID)
            speed = traci.vehicle.getSpeed(vehID) * 60.0 * 60.0 / 1000.0
#            print('Distance : {:7.2f}[m], Speed : {:5.2f}[km/h]  '.format(distance, speed), end='\r', file=sys.stderr)

            print('Distance : {:7.2f}[m], Speed : {:5.2f}[km/h]\033[K'.format(distance, speed), file=sys.stderr)
            print('LaneID : ', traci.vehicle.getRoadID(vehID), '\033[K', file=sys.stderr)
            (x, y) = traci.vehicle.getPosition(vehID)
            print('Road : ', traci.simulation.convertRoad(x,y), '\033[K', file=sys.stderr)
            print('Position : ', traci.simulation.convertGeo(x,y,False), '\033[K', file=sys.stderr)
#            print('Position : ', sumolib.net.convertXY2LonLat(traci.vehicle.getPosition(vehID)), '\033[K', file=sys.stderr)
            
            count = 0
            print('0   20  40  60  80  100 120', file=sys.stderr)
            print('+---+---+---+---+---+---+--', file=sys.stderr)
            print('\033[K', end="", file=sys.stderr)
            while count < speed / 5:
                print('#', end='', file=sys.stderr)
                count += 1
            print('', file=sys.stderr)

            print('\033[7A', end='', file=sys.stderr)
            sys.stderr.flush()

        step += 1

    print('\033[7B', file=sys.stderr)

    print('test:', traci.simulation.convertRoad(130.211299, 33.598048, True), '\033[K', file=sys.stderr)
    sys.stderr.flush()

    traci.close()

import argparse
def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--nogui', action='store_true', default=False, help='run the commandline version of sumo')
    options = parser.parse_args()
    return options


import subprocess

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line.
    # It will start sumo as a server, then connect and run.
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    sumoProcess = subprocess.Popen([sumoBinary, '-c', '../data/ito.sumocfg', '--tripinfo-output', '../output/tripinfo.xml', '--remote-port', str(PORT)], stdout=sys.stdout, stderr=sys.stderr)

    run()
    sumoProcess.wait()

    
