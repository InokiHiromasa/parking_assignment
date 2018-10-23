# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from domain.shared.repository import Repository
from domain.model.poi import POI

class POIRepository(Repository):

    def __init__(self):
        self._pois = {}

    def store(self, poi):
        if not isinstance(poi, POI):
            raise TypeError
        self._pois[poi.name()] = poi

    def resolve_by_id(self, id):
        return self._pois[id]

    def find_all(self):
        return self._pois.values()

    def find_all_ids(self):
        return self._pois.keys()

if __name__ == "__main__":
    pass
