# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

class VehicleInformation(object):

    def __init__(self):
        self.origin = None
        self.destination = None
        self.route = []

    def params(self):
        return self.__dict__
