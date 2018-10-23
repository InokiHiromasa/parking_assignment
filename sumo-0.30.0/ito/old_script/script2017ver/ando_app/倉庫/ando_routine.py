# _*_ coding: utf=8 -*-
from __future__ import absolute_import
from __future__ import print_function

from domain.model.routine import Routine

class ExtendedRoutine(Routine):
    def __init__(self, lag=0):
        self._lag = lag
        self._count = 0
        self._done = False

    def accept(self):
        if not self._done and self._count < self._lag:
            self._count = self._count + 1
            return False
        else:
            self._done = True
            return True
