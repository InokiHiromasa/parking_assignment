# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals
from abc import ABCMeta, abstractmethod

class Repository(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def store(self, vehicle):
        raise NotImplementedError

    @abstractmethod
    def resolve_by_id(self, id):
        raise NotImplementedError