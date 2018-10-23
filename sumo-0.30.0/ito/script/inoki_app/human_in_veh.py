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

#notUserが各駐車場にreachした際に使う
road_list = ['-161947715#2', '84515126', '-223785629']



# JSON_SERVER = 'http://localhost:3000/'

class HumanInVeh(BaseClient):
    # アプリユーザでない人間の動き
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
        self.floor = 0
        

    def event_handler(self, info):
        # アプリの起動条件
        # このタイミングもっと早くする
        # 一定割合の人にはアプリを適用せずに適当に駐車場に向かってもらうようにする
        # 適用しなかった人にはそれとわかる色を設定(灰色)
        if not self._used and info.road == '84515125#3':
            return 'NotUser'
                
        else:
            return False
###################################
    def vehcount(self,info):
        # アプリユーザでない人間が駐車場についた時・出る時の処理
        #　出る時に関してはアプリユーザと一緒
        # ついたとき，サーバにその旨を伝え，満車判定をサーバ側で行う（その判定結果を待つ）
        # 満車だった場合，行き先変更

        # id1 parking vehcount
        if not self._counted and info.road == '-161947715#2':
            print('NotUser reach_ROTARY')
            super(HumanInVeh, self).send_information('NotUser_reach_ROTARY')
            self._counted = True

        elif not self._counted and info.road == '161947715#2':
            print('NotUser leave_ROTARY')
            super(HumanInVeh, self).send_information('NotUser_leave_ROTARY')
            self._counted = True

        # id2 parking vehcount
        if not self._counted and self.AppUser and info.road == '84515126':
            print('to floor'+str(self.floor))
            super(HumanInVeh, self).send_information('reach_CENTER_floor'+str(self.floor))
            self._counted = True

        elif not self._counted and info.road == '-84515126':
            print('from floor'+str(self.floor))
            
            super(HumanInVeh, self).send_information('leave_CENTER_floor'+str(self.floor))
            self._counted = True

        # id3 parking vehcount
        if not self._counted and self.AppUser and info.road == '-223785629':
            print('to floor'+str(self.floor))
            super(HumanInVeh, self).send_information('reach_WEST_floor'+str(self.floor))
            self._counted = True

        elif not self._counted and info.road == '223785629':
            print('from floor'+str(self.floor))
            super(HumanInVeh, self).send_information('leave_WEST_floor'+str(self.floor))
            self._counted = True


    #################################

    def notuser_run(self):
        # 適当な駐車場の適当な階に向かってもらう
        # 満車だろうと向かうのでまだ改善が必要
        id = randint(1,3)
        self.floor = 1
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
        #super(HumanInVeh, self)._op_app(msg)
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
        if 'ROTARY' in self.res_message:
            lat = 33.59592
            lng = 130.21734
        elif 'CENTER' in self.res_message:
            lat = 33.598421
            lng = 130.221593
        elif 'WEST' in self.res_message:
            lat = 33.598048
            lng = 130.211299
        elif self.res_message == 'GO_HOME':
            # どこに向かわせればいいのかよくわからん…
            # とりあえず適当に
            lat = 30
            lng = 130

        # 階数判定
        if '1' in self.res_message:
            self.floor = 1
        elif '2' in self.res_message:
            self.floor = 2
        elif '3' in self.res_message:
            self.floor = 3



        if self.res_message:
            print(self.res_message)
            print('lat = %f, lng = %f' %(lat, lng))

            # 反則技…　
            self._res, _, _ = traci.simulation.convertRoad(lng, lat, True)
            print('res:', self._res)
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            self._used = True
