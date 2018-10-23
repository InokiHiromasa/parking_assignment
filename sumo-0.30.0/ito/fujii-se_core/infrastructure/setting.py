# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import json
from domain.model.poi import POI

def poi_setting(sim_id):
    with open("./utility/poi.json", "r") as file:
        ret = []
        data = json.load(file)
        for poi in data[sim_id].keys():
            entrance = data[sim_id][poi]["entrance"]
            exit = data[sim_id][poi]["exit"]
            capacity = data[sim_id][poi]["capacity"]
            frequency = data[sim_id][poi]["frequency"]
            port = data[sim_id][poi]["provide_info_port"]
            # temp Impl
            ret.append({"poi":POI(poi, entrance, exit, capacity), "freq": frequency, "port": port})
        return ret

if __name__ == "__main__":
    pass
