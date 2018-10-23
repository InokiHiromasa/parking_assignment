# _*_ coding: utf-8 -*-
from __future__ import print_function
from random import randint

import urllib2
import json

from infrastructure.traci import *
from infrastructure.shared.baseclient import BaseClient



# JSON_SERVER = 'http://localhost:3000/'

class AppInVeh(BaseClient):
    """
    # 各駐車場に向かっている車の数
    countid1 = 0
    countid2 = 0
    countid3 = 0
    # 各駐車場に停まっている車の数    
    veh_id1 = 0
    veh_id2 = 0
    veh_id3 = 0
    """
    def __init__(self):
        BaseClient.init()
        self._res = None
        self._used = False
        self._counted = False

    def event_handler(self, info):
        # アプリの起動条件
        if not self._used and info.road == '84515125#3':
            # notrecommend = randint(1,100)
            # if notrecommend <= 30:#30%でアプリを起動させない（リコメンドされない）   
            #     print(notrecommend)
            #     return False
            # else:
            #     print(notrecommend)
            #     return True
            return True
        else:
            return False
###################################
    def vehcount(self,info):
        # id1 parking vehcount
        if not self._counted and info.road == '-161947715#2':
            # AppInVeh.veh_id1+=1
            # AppInVeh.countid1-=1
            # print('reach id1')
            self._counted = True


        elif not self._counted and info.road == '161947715#2':
            AppInVeh.veh_id1-=1
            print('leave id1')
            self._counted = True


        # id2 parking vehcount
        if not self._counted and info.road == '84515126':
            AppInVeh.veh_id2+=1
            AppInVeh.countid2-=1
            print('reach id2')
            self._counted = True
        elif not self._counted and info.road == '-84515126':
            AppInVeh.veh_id2-=1
            print('leave id2')
            self._counted = True

        # id3 parking vehcount
        if not self._counted and info.road == '-223785629':
            AppInVeh.veh_id3+=1
            AppInVeh.countid3-=1
            print('reach id3')
            self._counted = True
        elif not self._counted and info.road == '223785629':
            AppInVeh.veh_id3-=1
            print('leave id3')
            self._counted = True

       
    #################################


    def run(self):
        id = randint(1, 3)
        """
        if id == 1: 
            AppInVeh.countid1+=1
            if AppInVeh.countid1 + AppInVeh.veh_id1 >= 10:
                    # １がいっぱいのとき
                if AppInVeh.countid2 + AppInVeh.veh_id2< 10:
                    id = 2
                    print('change id 1 to 2')
                    print(AppInVeh.countid1)
                    print(AppInVeh.veh_id1)
                elif AppInVeh.countid3 + AppInVeh.veh_id3< 10:
                    id = 3
                    print('change id 1 to 3')
                    print(AppInVeh.countid1)
                    print(AppInVeh.veh_id1)
                else:
                    print('There is no available parking')
                    print(AppInVeh.countid1)
                    print(AppInVeh.veh_id1)
                    print(AppInVeh.countid2)
                    print(AppInVeh.veh_id2)
                    print(AppInVeh.countid3)
                    print(AppInVeh.veh_id3)
                AppInVeh.countid1-=1

        elif id == 2:
            AppInVeh.countid2+=1
            if AppInVeh.countid2 + AppInVeh.veh_id2 >= 10:
                    # 2がいっぱいのとき
                
                if AppInVeh.countid1 + AppInVeh.veh_id1 < 10:
                    id = 1
                    print('change id 2 to 1')
                    print(AppInVeh.countid2)
                    print(AppInVeh.veh_id2)
                elif AppInVeh.countid3 + AppInVeh.veh_id3< 10:
                    id = 3
                    print('change id 2 to 3')
                    print(AppInVeh.countid2)
                    print(AppInVeh.veh_id2)
                else:
                    print('There is no available parking')
                    print(AppInVeh.countid1)
                    print(AppInVeh.veh_id1)
                    print(AppInVeh.countid2)
                    print(AppInVeh.veh_id2)
                    print(AppInVeh.countid3)
                    print(AppInVeh.veh_id3)
                AppInVeh.countid2-=1

        elif id == 3:
            AppInVeh.countid3+=1
            if AppInVeh.countid3 + AppInVeh.veh_id3 >= 10:
                # 3がいっぱいのとき
                
                if AppInVeh.countid1 + AppInVeh.veh_id1< 10:
                    id = 1
                    print('change id 3 to 1')
                    print(AppInVeh.countid3)
                    print(AppInVeh.veh_id3)
                elif AppInVeh.countid2 + AppInVeh.veh_id2< 10:
                    id = 2
                    print('change id 3 to 2')
                    print(AppInVeh.countid3)
                    print(AppInVeh.veh_id3)
                else:
                    print('There is no available parking')
                    print(AppInVeh.countid1)
                    print(AppInVeh.veh_id1)
                    print(AppInVeh.countid2)
                    print(AppInVeh.veh_id2)
                    print(AppInVeh.countid3)
                    print(AppInVeh.veh_id3)
                AppInVeh.countid3-=1
        """
        try:
            
            """
            url = JSON_SERVER + 'points/' + str(id)
            reader = urllib2.urlopen(url)
            item = json.loads(reader.read())
            lat = item['lat']
            lng = item['lng']
            """
            # 反則技…
            self._res, _, _ = traci.simulation.convertRoad(lng, lat, True)
            print('res:', self._res)
            self._used = True

        finally:
            reader.close()