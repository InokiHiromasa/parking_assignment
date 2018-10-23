# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from domain.model.poiagent import POIAgent

from infrastructure.repository.mobileagentrepository import MobileAgentRepository
from infrastructure.repository.poiagentrepository import POIAgentRepository
from infrastructure.repository.simrepository import SimRepository
from infrastructure.setting import poi_setting

import uuid

class Manager(object):

    def __init__(self):
        self.mobile_agent_repository = MobileAgentRepository()
        self.poi_agent_repository = POIAgentRepository()
        self.sim_repository = SimRepository()
        self._end_step = None

    def step_init(self):
        self._step = 0
    
    def step(self):
        self._step += 1

    def get_step(self):
        return self._step

    def end_step(self, end_time):
        self._end_step = end_time

    def check_end(self):
        if self._end_step:
            if self.get_step() >= self._end_step:
                return True

    def setting_poi(self):
        for sim_id in self.sim_repository.find_all_ids():
            sim = self.sim_repository.resolve_by_id(sim_id)
            for poi_info in poi_setting(sim_id):
                poi = poi_info["poi"]
                sim.poi_repository.store(poi)
                agent_id = uuid.uuid4().hex
                freq = poi_info["freq"]
                ports = poi_info["port"]
                self.poi_agent_repository.store(POIAgent(agent_id, poi, freq, ports))

    def setting_sim(self):
        pass

manager = Manager()

if __name__ == "__main__":
    pass
