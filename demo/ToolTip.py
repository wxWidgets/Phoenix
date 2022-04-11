#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.tt1 = wx.ToolTip("This is a wx.ToolTip.")
        self.tt2 = wx.ToolTip("This is\na multi-line\nToolTip.")
        self.tt3 = wx.ToolTip("Disabled ToolTips.")
        self.tt4 = wx.ToolTip("I will change this on the next line.")
        self.tt4.SetTip("ToolTip.GetTip(tt1) = %s" % self.tt1.GetTip())
        self.tt5 = wx.ToolTip("hmmm")
        self.tt6 = wx.ToolTip("wxPython (Phoenix)\n" * 10)
        self.tt7 = wx.ToolTip("Enable ToolTips.")
        self.tt8 = wx.ToolTip("bla bla bla " * 50)
        ## self.tt8.SetMaxWidth(-1)
        self.tt8.SetMaxWidth(0)

        wx.StaticText(self, -1, "Hover over a button to see a tool tip", (250,30))
        self.btn1 = wx.Button(self, -1, "Simple ToolTip", pos=(50, 30))
        self.btn1.SetToolTip(self.tt1)
        self.btn2 = wx.Button(self, -1, "Multi-Line ToolTip", pos=(50, 60))
        self.btn2.SetToolTip(self.tt2)
        self.btn3 = wx.Button(self, -1, "Disable ToolTips (if supported)", pos=(50, 90))
        self.btn3.SetToolTip(self.tt3)
        self.btn3.Bind(wx.EVT_BUTTON, self.OnDisableToolTips)
        self.btn4 = wx.Button(self, -1, "ToolTip.GetTip(self.tt1) = %s" % self.tt1.GetTip(), pos=(50, 120))
        self.btn4.SetToolTip(self.tt4)
        self.btn5 = wx.Button(self, -1, "ToolTip.GetWindow(self.tt2) = %s" % self.tt2.GetWindow(), pos=(50, 150))
        self.btn5.SetToolTip(self.tt5)
        self.tt5.SetTip("ToolTip.GetWindow(tt2) = %s" % self.tt2.GetWindow())
        self.btn6 = wx.Button(self, -1, "ToolTip.SetMaxWidth(-1)", pos=(50, 180))
        self.btn6.SetToolTip(self.tt6)
        self.btn7 = wx.Button(self, -1, "Enable ToolTips", pos=(50, 210))
        self.btn7.SetToolTip(self.tt7)
        self.btn7.Bind(wx.EVT_BUTTON, self.OnEnableToolTips)
        self.btn8 = wx.Button(self, -1, "ToolTip.SetMaxWidth(0)", pos=(50, 240))
        self.btn8.SetToolTip(self.tt8)
        self.btn9 = wx.Button(self, -1, "ToolTip set by string", pos=(50, 270))
        self.btn9.SetToolTip("ToolTip set without a wx.ToolTip")

    def OnDisableToolTips(self, event):
        wx.ToolTip.Enable(False)

    def OnEnableToolTips(self, event):
        wx.ToolTip.Enable(True)


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = """\
wx.ToolTip
"""


if __name__ == '__main__':
    import sys
    import os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
