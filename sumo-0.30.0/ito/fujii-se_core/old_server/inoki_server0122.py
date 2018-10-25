# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
from random import random
#####
from infrastructure.traci import *

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


    def deal_msg(self, sock, msg, readfds):


        if len(msg) == 0:
            sock.close()
            readfds.remove(sock)



        
        #################################
        # 駐車要請に対する動作
        elif msg == 'get_parking1':
            self.countid1+=1
            parking = 'parking1'
            if self.countid1 + self.veh_id1 >= 10:
                    # １がいっぱいのとき
                if self.countid2 + self.veh_id2< 10:
                    parking = 'parking2'
                    print('change id 1 to 2')
                    print(self.countid1)
                    print(self.veh_id1)
                elif self.countid3 + self.veh_id3< 10:
                    parking = 'parking3'
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
            print('get_parking1 success')

        elif msg == 'get_parking2':
            self.countid2+=1
            parking = 'parking2'
            if self.countid2 + self.veh_id2 >= 10:
                    # 2がいっぱいのとき
                
                if self.countid1 + self.veh_id1 < 10:
                    parking = 'parking1'
                    print('change id 2 to 1')
                    print(self.countid2)
                    print(self.veh_id2)
                elif self.countid3 + self.veh_id3< 10:
                    parking = 'parking3'
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
            print('get_parking2 success')

        elif msg == 'get_parking3':
            self.countid3+=1
            parking = 'parking3'
            if self.countid3 + self.veh_id3 >= 10:
                # 3がいっぱいのとき
                
                if self.countid1 + self.veh_id1< 10:
                    parking = 'parking1'
                    print('change id 3 to 1')
                    print(self.countid3)
                    print(self.veh_id3)
                elif self.countid2 + self.veh_id2< 10:
                    parking = 'parking2'
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
            print('get_parking3 success')

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