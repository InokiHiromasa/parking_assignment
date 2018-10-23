# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

class Statistics(object):

    class Counter(object):
        pass

    class Log(object):
        pass

    def __init__(self):
        self.counters = {}
    
    def count(self, target):
        if not target in self.counters.keys():
            self.counters[target] = 0
        self.counters[target] += 1
    
    def add(self, id):
        pass

    def params(self):
        return self.__dict__

    def show(self):
        print("")
        print("Statistic Information:")
        print(self.params())
        print("")
    
    def log(self):
        pass
        
statistics = Statistics()