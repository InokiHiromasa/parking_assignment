# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from infrastructure.traci import *

def api_departed_list():
    return traci.simulation.getDepartedIDList()

def api_arrived_list():
    return traci.simulation.getArrivedIDList()

def api_simulation_step():
    return traci.simulationStep()

def api_get_position(vehID):
    return traci.vehicle.getPosition(vehID)

def api_get_destination(vehID):
    return traci.vehicle.getRoute(vehID)[-1]

def api_get_origin(vehID):
    return traci.vehicle.getRoute(vehID)[0]

def api_get_speed(vehID):
    return traci.vehicle.getSpeed(vehID)

def api_set_color(vehID, color):
    traci.vehicle.setColor(vehID, color)

def api_get_road(vehID):
    return traci.vehicle.getRoadID(vehID)

def api_change_destination(vehID, destination):
    traci.vehicle.changeTarget(vehID, destination)

