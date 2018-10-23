# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

from domain.shared.repository import Repository
from domain.model.mobileagent import MobileAgent

import uuid

class MobileAgentRepository(Repository):

    def __init__(self):
        self._agents = {}

    def store(self, agent):
        if not isinstance(agent, MobileAgent):
            raise TypeError
        self._agents[agent.id()] = agent

    def resolve_by_id(self, id):
        return self._agents[id]

    def find_all(self):
        return filter(lambda e: not e.discarded(), self._agents.values())

    def find_all_ids(self):
        return filter(lambda e: not e.discarded(), self._agents.keys())

if __name__ == "__main__":
    pass
