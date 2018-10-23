# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals
from abc import ABCMeta, abstractmethod

class Entity(object):
    
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def id(self):
		pass