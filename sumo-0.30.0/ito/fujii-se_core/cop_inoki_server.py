# -*- coding: utf-8 -*-
##stepごとの結果表示は277
from __future__ import division, print_function, absolute_import, unicode_literals

import os
import sys
from random import random
from random import randint

from infrastructure.traci import *
import numpy as np
from time import sleep
from domain.model.manager import *

from context import layers
import notuser_layer
import layerselect

# 駐車場のidは上から順に2,1,3
# シミュレータ上の座標
CENTER_PARKING = [3449.20, 1920.51]
ROTARY = [3045.28, 1632.36]
WEST_PARKING = [2488.90,1857.16]
PARKINGS_NAME = ["CENTER", "ROTARY", "WEST"]
parking_dict = {"ROTARY":0, "CENTER":1, "WEST":2}
# 駐車場（建物）の数
PARKINGS_NUMBER = 3
# 駐車場ごとの階数
FLOORS_NUMBER = 3
# 駐車場1階あたりののキャパシティ
CAPACITY = 160
# センサ設置階設定
# ROTARYの1階、2階に設置するなら ROTARY_sensor = '12'
ROTARY_sensor = '12'
CENTER_sensor = '12' 
WEST_sensor = '12'


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
        ## [[ROTARY1,ROTARY2,ROTARY3],[CENTER1,CENTER2,CENTER3],[WEST1,WEST2,WEST3]]
        self.going = np.array([[0]*FLOORS_NUMBER for p in range(PARKINGS_NUMBER)])# 各駐車場に向かっている車の数
        self.veh = np.array([[0]*FLOORS_NUMBER for p in range(PARKINGS_NUMBER)])# 各駐車場に停まっている車の数
        self.veh_counted = np.array([[0]*FLOORS_NUMBER for p in range(PARKINGS_NUMBER)])# システムが把握している駐車数
        self.available_on_system = [[True]*FLOORS_NUMBER for p in range(PARKINGS_NUMBER)]#システムから見た満車判定用（True:空車 False:満車）
        self.available_actual = [[True]*FLOORS_NUMBER for p in range(PARKINGS_NUMBER)]#実際の満車判定用

        #評価用: 
        self.fullchangecount = 0 #他の駐車場にchangeするハメになった回数（フロアチェンジも含む、非ユーザはカウントしない）
        self.assigned_driver = 0#駐車場割り当てされた人数確認用
        self.allveh_count = 0#車の流量（混み具合）チェック用

    def parking_check(self,veh_number,available_info):
        #駐車状況チェック
        #システム上の状況:veh_number=veh_counted+going, available_info=available_on_system
        #実際の状況:vehnumber=veh, available_info=available_actual
        for p in range(PARKINGS_NUMBER):
            for f in range(FLOORS_NUMBER):
                if veh_number[p][f] >= CAPACITY:
                    available_info[p][f] = False
                    #vehがキャパ越えするのはエラー
                    if veh_number[p][f]>CAPACITY:
                        print("veh_number error")
                        veh_number[p][f] = CAPACITY
                else:
                    available_info[p][f] = True

    def parking_allcheck(self):
        self.parking_check(self.veh, self.available_actual)
        self.parking_check(self.veh_counted+self.going, self.available_on_system)


    def parking_select(self, parking, floor, available_info):
        #駐車判定
        #戻り値：parkingとfloor(id)、発見判定parking_found
        #まず与えられた駐車場・フロアの駐車判定
        if available_info[parking][floor] == True:
            print("parking succeeded")
            return(parking,floor)
            parking_found = True

        #parking_found=falseなら同じ駐車場の他の階を下から順に探索
        if parking_found != True:
            for f in range(FLOORS_NUMBER):
                if available_info[parking][f] == True:
                    print("floor changed")
                    return(parking,f)
                    parking_found = True
                    break

        #parking_found=falseなら他の駐車場も含めた満車判定
        #駐車先の優先順位はROTARY>CENTER>WESTなので0→2の繰り返し処理でOK
        if parking_found != True:
            for p in range(PARKINGS_NUMBER):
                for f in range(FLOORS_NUMBER):
                    if available_info[p][f]==True:
                        print("parking changed")
                        return(p,f)
                        parking_found = True
                        break
                else:
                    continue
                break

        #すべての駐車場が埋まっていたとき
        if parking_found != True:
            print("ALL parking FULL")
            return(PARKINGS_NUMBER, FLOORS_NUMBER) #存在しない駐車場とフロア




    def missrate_cal(self):
        #割り当てミス率の計算・表示
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



    def parking_assignment(self, sock, need_parking):
        #ユーザに対する駐車場割り当て処理
        self.parking_check(self.going+self.veh, self.available_on_system)#まず状況のチェック
        #[str,int]
        [parking, floor]=self.parking_select(parking_dict[need_parking],0,self.available_on_system)#とりあえず1階から順に見るのでfloor=0
        self.going[parking][floor] += 1 #割り当てられた場所に向かっている車の数＋1
        
        sock.send(PARKINGS_NAME[parking]+str(floor))#建物名と階数を結合して送信（例：ROTARY1）
        print(need_parking+' resulted in '+PARKINGS_NAME[parking]+str(floor))#結果表示　例：ROTARY resulted in ROTARY1
        for i in range(3):#各駐車場の状況表示
            print(str(i)+"|going:"+self.going[i]+"veh_counted:"+self.veh_counted[i]+"veh:"+self.veh[i])
        self.assigned_driver+=1
        self.missrate_cal()#ミス率計算・表示


    def user_or_not(self, parking, floor):
        #駐車場から出てきた車がuserかそうでないかを決定する
        #出て来た奴がアプリユーザである確率　= veh_counted / veh
        User_parking_rate = 100 * self.veh_counted[parking][floor]/self.veh[parking][floor]
        leave_user_check = randint(1,100)
        if leave_user_check <= User_parking_rate:
            print(PARKINGS_NAME[parking]+'_leavecheck: User')
            self.veh_counted[floor]-=1
        else:
            print(PARKINGS_NAME[parking]+'_leavecheck: NotUser')

        

    def deal_msg(self, sock, msg, readfds):
        #アプリ側から送られてくる各種メッセージへの対応

        if 'ROTARY' in msg: parking_id=0
        elif 'CENTER' in msg: parking_id=1
        elif 'WEST' in msg: parking_id=2

        global floor_id #なぜかreferenced before assignmentって怒られるので…
        if 'floor1' in msg: floor_id = 0
        elif 'floor2' in msg: floor_id = 1
        elif 'floor3' in msg: floor_id = 2

        if len(msg) == 0:
            sock.close()
            readfds.remove(sock)

        elif msg == 'allveh_count+1':
            self.allveh_count+=1

        elif 'step' in msg:
            step = msg[4:6]#ステップ数をmsg[4:6]で参照
            timesum = float(msg[22:])#timesum(各ステップごとの、駐車にかかった時間の合計)をmsg[22:]で参照
            print("timesum is "+msg[22:])#確認用

            #ステップごとのシミュレート結果表示
            print('!!!!!!!!-------------step_'+step+'_finish---------------!!!!!!!!!!')
            if self.assigned_driver == 0:
                print('Nobody  assigned')
            else:
                print('assign_MISS rate is '+str(self.fullchangecount/self.assigned_driver))
            print('allveh_count is '+str(self.allveh_count))
            print('ROTARY_parking_rate is '+str(sum(self.veh[0])/(CAPACITY*3)))
            print('CENTER_parking_rate is '+str(sum(self.veh[1])/(CAPACITY*3)))
            print('WEST_parking_rate is '+str(sum(self.veh[2])/(CAPACITY*3)))
            print('whole_parking_rate is '+str((sum(self.veh[0])+sum(self.veh[1])+sum(self.veh[2]))/(CAPACITY*9)))
            print('avarage_parking_time is '+str(timesum/self.assigned_driver))
            print('----------------------------------------------------------------')
            self.fullchangecount = 0
            self.assigned_driver = 0
            self.allveh_count = 0

        # 駐車要請に対する動作
        elif 'GOTO' in msg:
            # 本当は目的地ー駐車場ー現在地の距離を計算して最適な駐車場を提案したい
            # しかしここは、「一旦要請を蓄積してから、目的地に近づいた段階で割り当て」を実装しないとぶっちゃけ意味ない
            if msg == 'GOTOparking_1': best_parking = "ROTARY"
            elif msg == 'GOTOparking_2': best_parking = "CENTER"
            elif msg == 'GOTOparking_3': best_parking = "WEST"
            elif msg == 'GOTOparking_4': best_parking = "ROTARY"
            elif msg == 'GOTOparking_5': best_parking = "CENTER"
            self.parking_assignment(sock, best_parking)

        # 駐車場管理
  
        elif 'reach' in msg: #userのreach
                self.veh_counted[parking_id][floor_id]+=1
                self.veh[parking_id][floor_id]+=1
                self.going[parking_id][floor_id]-=1
                self.parking_allcheck()#状況更新
                print(msg)

        elif 'leave' in msg:
            #leave時にfloor_id持ってない問題解決のための苦肉の策
            #1階から順に退出していくことになっている（リアルじゃないポイント）
            if self.veh[parking_id][0] > 0: floor_id = 0
            elif self.veh[parking_id][1] > 0: floor_id = 1
            elif self.veh[parking_id][2] > 0: floor_id = 2
            else:
                #車が一切止まってない時に出ていく = もともと止まってた車のぶん、カウントしない
                floor_id = FLOORS_NUMBER
                
            if floor_id != FLOORS_NUMBER:
                self.user_or_not(parking_id,floor_id)#出てくる車がユーザであるか否か、ユーザならveh_countedを-1
                self.veh[parking_id][floor_id]-=1 #駐車場から1台出るので
            self.parking_allcheck() #状況更新
            print(msg)

        elif 'fullcheck' in msg:
            # 満車確認、満車対応 受信：ユーザか否か、目的地はどこか 送信：どの駐車場の何階に向かうか(paring,floor)
            self.parking_allcheck() # 状況確認・更新

            if 'NotUser' in msg:
                #COPメモ：notuserレイヤーのアクティベートを引数変えて呼ぶ
                #非ユーザのfullcheck
                #センサのある階にいく場合、veh_counted+1
                with notuser_layer.NotUser(self.veh[parking_id], self.veh_counted[parking_id], CAPACITY, ROTARY_sensor):
                    floor = l.floor_select()
                    if floor == 4:#満車の時
                        if parking_id == 0:#ROTARYに来ていた場合
                            #ROTARYがいっぱいのときに向かう駐車場は，CENTERとWESTで半々に（ROTARY-CENTERで無限に行き来するのは変）
                            instant_decide = randint(1,2)
                            if instant_decide == 1:
                                parking_id = 1 #CENTER
                                print('NotUser changed ROTARY to CENTER')
                            elif instant_decide == 2:
                                parking_id = 2 #WEST
                                print('NotUser changed ROTARY to WEST')
                        else: #ROTARY以外の場合
                            print('NotUser changed '+PARKINGS_NAME[parking_id]+' to ROTARY')
                            parking_id = 0 #ROTARY

                print('Notuser_fullcheck: '+'GOTO_'+PARKINGS_NAME[parking_id]+str(floor))
                sock.send('GOTO_'+PARKINGS_NAME[parking_id]+str(floor))#e.g. GOTO_ROTARY1

            #以下、ユーザのfullcheck
            else:
                requested_p = parking_id
                requested_f = int(msg[-1:])-1 #floorは自然数で受け渡しする(floor=1,2,3）ため、-1してfloor_idと一致させる
                requested = [requested_p,requested_f] #[int,int]

                [result_p, result_f] = self.parking_select(requested_p,requested_f,self.available_on_system) #ユーザなのでonsystem
                result = [result_p, result_f]

                if requested == result: #リクエスト通りに割り当て完了
                    sock.send('OK')

                else: #リクエスト通りに割り当てできなかった→フロアのみチェンジor駐車場ごとチェンジ
                    self.going[requested_p][requested_f] -=1 #予定していたところに向かうのをやめる

                    if available_on_system[requested_p][requested_f] == True: #満車を把握できていなかったら
                        self.veh_counted[requested_p][requested_f] +=1 #埋まっていたことがわかったので+1
                        #ここ、availableをFalseに変える方が自然だが、センサーの評価のため、あくまで1台分の加算のみ行っている

                    if requested_p == result_p: #駐車場は変更していない→フロアのみチェンジ
                        sock.send('changefloor_to_'+str(result_f+1))
                        self.going[result_p][result_f] +=1
                    else: #駐車場が違う→駐車場ごとチェンジ
                        sock.send('changeparking_to_'+PARKINGS_NAME[result_p]+str(result_f))
                        self.going[result_p][result_f] +=1
                        if result_p != PARKINGS_NUMBER: #割り当て結果がGO_HOMEじゃなければ
                            assigned_driver +=1 #再度駐車場を割り当てたことになるので+1

                    self.fullchangecount+=1 #割り当てミスカウント+1
                    self.missrate_cal()
                    



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
    l = layerselect.LayerSelect()
    ParkingServer('127.0.0.1', 4000).run()
