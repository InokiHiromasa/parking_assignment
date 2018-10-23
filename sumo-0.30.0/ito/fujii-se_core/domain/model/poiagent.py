# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from domain.shared.entity import Entity

from infrastructure.statistics import *
from infrastructure.shared.baseclient import BaseClient

class POIAgent(Entity):

    def __init__(self, id, poi, freq, ports):
        self._id = id
        self._poi = poi
        self._information = None
        self._frequency = freq
        self._ports = ports
        self._provider = [BaseClient("", port) for port in self._ports]

    def id(self):
        return self.id

    def poi(self):
        return self._poi

    def poi_information(self):
        return self._information

    def get_information(self):
        self._information = self.poi().information()

    def provide_information(self, step):
        for e in self._provider:
            e.send_information("info %s step:%d" % (self.poi_information(), step))
        #return "info %s" % self.poi_information()

    def check(self, step):
        if step % self._frequency == 0:
            return True
