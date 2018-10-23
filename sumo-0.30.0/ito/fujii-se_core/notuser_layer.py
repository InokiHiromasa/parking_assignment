# -*- coding: utf-8 -*-

##notuser_layer##

from context import layers
import layerselect



class NotUser(layers.Layer):
    def __init__(self, veh_id, vehcountid, capacity, sensor):
        self.veh_id = veh_id
        self.vehcountid = vehcountid
        self.capacity = capacity
        self.sensor = sensor

class LayerSelect(NotUser, layerselect.LayerSelect):

    @layers.instead
    # def floor_select(self, veh_id, capacity, sensor, vehcountid, context):
    def floor_select(self, context):
        veh_id = context.layer.veh_id
        vehcountid = context.layer.vehcountid
        capacity = context.layer.capacity
        sensor = context.layer.sensor

        floor = 1
        veh_id[0]+=1
        if veh_id[0] > capacity:
            floor = 2
            veh_id[0]-=1
            veh_id[1]+=1
            if veh_id[1] > capacity:
                floor = 3
                veh_id[1]-=1
                veh_id[2]+=1
                if veh_id[2] > capacity:
                    floor = 4
                    veh_id[2]-=1
                    #満車
        print('SENSOR_is_'+sensor)
        
        
        if str(floor) in sensor:
            #センサのある階に向かう
            #システムが把握できるのでvehcountidが加算
            #nonsensor_layer_activate
            vehcountid[floor-1]+=1
            print('<< SENSOR_floor >>')
        

        return floor