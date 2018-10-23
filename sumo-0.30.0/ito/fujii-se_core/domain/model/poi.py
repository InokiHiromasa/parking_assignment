# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

class POI(object):

    def __init__(self, name, entrance, exit, capacity):
        self._name = name
        self._entrance = entrance
        self._exit = exit
        self._capacity = capacity
        self._number = 0
        ## temp code
        self.repos = []

    def name(self):
        return self._name

    def entrance(self):
        return self._entrance

    def exit(self):
        return self._exit

    def enter(self, step, duration, object, number = 1):
        if self.repos:
            vehs = map(lambda x: x.object, self.repos)
            if not object in vehs:
                if number <= self.allowed_number():
                    self._number += number
                    self.repos.append(StayInfo(step, duration, object))
#                    print(self.information())
#                    print(self.repos)
                else:
#                    print("%s's capacity is over." % self._name)
                    return False
        else:
            self._number += number
            self.repos.append(StayInfo(step, duration, object))
        return True

    def leave(self, step):
        vehs = filter(lambda x: x.depart_step == step, self.repos)
        self._number -= len(vehs)
        for v in vehs:
            self.repos.remove(v)

    def check_leave(self, step):
        if self.repos:
            v = map(lambda x: x.depart_step, self.repos)
            if v.count(step):
                return True
        else:
            return False


    def allowed_number(self):
        return self._capacity - self._number

    def information(self):
        proportion = float(self._number)/self._capacity * 100
        return "name:%s max_capacity:%d number:%d proportion:%.2f"%( self._name, self._capacity, self._number, proportion)

class StayInfo(object):
    def __init__(self, step, duration, object):
        self.arrive_step = step
        self.depart_step = step + duration
        self.object = object

if __name__ == "__main__":
    pass