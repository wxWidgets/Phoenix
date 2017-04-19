#----------------------------------------------------------------------------
# Name:         FCEvents.py
# Purpose:      A convenient place to put all event types and binders for
#               FloatCanvas, and to help avoid circular imports.
#
# Author:
#
# Created:
# Version:
# Date:
# Licence:
# Tags:         phoenix-port, unittest, documented, py3-port
#----------------------------------------------------------------------------
"""
This is where FloatCanvas defines its event types and binders.
"""

import wx


## Create all the mouse events -- this is for binding to Objects
EVT_FC_ENTER_WINDOW = wx.NewEventType()
EVT_FC_LEAVE_WINDOW = wx.NewEventType()
EVT_FC_LEFT_DOWN = wx.NewEventType()
EVT_FC_LEFT_UP  = wx.NewEventType()
EVT_FC_LEFT_DCLICK = wx.NewEventType()
EVT_FC_MIDDLE_DOWN = wx.NewEventType()
EVT_FC_MIDDLE_UP = wx.NewEventType()
EVT_FC_MIDDLE_DCLICK = wx.NewEventType()
EVT_FC_RIGHT_DOWN = wx.NewEventType()
EVT_FC_RIGHT_UP = wx.NewEventType()
EVT_FC_RIGHT_DCLICK = wx.NewEventType()
EVT_FC_MOTION = wx.NewEventType()
EVT_FC_MOUSEWHEEL = wx.NewEventType()
## these two are for the hit-test stuff, I never make them real Events
## fixme: could I use the PyEventBinder for the Object events too?
EVT_FC_ENTER_OBJECT = wx.NewEventType()
EVT_FC_LEAVE_OBJECT = wx.NewEventType()

##Create all mouse event binding objects -- for binding to the Canvas
EVT_LEFT_DOWN = wx.PyEventBinder(EVT_FC_LEFT_DOWN)
EVT_LEFT_UP = wx.PyEventBinder(EVT_FC_LEFT_UP)
EVT_LEFT_DCLICK = wx.PyEventBinder(EVT_FC_LEFT_DCLICK)
EVT_MIDDLE_DOWN = wx.PyEventBinder(EVT_FC_MIDDLE_DOWN)
EVT_MIDDLE_UP = wx.PyEventBinder(EVT_FC_MIDDLE_UP)
EVT_MIDDLE_DCLICK = wx.PyEventBinder(EVT_FC_MIDDLE_DCLICK)
EVT_RIGHT_DOWN = wx.PyEventBinder(EVT_FC_RIGHT_DOWN)
EVT_RIGHT_UP = wx.PyEventBinder(EVT_FC_RIGHT_UP)
EVT_RIGHT_DCLICK = wx.PyEventBinder(EVT_FC_RIGHT_DCLICK)
EVT_MOTION = wx.PyEventBinder(EVT_FC_MOTION)
EVT_ENTER_WINDOW = wx.PyEventBinder(EVT_FC_ENTER_WINDOW)
EVT_LEAVE_WINDOW = wx.PyEventBinder(EVT_FC_LEAVE_WINDOW)
EVT_MOUSEWHEEL = wx.PyEventBinder(EVT_FC_MOUSEWHEEL)
