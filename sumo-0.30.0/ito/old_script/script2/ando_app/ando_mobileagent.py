# _*_ coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from domain.model.mobileagent import MobileAgent


CENTER_PARKING = '84515126'
ROTARY = '161947715#0'
WEST_PARKING = '-223785629'

class ExtendedMobileAgent(MobileAgent):

    def __init__(self, id, obj, apps, routine):
        MobileAgent.__init__(self, id, obj, apps)
        self._routine = routine
        self._newDest = None

    def use_app(self):
        if not self.discarded():
            if self._apps:
                for app in self._apps:
                    app.vehcount(self.object_information())

                    if app.event_handler(self.object_information()):
                        app.run()
                        self._newDest = app._res
                        self._object.change_color((255,255,255,0))

            if self._newDest:
                if self._routine.accept():
                    self._object.change_destination(self._newDest)

                    # 行き先で色変え
                    if self._newDest == CENTER_PARKING:
                        self._object.change_color((255,255,0,0))
                    elif self._newDest == ROTARY:
                        self._object.change_color((0,255,0,0))
                    elif self._newDest == WEST_PARKING:
                        self._object.change_color((255,0,0,0))
                    else:
                        self._object.change_color((255,0,255,0))