# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
from random import random
from random import randint

from infrastructure.traci import *
import numpy
from time import sleep
from domain.model.manager import *

from context import layers
import notuser_layer

# 駐車場のidは上から順に2,1,3
# シミュレータ上の座標
CENTER_PARKING = [3449.20, 1920.51]
ROTARY = [3045.28, 1632.36]
WEST_PARKING = [2488.90,1857.16]
PARKING_LIST = [CENTER_PARKING, ROTARY, WEST_PARKING]
# 駐車場1階あたりのキャパシティ
CAPACITY = 160
# センサ設置階設定
# ROTARYの1階、2階に設置するなら ROTARY_sensor = '12'
ROTARY_sensor = '1'
CENTER_sensor = '1' 
WEST_sensor = '1'


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
	    # 各駐車場に向かっている車の数（[0]から順に１階，２階…)
        # id1 = ROTARY, id2 = CENTER, id3 = WEST
        # 駐車場割り当て時に参照
        self.countid1 = [0,0,0]
        self.countid2 = [0,0,0]
        self.countid3 = [0,0,0]

        # 各駐車場に停まっている車の数（[0]から順に１階，２階…）
        # 満車判定時に参照
        self.veh_id1 = [0,0,0]
        self.veh_id2 = [0,0,0]
        self.veh_id3 = [0,0,0]

        # システムが把握している駐車数
        self.vehcountid1 = [0,0,0]
        self.vehcountid2 = [0,0,0]
        self.vehcountid3 = [0,0,0]


        #評価用: 他の駐車場にchangeするハメになった回数
        #駐車場把握の正確性の指標なので非ユーザのchangeはカウントしない
        #フロアチェンジもカウントしている
        self.fullchangecount = 0
        #駐車場割り当てされた人数確認用
        self.assigned_driver = 0
        #車の流量（混み具合）チェック用
        self.allveh_count = 0


    def floor_select(self, countid, vehnumber, capacity, sensor):
        # 引数sensorは使わないが、NotUserと引数の数を合わせるため(for COP)
        # 1階から順に見て行き，満車でない階を返す
        # すべての駐車場は３階建であると仮定している
        # floor = 4は，全ての階が埋まっていることを表す
        # countidの増加に影響する
        floor = 1
        countid[0]+=1
        if countid[0] + vehnumber[0] > capacity:
            floor = 2
            countid[0]-=1
            countid[1]+=1
            if countid[1] + vehnumber[1] > capacity:
                floor = 3
                countid[1]-=1
                countid[2]+=1
                if countid[2] + vehnumber[2] > capacity:
                    floor = 4
                    countid[2]-=1

        return floor

    def NotUser_floor_select(self, veh_id, capacity, sensor, vehcountid):
        # notuser_layer activate
        f_select = ParkingServer.floor_select(veh_id, vehcountid, capacity, sensor)
        with notuser_layer.NotUser():
            self.floor_select(veh_id, vehcountid, capacity, sensor)

            """
            if str(floor) in sensor:
                #センサのある階に向かう
                #システムが把握できるのでvehcountidが加算
                #nonsensor_layer_activate
                vehcountid[floor-1]+=1
                print('<< SENSOR_floor >>')

            return floor
            """
        

    def user_fullcheck(self, vehcount, floor):
        #fullcheckで他の階層を割り当てた時，そこが空いていなかった時の他のフロアの探索用
        #入力self.vehcountid, floor 出力floor
        for f in range(1, 5):
            if f != floor:
                #fullcheckですでにチェックしたところはもう見ないのでそれ以外
                if f == 4:
                    #他の階全部埋まってました
                    return f
                    break
                elif vehcount[f-1] < CAPACITY:
                    #できるだけ下の階で，空いているところがあればreturnしてbreak
                    return f
                    break


    def parking_assignment(self, sock, need_parking):
        if need_parking == ROTARY:
            parking = 'ROTARY'
            request = 'ROTARY'# for "~~ resulted in"
            #vehcountを用いることで，「システムが把握している駐車状況」をもちいて駐車場を選択できる
            floor = self.floor_select(self.countid1, self.vehcountid1, CAPACITY, ROTARY_sensor)
            if floor == 4:
                # ROTARYが満車の時
                print('ROTARY is FULL')
                #####満車確認用#####
                print(self.countid1)
                print(self.vehcountid1)
                ##################
                print('change to CENTER')
                parking = 'CENTER'
                floor = self.floor_select(self.countid2, self.vehcountid2, CAPACITY, CENTER_sensor)
                if floor == 4:
                    # CENTERが満車の時
                    print('CENTER is FULL')
                    #####満車確認用#####
                    print(self.countid2)
                    print(self.vehcountid2)
                    ##################
                    print('change to WEST')
                    parking = 'WEST'
                    floor = self.floor_select(self.countid3, self.vehcountid3, CAPACITY, WEST_sensor)

        elif need_parking == CENTER_PARKING:
            parking = 'CENTER'
            request = 'CENTER'
            floor = self.floor_select(self.countid2, self.vehcountid2, CAPACITY, CENTER_sensor)
            if floor == 4:
                # CENTERが満車の時
                print('CENTER is FULL')
                #####満車確認用#####
                print(self.countid2)
                print(self.vehcountid2)
                ##################
                print('change to ROTARY')
                parking = 'ROTARY'
                floor = self.floor_select(self.countid1, self.vehcountid1, CAPACITY, ROTARY_sensor)
                if floor == 4:
                    # ROTARYが満車の時
                    print('ROTARY is FULL')
                    #####満車確認用#####
                    print(self.countid1)
                    print(self.vehcountid1)
                    ##################
                    print('change to WEST')
                    parking = 'WEST'
                    floor = self.floor_select(self.countid3, self.vehcountid3, CAPACITY, WEST_sensor)

        elif need_parking == WEST_PARKING:
            parking = 'WEST'
            request = 'WEST'
            floor = self.floor_select(self.countid3, self.vehcountid3, CAPACITY, WEST_sensor)
            if floor == 4:
                # WESTが満車の時
                print('WEST is FULL')
                #####満車確認用#####
                print(self.countid3)
                print(self.vehcountid3)
                ##################
                print('change to ROTARY')
                parking = 'ROTARY'
                floor = self.floor_select(self.countid1, self.vehcountid1, CAPACITY, ROTARY_sensor)
                if floor == 4:
                    # ROTARYが満車の時
                    print('ROTARY is FULL')
                    #####満車確認用#####
                    print(self.countid1)
                    print(self.vehcountid1)
                    ##################
                    print('change to CENTER')
                    parking = 'CENTER'
                    floor = self.floor_select(self.countid2, self.vehcountid2, CAPACITY, CENTER_sensor)

        # どこも満車だった場合
        if floor == 4:
            print('ALL parking is FULL')
            parking = 'GO_HOME'
            sock.send(parking)
            print(parking)


        else:
            #正常にどこかが割り当てられた場合
            #建物名と階数を結合して送信（例：ROTARY1）
            sock.send(parking+str(floor))
            print(request+' resulted in '+parking+str(floor))
            print(self.countid1, self.vehcountid1, self.veh_id1)
            print(self.countid2, self.vehcountid2, self.veh_id2)
            print(self.countid3, self.vehcountid3, self.veh_id3)
            self.assigned_driver+=1
            print('##############################################')
            print('fullchangecount is '+str(self.fullchangecount))
            print('assigned_driver is '+str(self.assigned_driver))
            print('assign_MISS rate is '+str(self.fullchangecount/self.assigned_driver))
            print('##############################################')
            #例：ROTARY resulted in ROTARY1

    def deal_msg(self, sock, msg, readfds):



        if len(msg) == 0:
            sock.close()
            readfds.remove(sock)

        
        #################################
        elif msg == 'allveh_count+1':
            self.allveh_count+=1
            #なぜかveh_idが溢れるので対応checkpoint
            #ついでにvehcountidも
            #なんで溢れるのか。おそらくnotuserfloorselectが悪さしてると思うんだけど…
            for v in range(0,3):
                if self.veh_id1[v] > CAPACITY:
                    self.veh_id1[v] = CAPACITY
                    print('veh_id1の溢れを排除')
                if self.vehcountid1[v] > CAPACITY:
                    self.vehcountid1[v] = CAPACITY
                    print('vehcountid1の溢れを排除')

            for v in range(0,3):
                if self.veh_id2[v] > CAPACITY:
                    self.veh_id2[v] = CAPACITY
                    print('veh_id2の溢れを排除')
                if self.vehcountid2[v] > CAPACITY:
                    self.vehcountid2[v] = CAPACITY
                    print('vehcountid2の溢れを排除')

            for v in range(0,3):
                if self.veh_id3[v] > CAPACITY:
                    self.veh_id3[v] = CAPACITY
                    print('veh_id3の溢れを排除')
                if self.vehcountid3[v] > CAPACITY:
                    self.vehcountid3[v] = CAPACITY
                    print('vehcountid3の溢れを排除')


        elif 'step' in msg:
            if '7' in msg:
                step = 7
            if '8' in msg:
                step = 8
            if '9' in msg:
                step = 9
            if '10' in msg:
                step = 10
            if '11' in msg:
                step = 11
            if '12' in msg:
                step = 12
            if '13' in msg:
                step = 13
            if '14' in msg:
                step = 14
            if '15' in msg:
                step = 15
            if '16' in msg:
                step = 16
            if '17' in msg:
                step = 17
            if '18' in msg:
                step = 18

            for veh in self.veh_id1:
                if veh > CAPACITY:
                    print('veh_idERROR')
                    veh = CAPACITY
            for veh in self.veh_id2:
                if veh > CAPACITY:
                    print('veh_idERROR')
                    veh = CAPACITY
            for veh in self.veh_id3:
                if veh > CAPACITY:
                    print('veh_idERROR')
                    veh = CAPACITY
            print('!!!!!!!!-------------step_'+str(step)+'_finish---------------!!!!!!!!!!')
            if self.assigned_driver == 0:
                print('Nobody  assigned')
            else:
                print('assign_MISS rate is '+str(self.fullchangecount/self.assigned_driver))
            print('allveh_count is '+str(self.allveh_count))
            print('ROTARY_parking_rate is '+str(sum(self.veh_id1)/(CAPACITY*3)))
            print('CENTER_parking_rate is '+str(sum(self.veh_id2)/(CAPACITY*3)))
            print('WEST_parking_rate is '+str(sum(self.veh_id3)/(CAPACITY*3)))
            print('whole_parking_rate is '+str((sum(self.veh_id1)+sum(self.veh_id2)+sum(self.veh_id3))/(CAPACITY*9)))
            print('----------------------------------------------------------------')
            self.fullchangecount = 0
            self.assigned_driver = 0
            self.allveh_count = 0


        # 駐車要請に対する動作
        elif 'GOTO' in msg:
            # 本当は目的地ー駐車場ー現在地の距離を計算して最適な駐車場を提案したい
            # しかしここは、「一旦要請を蓄積してから、目的地に近づいた段階で割り当て」を実装しないとぶっちゃけ意味ない
            # だからいったんやめたcheckpoint
            if msg == 'GOTOparking_1':
                best_parking = ROTARY
            elif msg == 'GOTOparking_2':
                best_parking = CENTER_PARKING
            elif msg == 'GOTOparking_3':
                best_parking = WEST_PARKING
            elif msg == 'GOTOparking_4':
                best_parking = ROTARY
            elif msg == 'GOTOparking_5':
                best_parking = CENTER_PARKING
            """
            if msg == 'GOTObuilding_1':
                destination = [3636.18,1760.38]
            elif msg == 'GOTObuilding_2':
                destination = [3602.67,1814.91]
            elif msg == 'GOTObuilding_3':
                destination = [2991.88,1600.64]
            elif msg == 'GOTObuilding_4':
                destination = [2928.38,1523.92]
            elif msg == 'GOTObuilding_5':
                destination = [2453.22,1851.65]
            elif msg == 'GOTObuilding_6':
                destination = [2453.22,1851.65]
            

            d = numpy.array(destination)


            # print('waiting for x_position')
            sock.send('x_please')
            x_position = sock.recv(4096)
            x_position_float = float(x_position)

            #x_position = float(sock.recv(4096))

            # print('waiting for y_position')
            sock.send('y_please')
            y_position = sock.recv(4096)
            y_position_float = float(y_position)

            # print([x_position_float, y_position_float])

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
                #print(total_dis)
                if total_dis < total_dis_min:
                    total_dis_min = total_dis
                    best_parking = parking
            """
            

            self.parking_assignment(sock, best_parking)
            


        # 駐車場管理
        elif 'floor' in msg:
            if 'floor1' in msg:
                floor_id = 0
            elif 'floor2' in msg:
                floor_id = 1
            elif 'floor3' in msg:
                floor_id = 2


            # id1
            if 'reach_ROTARY' in msg:
                self.vehcountid1[floor_id]+=1
                self.veh_id1[floor_id]+=1
                self.countid1[floor_id]-=1
                if self.countid1[floor_id] < 0:
                    print("countidがマイナス: ROTARY")
                    #countidマイナス対処、無理やり感あり。checkpoint
                    self.countid1[floor_id] = 0
                    
                print(msg)

            elif 'leave_ROTARY' in msg:
                #leave時にfloor_id持ってない問題解決のための苦肉の策
                #1階から順に退出していくことになっている（リアルじゃないポイント）
                if self.veh_id1[0] > 0:
                    floor_id = 0
                elif self.veh_id1[1] > 0:
                    floor_id = 1
                elif self.veh_id1[2] > 0:
                    floor_id = 2
                else:
                    #車が一切止まってない時に出ていく = もともと止まってた車のぶん
                    #カウントしないでほしい
                    floor_id = 0
                    self.veh_id1[0]+=1
                    #プラマイゼロにしたい

                #出て来た奴がアプリユーザである確率　= vehcountid / veh_id で，出て来た奴がアプリユーザかどうか決める
                User_parking_rate = 100 * self.vehcountid1[floor_id]/self.veh_id1[floor_id]
                leave_user_check = randint(1,100)
                if leave_user_check <= User_parking_rate:
                    print('@@@  ROTARY_leavecheck: User  @@@')
                    self.vehcountid1[floor_id]-=1
                else:
                    print('@@@  ROTARY_leavecheck: NotUser  @@@')

                self.veh_id1[floor_id]-=1
                print(msg)

            # id2
            elif 'reach_CENTER' in msg:
                self.vehcountid2[floor_id]+=1
                self.veh_id2[floor_id]+=1
                self.countid2[floor_id]-=1
                if self.countid2[floor_id] < 0:
                    print("countidがマイナス: CENTER")
                    #countidマイナス対処checkpoint
                    self.countid2[floor_id] = 0
                print(msg)

            elif 'leave_CENTER' in msg:
                if self.veh_id2[0] > 0:
                    floor_id = 0
                elif self.veh_id2[1] > 0:
                    floor_id = 1
                elif self.veh_id2[2] > 0:
                    floor_id = 2
                else:
                    floor_id = 0
                    self.veh_id2[0]+=1

                User_parking_rate = 100 * self.vehcountid2[floor_id]/self.veh_id2[floor_id]
                leave_user_check = randint(1,100)
                if leave_user_check <= User_parking_rate:
                    print('@@@  CENTER_leavecheck: User  @@@')
                    self.vehcountid2[floor_id]-=1
                else:
                    print('@@@  CENTER_leavecheck: NotUser  @@@')
                    
                self.veh_id2[floor_id]-=1
                print(msg)

            # id3
            elif 'reach_WEST' in msg:
                self.vehcountid3[floor_id]+=1
                self.veh_id3[floor_id]+=1
                self.countid3[floor_id]-=1
                if self.countid3[floor_id] < 0:
                    print("countidがマイナス: WEST")
                    #countidマイナス対処checkpoint
                    self.countid3[floor_id] = 0
                print(msg)

            elif 'leave_WEST' in msg:
                if self.veh_id3[0] > 0:
                    floor_id = 0
                elif self.veh_id3[1] > 0:
                    floor_id = 1
                elif self.veh_id3[2] > 0:
                    floor_id = 2
                else:
                    floor_id = 0
                    self.veh_id3[0]+=1

                User_parking_rate = 100 * self.vehcountid3[floor_id]/self.veh_id3[floor_id]
                leave_user_check = randint(1,100)
                if leave_user_check <= User_parking_rate:
                    print('@@@  WEST_leavecheck: User  @@@')
                    self.vehcountid3[floor_id]-=1

                else:
                    print('@@@  WEST_leavecheck: NotUser  @@@')

                self.veh_id3[floor_id]-=1
                print(msg)

        ###################################################################

        elif 'fullcheck' in msg:
            # 満車確認、満車時対応
            if 'NotUser' in msg:
                #非ユーザのfullcheck
                #非ユーザのfullchangecountはカウントするべきではない
                if 'ROTARY' in msg:
                    parking = 'ROTARY'
                    floor = self.NotUser_floor_select(self.veh_id1, CAPACITY, ROTARY_sensor, self.vehcountid1)
                    if floor == 4:
                        #CENTER-ROTARY間で延々走り続けるのはちょっとおかしいので
                        #ROTARYがいっぱいのときに向かう駐車場は，CENTERとWESTで半々にしようと思う

                        instant_deside = randint(1,2)
                        
                        if instant_deside == 1:
                            parking = 'CENTER'
                            print('NotUser changed ROTARY to CENTER')
                        elif instant_deside == 2:
                            parking = 'WEST'
                            print('NotUser changed ROTARY to WEST')
                        
                elif 'CENTER' in msg:
                    parking = 'CENTER'
                    floor =  self.NotUser_floor_select(self.veh_id2, CAPACITY, CENTER_sensor, self.vehcountid2)
                    if floor == 4:
                        parking = 'ROTARY'
                        print('NotUser changed CENTER to ROTARY')
                     
                elif 'WEST' in msg:
                    parking = 'WEST'
                    floor =  self.NotUser_floor_select(self.veh_id3, CAPACITY, WEST_sensor, self.vehcountid3)
                    if floor == 4:
                        parking = 'ROTARY'
                        print('NotUser changed WEST to ROTARY')

                print('Notuser_fullcheck: '+'GOTO_'+parking+str(floor))
                sock.send('GOTO_'+parking+str(floor))#e.g. GOTO_ROTARY1




            #以下、ユーザのfullcheck

            elif 'ROTARY' in msg:
                OK_check = False
                #OK_check == True : 想定していたところがちゃんと空いていた
                if '1' in msg:
                    OK_check_floorid = 0
                    if self.veh_id1[0] < CAPACITY:
                        sock.send('OK')
                        print('user_fullcheck: OK')
                        OK_check = True
                elif '2' in msg:
                    OK_check_floorid = 1
                    if self.veh_id1[1] < CAPACITY:
                        sock.send('OK')
                        print('user_fullcheck: OK')
                        OK_check = True
                elif '3' in msg:
                    OK_check_floorid = 2
                    if self.veh_id1[2] < CAPACITY:
                        sock.send('OK')
                        print('user_fullcheck: OK')
                        OK_check = True

                if OK_check == False:
                    #空いてなかった場合
                    #割り当てたところが空いていなかった　＝　駐車場の把握が失敗している
                    #向かう予定だったのをやめるのでcountidを1下げる
                    self.countid1[OK_check_floorid]-=1
                    # うまってたことをシステムに報告
                    if self.vehcountid1[OK_check_floorid] < CAPACITY:
                        print('OK_check_floorid is: '+str(OK_check_floorid))
                        self.vehcountid1[OK_check_floorid] += 1
                        print('空いてると思ってたけど空いてなかった')

                    floor = self.floor_select(self.countid1, self.vehcountid1, CAPACITY, ROTARY_sensor)
                    if floor <= 3:
                        #システムから見て他の階が空いていた時
                        if self.veh_id1[floor-1] < CAPACITY:
                            #ほんとに他の階が空いていたならそこに変更
                            print('user_fullcheck:'+'changefloor_to_'+str(floor))
                            sock.send('changefloor_to_'+str(floor))
                        else:
                            print('そっちの階も空いていません')
                            self.countid1[floor-1]-=1
                            #他の階を探索，一度探索したところは探索しない（するとシステムが駐車状況を完璧に把握してしまう）
                            changed_floor = self.user_fullcheck(self.vehcountid1, floor)
                            floor = changed_floor
                            #割り当てし直しているのでfullchangecountにプラス1．．．したら数が大変なことになる
                            if floor <= 3:
                                print('user_fullcheck:'+'changefloor_to_'+str(floor))
                                sock.send('changefloor_to_'+str(floor))
                                self.countid1[floor-1]+=1



                    if floor == 4:
                        #他の階も空いていなかったとき
                        #別の駐車場チェック、近い順(この決め方、雑かも)
                        floor = self.floor_select(self.countid2, self.veh_id2, CAPACITY, CENTER_sensor)
                        parking = 'CENTER'
                        if floor == 4:
                            floor = self.floor_select(self.countid3, self.veh_id3, CAPACITY, WEST_sensor)
                            parking = 'WEST'
                            if floor == 4:
                                parking = 'GO_HOME'
                                self.assigned_driver-=1
                                #gohomeは割り当てとは言えないので，プラマイゼロにしたい
                        self.assigned_driver+=1
                        print('user_fullcheck:'+'changeparking_to_'+parking+str(floor))
                        sock.send('changeparking_to_'+parking+str(floor))

                if OK_check == False:
                    self.fullchangecount+=1
                    print('##############################################')
                    print('fullchangecount is '+str(self.fullchangecount))
                    print('assigned_driver is '+str(self.assigned_driver))
                    if self.assigned_driver <= 0:
                        print('前のフェーズで割り当てられた人のfullcheckでした')
                        self.assigned_driver=1
                        #zero division対策
                    if self.fullchangecount > self.assigned_driver:
                        #ミス率が100%超えるのはありえない
                        print('前のフェーズで割り当てられた人のfullchangeです')
                        self.assigned_driver+=1

                    print('assign_MISS rate is '+str(self.fullchangecount/self.assigned_driver))
                    print('##############################################')

            elif 'CENTER' in msg:
                OK_check = False
                if '1' in msg:
                    OK_check_floorid = 0
                    if self.veh_id2[0] < CAPACITY:
                        sock.send('OK')
                        print('user_fullcheck: OK')
                        OK_check = True
                elif '2' in msg:
                    OK_check_floorid = 1
                    if self.veh_id2[1] < CAPACITY:
                        sock.send('OK')
                        print('user_fullcheck: OK')
                        OK_check = True
                elif '3' in msg:
                    OK_check_floorid = 2
                    if self.veh_id2[2] < CAPACITY:
                        sock.send('OK')
                        print('user_fullcheck: OK')
                        OK_check = True

                if OK_check == False:
                    #空いてなかった場合
                    self.countid2[OK_check_floorid]-=1
                    if self.vehcountid2[OK_check_floorid] < CAPACITY:
                        print('OK_check_floorid is: '+str(OK_check_floorid))
                        self.vehcountid2[OK_check_floorid] += 1
                        print('空いてると思ってたけど空いてなかった')

                    floor = self.floor_select(self.countid2, self.vehcountid2, CAPACITY, CENTER_sensor)
                    if floor <= 3:
                        if self.veh_id2[floor-1] < CAPACITY:
                            print('user_fullcheck:'+'changefloor_to_'+str(floor))
                            sock.send('changefloor_to_'+str(floor))
                        else:
                            print('そっちの階も空いていません')
                            self.countid2[floor-1]-=1
                            changed_floor = self.user_fullcheck(self.vehcountid2, floor)
                            floor = changed_floor
                            if floor <= 3:
                                print('user_fullcheck:'+'changefloor_to_'+str(floor))
                                sock.send('changefloor_to_'+str(floor))
                                self.countid2[floor-1]+=1

                    if floor == 4:
                        floor = self.floor_select(self.countid1, self.veh_id1, CAPACITY, ROTARY_sensor)
                        parking = 'ROTARY'
                        if floor == 4:
                            floor = self.floor_select(self.countid3, self.veh_id3, CAPACITY, WEST_sensor)
                            parking = 'WEST'
                            if floor == 4:
                                parking = 'GO_HOME'
                                self.assigned_driver-=1
                                #gohomeは割り当てとは言えないので，プラマイゼロにしたい
                        self.assigned_driver+=1
                        print('user_fullcheck:'+'changeparking_to_'+parking+str(floor))
                        sock.send('changeparking_to_'+parking+str(floor))

                if OK_check == False:
                    self.fullchangecount+=1
                    print('##############################################')
                    print('fullchangecount is '+str(self.fullchangecount))
                    print('assigned_driver is '+str(self.assigned_driver))
                    if self.assigned_driver <= 0:
                        print('前のフェーズで割り当てられた人のfullcheckでした')
                        self.assigned_driver=1
                        #zero division対策
                    if self.fullchangecount > self.assigned_driver:
                        #ミス率が100%超えるのはありえない
                        print('前のフェーズで割り当てられた人のfullchangeです')
                        self.assigned_driver+=1
                    print('assign_MISS rate is '+str(self.fullchangecount/self.assigned_driver))
                    print('##############################################')

            elif 'WEST' in msg:
                OK_check = False
                if '1' in msg:
                    OK_check_floorid = 0
                    if self.veh_id3[0] < CAPACITY:
                        sock.send('OK')
                        print('user_fullcheck: OK')
                        OK_check = True
                elif '2' in msg:
                    OK_check_floorid = 1
                    if self.veh_id3[1] < CAPACITY:
                        sock.send('OK')
                        print('user_fullcheck: OK')
                        OK_check = True
                elif '3' in msg:
                    OK_check_floorid = 2
                    if self.veh_id3[2] < CAPACITY:
                        sock.send('OK')
                        print('user_fullcheck: OK')
                        OK_check = True

                if OK_check == False:
                    #空いてなかった場合
                    self.countid3[OK_check_floorid]-=1
                    if self.vehcountid3[OK_check_floorid] < CAPACITY:
                        print('OK_check_floorid is: '+str(OK_check_floorid))
                        self.vehcountid3[OK_check_floorid] += 1
                        print('空いてると思ってたけど空いてなかった')
                    floor = self.floor_select(self.countid3, self.vehcountid3, CAPACITY, WEST_sensor)

                    if floor <= 3:
                        if self.veh_id3[floor-1] < CAPACITY:
                            print('user_fullcheck:'+'changefloor_to_'+str(floor))
                            sock.send('changefloor_to_'+str(floor))
                        else:
                            print('そっちの階も空いていません')
                            self.countid3[floor-1]-=1
                            changed_floor = self.user_fullcheck(self.vehcountid3 , floor)
                            floor = changed_floor
                            if floor <= 3:
                                print('user_fullcheck:'+'changefloor_to_'+str(floor))
                                sock.send('changefloor_to_'+str(floor))
                                self.countid3[floor-1]+=1

                    if floor == 4:
                        floor = self.floor_select(self.countid1, self.veh_id1, CAPACITY, ROTARY_sensor)
                        parking = 'ROTARY'
                        if floor == 4:
                            floor = self.floor_select(self.countid2, self.veh_id2, CAPACITY, CENTER_sensor)
                            parking = 'CENTER'
                            if floor == 4:
                                parking = 'GO_HOME'
                                self.assigned_driver-=1
                                #gohomeは割り当てとは言えないので，プラマイゼロにしたい
                        self.assigned_driver+=1
                        print('user_fullcheck:'+'changeparking_to_'+parking+str(floor))
                        sock.send('changeparking_to_'+parking+str(floor))



                if OK_check == False:
                    self.fullchangecount+=1
                    print('##############################################')
                    print('fullchangecount is '+str(self.fullchangecount))
                    print('assigned_driver is '+str(self.assigned_driver))
                    if self.assigned_driver <= 0:
                        print('前のフェーズで割り当てられた人のfullcheckでした')
                        self.assigned_driver=1
                        #zero division対策
                    if self.fullchangecount > self.assigned_driver:
                        #ミス率が100%超えるのはありえない
                        print('前のフェーズで割り当てられた人のfullchangeです')
                        self.assigned_driver+=1
                    print('assign_MISS rate is '+str(self.fullchangecount/self.assigned_driver))
                    print('##############################################')










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