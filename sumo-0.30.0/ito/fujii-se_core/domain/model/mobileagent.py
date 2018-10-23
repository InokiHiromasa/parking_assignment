# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from domain.shared.entity import Entity
from domain.model.routine import Routine

from infrastructure.statistics import *

class MobileAgent(Entity):

    def __init__(self, id, obj, apps):
        self._id = id
        self._routine = Routine()
        self._object = obj
        self._information = None
        self._discarded = False
        self._apps = apps

        self._used = False
        self._counted = False

    def id(self):
        return self.id

    def routine(self):
        return self._routine

    def object(self):
        return self._object

    def object_information(self):
        return self._information

    def get_information(self):
        self.check_discarded()
        if not self.discarded():
            self._information = self._object.update_information()

    def discarded(self):
        return self._discarded

    def check_discarded(self):
        if self._object.discarded():
            self._discarded = True

    def use_app(self):
        if not self.discarded():
            if self._apps:
                for app in self._apps:
                    if app.event_handler(self.object_information()) and not self._used:
                        ## Log
                        statistics.count("App")

                        app.run()
                        self._used = True

                        ## 操作
                        if self.routine().accept():
                            self._object.change_destination(app._res)
                        #self._object.change_destination(self.object_information().destination)

