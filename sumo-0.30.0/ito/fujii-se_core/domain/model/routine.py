# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from random import random

class Routine(object):
    def __init__(self):
        self.acceptable_range = 100
        
    def accept(self):
        return random()*100 <= self.acceptable_range