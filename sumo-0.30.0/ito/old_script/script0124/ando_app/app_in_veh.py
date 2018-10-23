# _*_ coding: utf-8 -*-
from __future__ import print_function
from random import randint

import urllib2
import json
import socket
from contextlib import closing
import numpy
from time import sleep

from infrastructure.traci import *
from infrastructure.shared.baseclient import BaseClient
from domain.model.vehicle import Vehicle
from domain.model.manager import *



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


        self.res_message = None

    def event_handler(self, info):
        # アプリの起動条件
        # このタイミングもっと早くする
        # 一定割合の人にはアプリを適用せずに適当に駐車場に向かってもらうようにする
        # 適用しなかった人にはそれとわかる色を設定(灰色)
        if not self._used and info.road == '84515125#3':
            notrecommend = randint(1,100)
            print('--------------------------------')
            if notrecommend <= 30:#30%でアプリを起動させない（リコメンドされない）   
                print('not recommended')
                return 'NotUser'
                

            elif notrecommend > 30:
                print('recommended')
                return 'User'
                
        else:
            return False
###################################
    def vehcount(self,info):
        # id1 parking vehcount
        if not self._counted and info.road == '-161947715#2':
            super(AppInVeh, self).send_information('reach_id1')
            self._counted = True

        elif not self._counted and info.road == '161947715#2':       
            super(AppInVeh, self).send_information('leave_id1')
            self._counted = True

        # id2 parking vehcount
        if not self._counted and info.road == '84515126':
            super(AppInVeh, self).send_information('reach_id2')
            self._counted = True

        elif not self._counted and info.road == '-84515126':
            super(AppInVeh, self).send_information('leave_id2')
            self._counted = True

        # id3 parking vehcount
        if not self._counted and info.road == '-223785629':
            super(AppInVeh, self).send_information('reach_id3')
            self._counted = True

        elif not self._counted and info.road == '223785629':
            super(AppInVeh, self).send_information('leave_id3')
            self._counted = True
    #################################

    def notuser_run(self):
        # とりあえず強制的にウエストに行ってもらう
        id = randint(1,3)
        if id == 1:
            lat = 33.59592
            lng = 130.21734
            print('NOTuser_ROTARY')
        elif id == 2:
            lat = 33.598421
            lng = 130.221593
            print('NOTuser_CENTER')
        elif id == 3:
            lat = 33.598048
            lng = 130.211299
            print('NOTuser_WEST')

        self._res, _, _ = traci.simulation.convertRoad(lng, lat, True)
        print('res:', self._res)
        self._used = True



    def run(self, x_position, y_position):
        # 目的地設定，ゴリ押し
        id = randint(1, 6)

        """
        if id == 1:
            destination = [3636.18,1760.38]
        elif id == 2:
            destination = [3602.67,1814.91]
        elif id == 3:
            destination = [3198.50,1716.14]
        elif id == 4:
            destination = [3091.93,1840.13]
        elif id == 5:
            destination = [2991.88,1600.64]
        elif id == 6:
            destination = [2480.42,1701.82]

        d = numpy.array(destination)

        veh_position = [x_position, y_position]
        v = numpy.array(veh_position)

        # 目的地ー駐車場，駐車場ー現在の車の位置の直線距離を計算，最小のものを探す
        # これほんとはサーバ側でやるべき
        total_dis_min = float("inf")
        for parking in PARKING_LIST:
            p = numpy.array(parking)
            DP_distance = numpy.linalg.norm(p - d)
            PV_distance = numpy.linalg.norm(v - p)
            total_dis = DP_distance + PV_distance
            print(total_dis)
            if total_dis < total_dis_min:
                total_dis_min = total_dis
                assign_parking = parking

        print(id)
        print('assign_parking is...')

        if assign_parking == CENTER_PARKING:
            print('CENTER_PARKING')
            p_id = 2
        elif assign_parking == ROTARY:
            print('ROTARY')
            p_id = 1
        elif assign_parking == WEST_PARKING:
            print('WEST_PARKING')
            p_id = 3
        """
        
        if id == 1:
            msg = 'GOTObuilding_1'
        elif id == 2:
            msg = 'GOTObuilding_2'
        elif id == 3:
            msg = 'GOTObuilding_3'
        elif id == 4:
            msg = 'GOTObuilding_4'
        elif id == 5:
            msg = 'GOTObuilding_5'
        elif id == 6:
            msg = 'GOTObuilding_6'
            
        """
        url = JSON_SERVER + 'points/' + str(id)
        reader = urllib2.urlopen(url)
        item = json.loads(reader.read())
        lat = item['lat']
        lng = item['lng']
        """
        #super(AppInVeh, self)._op_app(msg)
        # なぜかbaseclientのを利用しようとすると上手くいかない…？
        #msg(GOTO~~)を送信し，'x_please'を受け取る予定
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with closing(sock):
            sock.connect( (self._addr, self._port) )
            sock.send(msg)
            self.res_message = sock.recv(1024)
            if self.res_message == 'x_please':
                sock.send(str(x_position))
                self.res_message = sock.recv(1024)

                if self.res_message == 'y_please':
                    sock.send(str(y_position))
                    self.res_message = sock.recv(1024)

        # 目的地送信後，x，yの順に現在地を送信
        # サーバからの合図をもとに送信するけどここが上手く行ってない可能性…
        # 'x_position'を送信し，'y_please'を受け取る予定

        
        print('res_parking is ...')
        if self.res_message == 'ROTARY':
            lat = 33.59592
            lng = 130.21734
        elif self.res_message == 'CENTER':
            lat = 33.598421
            lng = 130.221593
        elif self.res_message == 'WEST':
            lat = 33.598048
            lng = 130.211299

        if self.res_message:
            print(self.res_message)
            print('lat = %f, lng = %f' %(lat, lng))

            # 反則技…　
            self._res, _, _ = traci.simulation.convertRoad(lng, lat, True)
            print('res:', self._res)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            self._used = True
