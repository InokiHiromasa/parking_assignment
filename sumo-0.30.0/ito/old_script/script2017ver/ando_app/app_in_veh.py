# _*_ coding: utf-8 -*-
from __future__ import print_function
from random import randint

import urllib2
import json
import socket
from contextlib import closing

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
    def __init__(self, addr, port):
        self._addr = addr
        self._port = port
        self._cmd = ""
        self._res = None
        self._used = False
        self._counted = False

        self.res_parking = None

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
            super(AppInVeh, self).send_information('reach_id1')

            self._counted = True


        elif not self._counted and info.road == '161947715#2':
            # AppInVeh.veh_id1-=1
            # print('leave id1')
            super(AppInVeh, self).send_information('leave_id1')
            self._counted = True


        # id2 parking vehcount
        if not self._counted and info.road == '84515126':
            # AppInVeh.veh_id2+=1
            # AppInVeh.countid2-=1
            # print('reach id2')
            super(AppInVeh, self).send_information('reach_id2')
            self._counted = True

        elif not self._counted and info.road == '-84515126':
            # AppInVeh.veh_id2-=1
            # print('leave id2')
            super(AppInVeh, self).send_information('leave_id2')
            self._counted = True

        # id3 parking vehcount
        if not self._counted and info.road == '-223785629':
            # AppInVeh.veh_id3+=1
            # AppInVeh.countid3-=1
            # print('reach id3')
            super(AppInVeh, self).send_information('reach_id3')
            self._counted = True
        elif not self._counted and info.road == '223785629':
            # AppInVeh.veh_id3-=1
            # print('leave id3')
            super(AppInVeh, self).send_information('leave_id3')
            self._counted = True

       
    #################################


    def run(self):
        id = randint(1, 3)
        
        if id == 1:
            msg = 'get_parking1'
        elif id == 2:
            msg = 'get_parking2'
        elif id == 3:
            msg = 'get_parking3'
        
        
            
        """
        url = JSON_SERVER + 'points/' + str(id)
        reader = urllib2.urlopen(url)
        item = json.loads(reader.read())
        lat = item['lat']
        lng = item['lng']
        """
        #super(AppInVeh, self)._op_app(msg)
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with closing(sock):
            sock.connect( (self._addr, self._port) )
            sock.send(msg)
            self.res_parking = sock.recv(1024)
        

        if self.res_parking == 'parking1':
            lat = 33.59592
            lng = 130.21734
        elif self.res_parking == 'parking2':
            lat = 33.598421
            lng = 130.221593
        elif self.res_parking == 'parking3':
            lat = 33.598048
            lng = 130.211299

        print(self.res_parking)
        print('lat = %f, lng = %f' %(lat, lng))

        # 反則技…
        self._res, _, _ = traci.simulation.convertRoad(lng, lat, True)
        print('res:', self._res)
        self._used = True
