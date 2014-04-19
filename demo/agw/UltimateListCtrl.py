#!/usr/bin/env python

import wx
import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import ultimatelistctrl as ULC
except ImportError: # if it's not there locally, try the wxPython lib.
    from wx.lib.agw import ultimatelistctrl as ULC


#---------------------------------------------------------------------------

buttonDefs = {
    814 : ('UltimateReportDemo',   ' wx.LC_REPORT style '),
    815 : ('UltimateVirtualDemo',  ' wx.LC_VIRTUAL style '),
    816 : ('UltimateListIconDemo', ' wx.LC_ICON style '),
    817 : ('UltimateListListDemo', ' wx.LC_LIST style '),
    818 : ('Windows7Explorer_Contents', ' Windows 7 Explorer "Contents" style'),
    819 : ('MacLargeDemo', ' Torrent Style :-D')
    }


class ButtonPanel(wx.Panel):
    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent, -1)
        self.log = log

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add((20, 20))
        keys = list(buttonDefs.keys())
        keys.sort()

        for k in keys:
            text = buttonDefs[k][1]
            btn = wx.Button(self, k, text)
            box.Add(btn, 0, wx.ALIGN_CENTER|wx.ALL, 10)
            self.Bind(wx.EVT_BUTTON, self.OnButton, btn)

        self.SetSizer(box)
        box.Fit(self)


    def OnButton(self, event):

        event.Skip()

        wx.BeginBusyCursor()

        modName = buttonDefs[event.GetId()][0]
        module = __import__(modName)
        frame = module.TestFrame(None, self.log)

        wx.EndBusyCursor()

#---------------------------------------------------------------------------

def runTest(frame, nb, log):
    win = ButtonPanel(nb, log)
    return win

#---------------------------------------------------------------------------



overview = ULC.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

