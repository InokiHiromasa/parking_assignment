# _*_ coding: utf-8 -*-
from __future__ import print_function
from random import randint

import urllib2
import json

from infrastructure.traci import *

JSON_SERVER = 'http://localhost:3000/'

class AppInVeh():
    def __init__(self):
        self._res = None
        self._used = False

    def event_handler(self, info):
        if not self._used and info.road == '84515125#3':
            return True
        else:
            return False

    def run(self):
        try:
            id = randint(1, 3)
            url = JSON_SERVER + 'points/' + str(id)
            reader = urllib2.urlopen(url)
            item = json.loads(reader.read())
            lat = item['lat']
            lng = item['lng']
            # 反則技…
            self._res, _, _ = traci.simulation.convertRoad(lng, lat, True)
            print('res:', self._res)
            self._used = True

        finally:
            reader.close()