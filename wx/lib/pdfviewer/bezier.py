# Name:         bezier.py 
# Package:      wx.lib.pdfviewer
#
# Purpose:      Compute Bezier curves for PDF rendered using wx.DC
#               Adapted from the original source code, see below.
#
# Author:       David Hughes     dfh@forestfield.co.uk
# Copyright:    Forestfield Software Ltd
# Licence:      Public domain

# History:      Created 17 Jun 2009
#
# Tags:         phoenix-port, documented
#
#----------------------------------------------------------------------------
"""
This module is used to compute Bezier curves for PDF rendering.
"""

import wx
from vec2d import *
 
def calculate_bezier(p, steps = 30):
    """
    Calculate a bezier curve from 4 control points and return a 
    list of the resulting points.
    Depends on the 2d vector class from http://www.pygame.org/wiki/2DVectorClass
     
    2007 Victor Blomqvist
    Released to the Public Domain    
    The function uses the forward differencing algorithm described at 
    http://www.niksula.cs.hut.fi/~hkankaan/Homepages/bezierfast.html
    """
    
    t = 1.0 / steps
    temp = t*t
    
    f = p[0]
    fd = 3 * (p[1] - p[0]) * t
    fdd_per_2 = 3 * (p[0] - 2 * p[1] + p[2]) * temp
    fddd_per_2 = 3 * (3 * (p[1] - p[2]) + p[3] - p[0]) * temp * t
    
    fddd = fddd_per_2 + fddd_per_2
    fdd = fdd_per_2 + fdd_per_2
    fddd_per_6 = fddd_per_2 * (1.0 / 3)
    
    points = []
    for x in range(steps):
        points.append(f)
        f = f + fd + fdd_per_2 + fddd_per_6
        fd = fd + fdd + fddd_per_2
        fdd = fdd + fddd
        fdd_per_2 = fdd_per_2 + fddd_per_2
    points.append(f)
    return points

def compute_points(controlpoints, nsteps=30):
    """
    Input 4 control points as :class:`RealPoint` and convert to vec2d instances.
    compute the nsteps points on the resulting curve and return them
    as a list of :class:`Point`
    """
    controlvectors = []
    for p in controlpoints:
        controlvectors.append(vec2d(p.x, p.y))
    pointvectors = calculate_bezier(controlvectors, nsteps)
    curvepoints = []
    for v in pointvectors:
        curvepoints.append(wx.Point(v[0], v[1]))
    return curvepoints    

