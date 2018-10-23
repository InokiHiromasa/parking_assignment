# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from domain.shared.repository import Repository
from domain.model.sim import Sim

import uuid

class SimRepository(Repository):
    
    def __init__(self):
        self._sims = {}
    
    def store(self, sim):
        if not isinstance(sim, Sim):
            raise TypeError
        self._sims[sim.id()] = sim
        
    def resolve_by_id(self, id):
        return self._sims[id]

    def find_all(self):
        return self._sims.values()

    def find_all_ids(self):
        return self._sims.keys()

if __name__ == "__main__":
    pass
    simRepository = SimRepository()
    simRepository.store(Sim("sim", 8873))
    print(simRepository._sims)

