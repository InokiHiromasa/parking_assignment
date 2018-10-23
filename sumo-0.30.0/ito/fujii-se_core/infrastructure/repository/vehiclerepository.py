# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from domain.shared.repository import Repository
from domain.model.vehicle import Vehicle

import uuid

class VehicleRepository(Repository):

    def __init__(self):
        self._vehicles = {}

    def store(self, vehicle):
        if not isinstance(vehicle, Vehicle):
            raise TypeError
        self._vehicles[vehicle.id()] = vehicle
        
    def restore(self, id):
        del self._vehicles[id]

    def resolve_by_id(self, id):
        return self._vehicles[id]

    def find_all(self):
        return self._vehicles.values()

    def find_all_ids(self):
        return self._vehicles.keys()

if __name__ == "__main__":
    pass

