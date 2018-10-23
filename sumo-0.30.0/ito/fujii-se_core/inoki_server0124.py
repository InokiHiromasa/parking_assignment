# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
from random import random
#####
from infrastructure.traci import *
import numpy
from time import sleep

# 駐車場のidは上から順に2,1,3
# シミュレータ上の座標でやってるけど建物番号みたいなのでやりたいなあ（poly）
CENTER_PARKING = [3449.20, 1920.51]
ROTARY = [3045.28, 1632.36]
WEST_PARKING = [2488.90,1857.16]
PARKING_LIST = [CENTER_PARKING, ROTARY, WEST_PARKING]

#####

if 'SE_HOME' in os.environ:

    tools = os.path.join(os.environ['SE_HOME'], 'tools')
    sys.path.append(tools)
    from infrastructure.shared.baseserver import BaseServer

else:
    sys.path.append("../")
    from infrastructure.shared.baseserver import BaseServer


# PARKING_LIST = ['p1en', 'p3en']

# data = {}



class ParkingServer(BaseServer):
    def __init__(self, host, port):
        BaseServer.__init__(self, host, port)
	    # 各駐車場に向かっている車の数
        self.countid1 = 0
        self.countid2 = 0
        self.countid3 = 0
        # 各駐車場に停まっている車の数    
        self.veh_id1 = 0
        self.veh_id2 = 0
        self.veh_id3 = 0

    def vehcount(self, sock, need_parking):
        if need_parking == ROTARY:
            self.countid1+=1
            parking = 'ROTARY'
            if self.countid1 + self.veh_id1 >= 10:
                    # １がいっぱいのとき
                if self.countid2 + self.veh_id2< 10:
                    parking = 'CENTER'
                    print('change id 1 to 2')
                    print(self.countid1)
                    print(self.veh_id1)
                elif self.countid3 + self.veh_id3< 10:
                    parking = 'WEST'
                    print('change id 1 to 3')
                    print(self.countid1)
                    print(self.veh_id1)
                else:
                    print('There is no available parking')
                    print(self.countid1)
                    print(self.veh_id1)
                    print(self.countid2)
                    print(self.veh_id2)
                    print(self.countid3)
                    print(self.veh_id3)
                self.countid1-=1
            sock.send(parking)
            print('get_ROTARY resulted in '+parking)

        elif need_parking == CENTER_PARKING:
            self.countid2+=1
            parking = 'CENTER'
            if self.countid2 + self.veh_id2 >= 10:
                    # 2がいっぱいのとき
                
                if self.countid1 + self.veh_id1 < 10:
                    parking = 'ROTARY'
                    print('change id 2 to 1')
                    print(self.countid2)
                    print(self.veh_id2)
                elif self.countid3 + self.veh_id3< 10:
                    parking = 'WEST'
                    print('change id 2 to 3')
                    print(self.countid2)
                    print(self.veh_id2)
                else:
                    print('There is no available parking')
                    print(self.countid1)
                    print(self.veh_id1)
                    print(self.countid2)
                    print(self.veh_id2)
                    print(self.countid3)
                    print(self.veh_id3)
                self.countid2-=1

            sock.send(parking)
            print('get_CENTER resulted in '+parking)

        elif need_parking == WEST_PARKING:
            self.countid3+=1
            parking = 'WEST'
            if self.countid3 + self.veh_id3 >= 10:
                # 3がいっぱいのとき
                
                if self.countid1 + self.veh_id1< 10:
                    parking = 'ROTARY'
                    print('change id 3 to 1')
                    print(self.countid3)
                    print(self.veh_id3)
                elif self.countid2 + self.veh_id2< 10:
                    parking = 'CENTER'
                    print('change id 3 to 2')
                    print(self.countid3)
                    print(self.veh_id3)
                else:
                    print('There is no available parking')
                    print(self.countid1)
                    print(self.veh_id1)
                    print(self.countid2)
                    print(self.veh_id2)
                    print(self.countid3)
                    print(self.veh_id3)
                self.countid3-=1

            sock.send(parking)
            print('get_WEST resulted in '+parking)




    def deal_msg(self, sock, msg, readfds):


        if len(msg) == 0:
            sock.close()
            readfds.remove(sock)

        
        #################################
        # 駐車要請に対する動作
        elif 'GOTO' in msg:
            if msg == 'GOTObuilding_1':
                destination = [3636.18,1760.38]
            elif msg == 'GOTObuilding_2':
                destination = [3602.67,1814.91]
            elif msg == 'GOTObuilding_3':
                destination = [3198.50,1716.14]
            elif msg == 'GOTObuilding_4':
                destination = [3091.93,1840.13]
            elif msg == 'GOTObuilding_5':
                destination = [2991.88,1600.64]
            elif msg == 'GOTObuilding_6':
                destination = [2480.42,1701.82]

            d = numpy.array(destination)


            print('waiting for x_position')
            sock.send('x_please')
            x_position = sock.recv(4096)
            x_position_float = float(x_position)

            #x_position = float(sock.recv(4096))

            print('waiting for y_position')
            sock.send('y_please')
            y_position = sock.recv(4096)
            y_position_float = float(y_position)

            print([x_position_float, y_position_float])

            veh_position = [x_position_float, y_position_float]
            v = numpy.array(veh_position)

            # 目的地ー駐車場，駐車場ー現在の車の位置の直線距離を計算，最小のものを探す
            # 最小の駐車場をassign_parkingに格納
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

            self.vehcount(sock, assign_parking)
            


        # 駐車場管理・id1
        elif msg == 'reach_id1':
            self.veh_id1+=1
            self.countid1-=1
            print('reach id1')

        elif msg == 'leave_id1':
            self.veh_id1-=1
            print('leave id1')

        # id2
        elif msg == 'reach_id2':
            self.veh_id2+=1
            self.countid2-=1
            print('reach id2')

        elif msg == 'leave_id2':
            self.veh_id2-=1
            print('leave id2')

        # id3
        elif msg == 'reach_id3':
            self.veh_id3+=1
            self.countid3-=1
            print('reach id3')

        elif msg == 'leave_id3':
            self.veh_id3-=1
            print('leave id3')


        ####################################
        

        else:
            # res = msg.split(" ")

            #if res[0] == "info":
            #    name = res[1].split(":")[1]
            #    porp = res[4].split(":")[1]
            #   data[name] = porp

            #    if res[5].split(":")[1] == "3990":

            #        exit()

            print(msg)
        



if __name__ == '__main__':

    ParkingServer('127.0.0.1', 4000).run()