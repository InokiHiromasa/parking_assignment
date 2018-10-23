function setSpeedDeviation(typeID, deviation)
%setSpeedDeviation Sets the maximum speed deviation for vehicles of this type.
%   setSpeedDeviation(TYPEID,DEVIATION) Sets the maximum speed deviation
%   for vehicles of this type.

%   Copyright 2016 Universidad Nacional de Colombia,
%   Politecnico Jaime Isaza Cadavid.
%   Authors: Andres Acosta, Jairo Espinosa, Jorge Espinosa.
%   $Id: setSpeedDeviation.m 31 2016-09-28 15:16:56Z afacostag $

import traci.constants
traci.sendDoubleCmd(constants.CMD_SET_VEHICLETYPE_VARIABLE, constants.VAR_SPEED_DEVIATION, typeID, deviation);