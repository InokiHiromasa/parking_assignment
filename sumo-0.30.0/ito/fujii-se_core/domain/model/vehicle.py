# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from domain.shared.entity import Entity
from domain.model.vehicleinformation import VehicleInformation
from infrastructure.sumoapi import (api_get_position, api_get_destination, api_get_speed, api_set_color, api_get_road, api_change_destination, api_get_origin)


class Vehicle(Entity):

    def __init__(self, id):
        self._id = id
        self._discarded = False
        self._color = False
        self._information = VehicleInformation()

    def id(self):
		return self._id

    def update_information(self):
        self._information.origin = api_get_origin(self.id())
        self._information.position = api_get_position(self.id())
        self._information.road = api_get_road(self.id())
        self._information.destination = api_get_destination(self.id())
        self._information.speed = api_get_speed(self.id())

### デバッグ用色付け
        if self._information.destination == "PoI":
            if not self._color:
                self.change_color((60, 60, 255, 0))
                self._color = True
        elif self._information.destination[0] == "p":
            if not self._color:
                self.change_color((255, 60, 60, 0))
                self.color = True 
### デバッグ用色付け

        return self._information


    def change_destination(self, destination):
        ## check destination edge in this sim
        api_change_destination(self.id(), destination)

    def discarded(self):
        return self._discarded
        
    def change_color(self, color):
         api_set_color(self.id(), color)


if __name__ == "__main__":
    pass
