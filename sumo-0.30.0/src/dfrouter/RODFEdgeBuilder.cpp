/****************************************************************************/
/// @file    RODFEdgeBuilder.cpp
/// @author  Daniel Krajzewicz
/// @author  Eric Nicolay
/// @author  Michael Behrisch
/// @author  Yun-Pang Floetteroed
/// @date    Thu, 16.03.2006
/// @version $Id: RODFEdgeBuilder.cpp 23529 2017-03-18 10:22:36Z behrisch $
///
// Interface for building instances of dfrouter-edges
/****************************************************************************/
// SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/
// Copyright (C) 2006-2017 DLR (http://www.dlr.de/) and contributors
/****************************************************************************/
//
//   This file is part of SUMO.
//   SUMO is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
/****************************************************************************/

// ===========================================================================
// included modules
// ===========================================================================
#ifdef _MSC_VER
#include <windows_config.h>
#else
#include <config.h>
#endif

#include "RODFEdgeBuilder.h"
#include "RODFEdge.h"


// ===========================================================================
// method definitions
// ===========================================================================
RODFEdgeBuilder::RODFEdgeBuilder() {}


RODFEdgeBuilder::~RODFEdgeBuilder() {}


ROEdge*
RODFEdgeBuilder::buildEdge(const std::string& name, RONode* from, RONode* to, const int priority) {
    return new RODFEdge(name, from, to, getNextIndex(), priority);
}


/****************************************************************************/

