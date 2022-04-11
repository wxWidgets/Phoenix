#---------------------------------------------------------------------------
# Name:        newevent.py
# Purpose:     Easy generation of new events classes and binder objects.
#
# Author:      Miki Tebeka <miki.tebeka@gmail.com>
#
# Created:     18-Sept-2006
# Copyright:   (c) 2006-2020 by Total Control Software
# Licence:     wxWindows license
#
# Tags:        phoenix-port, documented
#---------------------------------------------------------------------------

"""
Easy generation of new events classes and binder objects.


Description
===========

This module contains two functions which makes the generation of custom wxPython events
particularly easy.


Usage
=====

Sample usage::

    import wx
    import time
    import threading

    import wx.lib.newevent as NE

    MooEvent, EVT_MOO = NE.NewEvent()
    GooEvent, EVT_GOO = NE.NewCommandEvent()

    DELAY = 0.7

    def evt_thr(win):
        time.sleep(DELAY)
        wx.PostEvent(win, MooEvent(moo=1))

    def cmd_thr(win, id):
        time.sleep(DELAY)
        wx.PostEvent(win, GooEvent(id, goo=id))

    ID_CMD1 = wx.NewIdRef()
    ID_CMD2 = wx.NewIdRef()

    class Frame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, -1, "MOO")
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.Bind(EVT_MOO, self.on_moo)
            b = wx.Button(self, -1, "Generate MOO")
            sizer.Add(b, 1, wx.EXPAND)
            b.Bind(wx.EVT_BUTTON, self.on_evt_click)
            b = wx.Button(self, ID_CMD1, "Generate GOO with %d" % ID_CMD1)
            sizer.Add(b, 1, wx.EXPAND)
            b.Bind(wx.EVT_BUTTON, self.on_cmd_click)
            b = wx.Button(self, ID_CMD2, "Generate GOO with %d" % ID_CMD2)
            sizer.Add(b, 1, wx.EXPAND)
            b.Bind(wx.EVT_BUTTON, self.on_cmd_click)

            self.Bind(EVT_GOO, self.on_cmd1, id=ID_CMD1)
            self.Bind(EVT_GOO, self.on_cmd2, id=ID_CMD2)

            self.SetSizer(sizer)
            self.SetAutoLayout(True)
            sizer.Fit(self)

        def on_evt_click(self, e):
            t = threading.Thread(target=evt_thr, args=(self, ))
            t.setDaemon(True)
            t.start()

        def on_cmd_click(self, e):
            t = threading.Thread(target=cmd_thr, args=(self, e.GetId()))
            t.setDaemon(True)
            t.start()

        def show(self, msg, title):
            dlg = wx.MessageDialog(self, msg, title, wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

        def on_moo(self, e):
            self.show("MOO = %s" % e.moo, "Got Moo")

        def on_cmd1(self, e):
            self.show("goo = %s" % e.goo, "Got Goo (cmd1)")

        def on_cmd2(self, e):
            self.show("goo = %s" % e.goo, "Got Goo (cmd2)")


    app = wx.App(0)
    f = Frame()
    f.Show(True)
    app.MainLoop()

"""

__author__ = "Miki Tebeka <miki.tebeka@gmail.com>"

import wx

#---------------------------------------------------------------------------

def NewEvent():
    """
    Generates a new `(event, binder)` tuple.

    ::

        MooEvent, EVT_MOO = NewEvent()

    """

    evttype = wx.NewEventType()

    class _Event(wx.PyEvent):
        def __init__(self, **kw):
            wx.PyEvent.__init__(self)
            self.SetEventType(evttype)
            self._getAttrDict().update(kw)

    return _Event, wx.PyEventBinder(evttype)


def NewCommandEvent():
    """
    Generates a new `(command_event, binder)` tuple.

    ::

        MooCmdEvent, EVT_MOO = NewCommandEvent()

    """

    evttype = wx.NewEventType()

    class _Event(wx.PyCommandEvent):
        def __init__(self, id, **kw):
            wx.PyCommandEvent.__init__(self, evttype, id)
            self._getAttrDict().update(kw)

    return _Event, wx.PyEventBinder(evttype, 1)


#---------------------------------------------------------------------------

def _test():
    """A little smoke test"""
    import time
    import threading

    MooEvent, EVT_MOO = NewEvent()
    GooEvent, EVT_GOO = NewCommandEvent()

    DELAY = 0.7

    def evt_thr(win):
        time.sleep(DELAY)
        wx.PostEvent(win, MooEvent(moo=1))

    def cmd_thr(win, id):
        time.sleep(DELAY)
        wx.PostEvent(win, GooEvent(id, goo=id))

    ID_CMD1 = wx.NewIdRef()
    ID_CMD2 = wx.NewIdRef()

    class Frame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, -1, "MOO")
            sizer = wx.BoxSizer(wx.VERTICAL)
            self.Bind(EVT_MOO, self.on_moo)
            b = wx.Button(self, -1, "Generate MOO")
            sizer.Add(b, 1, wx.EXPAND)
            b.Bind(wx.EVT_BUTTON, self.on_evt_click)
            b = wx.Button(self, ID_CMD1, "Generate GOO with %d" % ID_CMD1)
            sizer.Add(b, 1, wx.EXPAND)
            b.Bind(wx.EVT_BUTTON, self.on_cmd_click)
            b = wx.Button(self, ID_CMD2, "Generate GOO with %d" % ID_CMD2)
            sizer.Add(b, 1, wx.EXPAND)
            b.Bind(wx.EVT_BUTTON, self.on_cmd_click)

            self.Bind(EVT_GOO, self.on_cmd1, id=ID_CMD1)
            self.Bind(EVT_GOO, self.on_cmd2, id=ID_CMD2)

            self.SetSizer(sizer)
            self.SetAutoLayout(True)
            sizer.Fit(self)

        def on_evt_click(self, e):
            t = threading.Thread(target=evt_thr, args=(self, ))
            t.setDaemon(True)
            t.start()

        def on_cmd_click(self, e):
            t = threading.Thread(target=cmd_thr, args=(self, e.GetId()))
            t.setDaemon(True)
            t.start()

        def show(self, msg, title):
            dlg = wx.MessageDialog(self, msg, title, wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

        def on_moo(self, e):
            self.show("MOO = %s" % e.moo, "Got Moo")

        def on_cmd1(self, e):
            self.show("goo = %s" % e.goo, "Got Goo (cmd1)")

        def on_cmd2(self, e):
            self.show("goo = %s" % e.goo, "Got Goo (cmd2)")


    app = wx.App(0)
    f = Frame()
    f.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    _test()
