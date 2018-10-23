# -*- coding: utf-8 -*-

from context import layers

class LayerSelect(object):
    def floor_select(self, countid, vehnumber, capacity, sensor):
        # sensorはnotuserのときにつかう
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

    """

    def NotUser_floor_select(self, veh_id, capacity, sensor, vehcountid):
        # notuser_layer activate
        with notuser_layer.NotUser():
            floor = l.floor_select(veh_id, vehcountid, capacity)
            
            if str(floor) in sensor:
                #センサのある階に向かう
                #システムが把握できるのでvehcountidが加算
                #nonsensor_layer_activate
                vehcountid[floor-1]+=1
                print('<< SENSOR_floor >>')

            return floor
            
    """