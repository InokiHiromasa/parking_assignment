# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from domain.shared.entity import Entity
from infrastructure.repository.vehiclerepository import VehicleRepository
from infrastructure.repository.poirepository import POIRepository
from infrastructure.sumoapi import (api_departed_list, api_arrived_list, api_simulation_step)

class Sim(Entity):

    def __init__(self, id, port):
        self._id = id
        self._port = port
        self.vehicle_repository = VehicleRepository()
        self.poi_repository = POIRepository()
        
    def id(self):
        return self._id
        
    def departed_list(self):
        return api_departed_list()
        
    def arrived_list(self):
        return api_arrived_list()
        
    def simulation_step(self):
        api_simulation_step()
