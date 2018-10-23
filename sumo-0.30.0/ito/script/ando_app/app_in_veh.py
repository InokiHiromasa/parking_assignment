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
#満車の時のchange_destinationのために
from domain.model.mobileagent import MobileAgent

#notUserが各駐車場にreachした際に使う
road_list = ['-161947715#2', '84515126', '-223785629']

# for fullcheck
ROTARY_enter = '84515125#10'
CENTER_enter = '84515125#6'
WEST_enter = '-84515125#22'
enter_list=[ROTARY_enter, CENTER_enter, WEST_enter]

#notUserの割合決定
Notrecommend_rate = 70


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
        self.floor = 0
        self.AppUser = None
        self._fullchecked = False
        self.fullcheck_res = None
        self.changedDest = None
        self.destination = None
        self.nowstep = 0
        self.ROTARY_change = False

    def event_handler(self, info):
        # アプリの起動条件
        # このタイミングもっと早くする
        # 一定割合の人にはアプリを適用せずに適当に駐車場に向かってもらうようにする
        # 適用しなかった人にはそれとわかる色を設定(灰色)
        # できるだけ早い段階でeventhandlerすれば，ミス率が上がる（現実に近づく）と思う
        if not self._used and info.road == '191353111#1':
            #伊都キャンに訪れる車の総量をサーバ側で管理
            #時間帯による車の流量の確認に使う
            super(AppInVeh, self).send_information('allveh_count+1')
            
            notrecommend = randint(1,100)
            print('--------------------------------')
            if notrecommend <= Notrecommend_rate:#30%でアプリを起動させない（リコメンドされない）   
                print('not recommended')
                self.AppUser = False
                return 'NotUser'
                
            if notrecommend > Notrecommend_rate:
                print('recommended')
                self.AppUser = True
                return 'User'

                
        else:
            return False
