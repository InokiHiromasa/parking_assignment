#!/usr/bin/env python
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
import subprocess
import uuid

from random import randint

# To use support env 
if 'SIM_SUPPORT_ENV' in os.environ:
    sys.path.append(os.environ['SIM_SUPPORT_ENV'])

    from domain.model.sim import Sim
    from domain.model.vehicle import Vehicle
    from domain.model.mobileagent import MobileAgent
    from domain.model.manager import *
    from infrastructure.traci import *

    from ando_app.app_in_veh import AppInVeh

    from ando_app.ando_mobileagent import ExtendedMobileAgent
    from ando_app.ando_routine import ExtendedRoutine
    
else:
    sys.exit("please declare environment variable 'SIM_SUPPORT_ENV'.")

# def assign_apps(veh):
#     if veh.id() == '0.10':
#         veh.change_color((255,0,0,0))
#         print('assigned')
#         return [AppInVeh()]
#     else:
#         return None

# def assign_mobile_agent(veh):
#     if veh.id() == '0.10':
#         veh.change_color((255,0,0,0))        
#         agent_id = uuid.uuid4().hex
#         return ExtendedMobileAgent(agent_id, veh, [AppInVeh()], ExtendedRoutine(30))
#     else:
#         return None

def assign_mobile_agent(veh):
    lag = randint(10, 50)
    agent_id = uuid.uuid4().hex
    return ExtendedMobileAgent(agent_id, veh, [AppInVeh()], ExtendedRoutine(lag))



def sim_run():
    manager.step_init()

    while True:
        # for each poi agent

        # for each simulator
        for sim_id in manager.sim_repository.find_all_ids():
            sim = manager.sim_repository.resolve_by_id(sim_id)
            for veh in sim.departed_list():
                v = Vehicle(veh)
                sim.vehicle_repository.store(v)
                agent = assign_mobile_agent(v)
                if agent is not None:
                    manager.mobile_agent_repository.store(agent)
                # agent_id = uuid.uuid4().hex
                # manager.mobile_agent_repository.store(MobileAgent(agent_id, v, assign_apps(v)))

            for veh in sim.arrived_list():
                v = sim.vehicle_repository.resolve_by_id(veh)
                v._discarded = True
                sim.vehicle_repository.restore(veh)
            
            # for each mobile agent
            for agent in manager.mobile_agent_repository.find_all():
                agent.get_information()
                agent.use_app()

            # sim tick
            sim.simulation_step()

        manager.step()
        if manager.check_end():
            return


PORT = 8873
SUMOCFG_FILE = '../data/ito_test.sumocfg'

if __name__ == '__main__':
    sumoBinary = checkBinary('sumo-gui')
    sumoProcess = subprocess.Popen([sumoBinary, '-c', SUMOCFG_FILE , '--tripinfo-output', '../output/tripinfo.xml', '--remote-port', str(PORT)], stdout=sys.stdout, stderr=sys.stderr)

    traci.init(port=PORT, label='sim')

    manager.sim_repository.store( Sim("sim", PORT) )
    # manager.setting_poi()
    manager.end_step(4500)

    sim_run()

    traci.close()
    sumoProcess.wait()