###################################
    def step_check(self):
        step = manager.get_step()
        if self.nowstep != 7 and step == 3600:
            super(AppInVeh, self).send_information('step_7_finish')
            self.nowstep = 7
        if self.nowstep != 8 and step == 7200:
            super(AppInVeh, self).send_information('step_8_finish')
            self.nowstep = 8
        if self.nowstep != 9 and step == 10800:
            super(AppInVeh, self).send_information('step_9_finish')
            self.nowstep = 9
        if self.nowstep != 10 and step == 14400:
            super(AppInVeh, self).send_information('step_10_finish')
            self.nowstep = 10
        if self.nowstep != 11 and step == 18000:
            super(AppInVeh, self).send_information('step_11_finish')
            self.nowstep = 11
        if self.nowstep != 12 and step == 21600:
            super(AppInVeh, self).send_information('step_12_finish')
            self.nowstep = 12
        if self.nowstep != 13 and step == 25200:
            super(AppInVeh, self).send_information('step_13_finish')
            self.nowstep = 13
        if self.nowstep != 14 and step == 28800:
            super(AppInVeh, self).send_information('step_14_finish')
            self.nowstep = 14
        if self.nowstep != 15 and step == 32400:
            super(AppInVeh, self).send_information('step_15_finish')
            self.nowstep = 15
        if self.nowstep != 16 and step == 36000:
            super(AppInVeh, self).send_information('step_16_finish')
            self.nowstep = 16
        if self.nowstep != 17 and step == 39600:
            super(AppInVeh, self).send_information('step_17_finish')
            self.nowstep = 17
        if self.nowstep != 18 and step == 43200:
            super(AppInVeh, self).send_information('step_18_finish')
            self.nowstep = 18


    
    def vehcount(self,info):
        # reachは、アプリユーザのみカウントしたい

        # id1 parking vehcount
        # ROTARYから駐車場チェンジしたときにreach扱いにしないでほしい
        if not self._counted and self.AppUser and not self.ROTARY_change and info.road  == '-161947715#2':
            print(self.AppUser)
            print('to floor'+str(self.floor))
            super(AppInVeh, self).send_information('reach_ROTARY_floor'+str(self.floor))
            self._counted = True


        #leave時もおなじく，駐車場チェンジした車のleaveをカウントするな
        elif not self._counted and not self.ROTARY_change and info.road == '161947715#2':
            print('from floor'+str(self.floor))
            #reachと同じようにしてるけど，実際はすべてself.floorは0になっている
            #だから合わせて送信しても意味ないんだけどまあ直すのめんどくさいしこのままで
            #0になってしまうことに対して解決策が今のところないので
            #サーバ側で適当なfloorから出てきてることにしてる
            super(AppInVeh, self).send_information('leave_ROTARY_floor'+str(self.floor))
            self._counted = True

        # id2 parking vehcount
        if not self._counted and self.AppUser and info.road == '84515126':
            print(self.AppUser)
            print('to floor'+str(self.floor))
            super(AppInVeh, self).send_information('reach_CENTER_floor'+str(self.floor))
            self._counted = True

        elif not self._counted and info.road == '-84515126':
            print('from floor'+str(self.floor))
            
            super(AppInVeh, self).send_information('leave_CENTER_floor'+str(self.floor))
            self._counted = True

        # id3 parking vehcount
        if not self._counted and self.AppUser and info.road == '-223785629':
            print(self.AppUser)
            print('to floor'+str(self.floor))
            super(AppInVeh, self).send_information('reach_WEST_floor'+str(self.floor))
            self._counted = True

        elif not self._counted and info.road == '223785629':
            print('from floor'+str(self.floor))
            super(AppInVeh, self).send_information('leave_WEST_floor'+str(self.floor))
            self._counted = True


    ################################

    def fullcheck_handler(self, info):
        if not self._fullchecked and info.road == ROTARY_enter and self.destination == 'ROTARY':
            return True

        elif not self._fullchecked and info.road == CENTER_enter and self.destination == 'CENTER':
            return True

        elif not self._fullchecked and info.road == WEST_enter and self.destination == 'WEST':
            return True

        else:
            return False


    def fullcheck(self, info):
        #入力info, 出力はなし（最後にchangeDestinationする）
        #駐車場に入るまえに満車確認を行い，満車だった場合ほかのところにいく
        #入力info, 出力self._resに新目的地
        #ユーザの場合，まず自分が割り当てられた階が空いているかの確認をし，空いていなかったら他の階の確認，それでもダメなら再度割り当て
        #非ユーザの場合，１階から順に見て，空いているところに止める．空いてなかったら一番近いところにとめる
        if info.road == ROTARY_enter:
            parkingname = 'ROTARY'
        elif info.road == CENTER_enter:
            parkingname = 'CENTER'
        elif info.road == WEST_enter:
            parkingname = 'WEST'
        else:
            print('enterじゃないのにfullcheckするんじゃねえぞhandler')

        ##ここのif文をスルーしてこのあとのところだけ実行されてしまっている？？？？？
        ##parkingname referenced before assignment って言われちゃうのは多分そういうこと
        ##でもそんなことありえますか？？？？？？？
        ##現在地がenterじゃないのにfullcheckが呼ばれてしまっている？？？

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        if self.AppUser == True:
            #ユーザに対する処理
            #まず予定されていたところが本当に空いているか確認
            with closing(sock):
                sock.connect( (self._addr, self._port) )
                sock.send('fullcheck_'+parkingname+str(self.floor))#e.g. fullcheck_ROTARY1
                self.fullcheck_res = sock.recv(1024)

            print(self.fullcheck_res)

            #if 'changefloor' in self.fullcheck_res:
            #よく考えたらこれchangeparkingでもやることだったわ
            if 'change' in self.fullcheck_res:
                if '1' in self.fullcheck_res:
                    self.floor = 1
                elif '2' in self.fullcheck_res:
                    self.floor = 2
                elif '3' in self.fullcheck_res:
                    self.floor = 3

                if 'changeparking' in self.fullcheck_res:
                    if parkingname == 'ROTARY':
                        #ROTARYは駐車場チェンジしてもreachしちゃうからよくない
                        self.ROTARY_change = True
                    if 'ROTARY' in self.fullcheck_res:
                        lat = 33.59592
                        lng = 130.21734
                    elif 'CENTER' in self.fullcheck_res:
                        lat = 33.598421
                        lng = 130.221593
                    elif 'WEST' in self.fullcheck_res:
                        lat = 33.598048
                        lng = 130.211299
                    
                    elif 'GO_HOME' in self.fullcheck_res:
                        #どこも埋まってた場合…消えてもらう
                        #マップの左上の座標
                        lat = 33.621855
                        lng = 130.187091

                    self.changedDest, _, _ = traci.simulation.convertRoad(lng, lat, True)
                #MobileAgent._object.change_destination(self._changedDest)

            #空いていたらなにもせずスルー、空いていなかったら他の階を確認
            #他の階が空いていたらself.floorを変更して終わり、空いていなかったら他の駐車場
            #他の駐車場、どこに行くかは、再び駐車場割り当て（現在の駐車場抜きで）を行うか、もう僕が決めてしまうか



        elif self.AppUser == False:
            #非ユーザに対する処理
            #notuser_layer activate
            with closing(sock):
                sock.connect( (self._addr, self._port) )
                sock.send('fullcheck_'+ parkingname + '_NotUser' )#e.g. fullcheck_ROTARY_NotUser
                self.fullcheck_res = sock.recv(1024)

            print(self.fullcheck_res)

            if '1' in self.fullcheck_res:
                self.floor = 1
            elif '2' in self.fullcheck_res:
                self.floor = 2
            elif '3' in self.fullcheck_res:
                self.floor = 3
            elif '4' in self.fullcheck_res:
                #行き先を変更された
                #つぎの行き先についたときにまた階選択するのでいまはなにもしなくていい
                #ROTARY_changeにだけ気をつけよう
                if parkingname == 'ROTARY':
                    self.ROTARY_change = True

            if 'ROTARY' in self.fullcheck_res:
                lat = 33.59592
                lng = 130.21734
            elif 'CENTER' in self.fullcheck_res:
                lat = 33.598421
                lng = 130.221593
            elif 'WEST' in self.fullcheck_res:
                lat = 33.598048
                lng = 130.211299

            self.changedDest, _, _ = traci.simulation.convertRoad(lng, lat, True)
            

        self._fullchecked = True


        
        #MobileAgent._object.change_destination(self._changedDest)
        #１階から順に空いているかチェック
        #あいていたらそこにとめる
        #空いていなかったら一番近い駐車場に向かってもらう




    def notuser_run(self):
        # 適当な駐車場に向かってもらう
        # 階はサーバ側で決定（できる限り下の階に止めようとする）
        id = randint(1,5)
        self.floor = 1
        if id == 1 or id == 4:
            lat = 33.59592
            lng = 130.21734
            self.destination = 'ROTARY'
            print('NOTuser_ROTARY')
        elif id == 2 or id == 5:
            lat = 33.598421
            lng = 130.221593
            self.destination = 'CENTER'
            print('NOTuser_CENTER')
        elif id == 3:
            lat = 33.598048
            lng = 130.211299
            self.destination = 'WEST'
            print('NOTuser_WEST')


        self._res, _, _ = traci.simulation.convertRoad(lng, lat, True)
        print('res:', self._res)
        self._used = True



    def run(self, x_position, y_position):
        # 目的地設定，ゴリ押し
        id = randint(1, 5)
        
        msg = 'GOTOparking_'+str(id)

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
        # いま，位置による割り当てをいったんやめているので，x_pleaseもこず，1回目のrecvから直接以下の文に進む

        
        print('res_parking is ...')
        if 'ROTARY' in self.res_message:
            lat = 33.59592
            lng = 130.21734
            self.destination = 'ROTARY'
        elif 'CENTER' in self.res_message:
            lat = 33.598421
            lng = 130.221593
            self.destination = 'CENTER'
        elif 'WEST' in self.res_message:
            lat = 33.598048
            lng = 130.211299
            self.destination = 'WEST'
        
        elif self.res_message == 'GO_HOME':
            # どこに向かわせればいいのかよくわからん…
            # とりあえず消えろ
            lat = 33.621855
            lng = 130.187091
            #マップの左上
            """
            randamgo = randint(1,3)
            if randamgo == 1:
                lat = 33.59592
                lng = 130.21734
                self.destination = 'ROTARY'
                self.floor = 1
            elif randamgo == 2:
                lat = 33.598421
                lng = 130.221593
                self.destination = 'CENTER'
                self.floor = 1
            elif randamgo == 3:
                lat = 33.598048
                lng = 130.211299
                self.destination = 'WEST'
                self.floor = 1
            """
        



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
