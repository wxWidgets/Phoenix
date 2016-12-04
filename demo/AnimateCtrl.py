#!/usr/bin/env python

import wx
from wx.adv import Animation, AnimationCtrl
from Main import opj

GIFNames = [
    'bitmaps/AG00178_.gif',
    'bitmaps/BD13656_.gif',
    'bitmaps/AG00185_.gif',
    'bitmaps/AG00039_.gif',
    'bitmaps/AG00183_.gif',
    'bitmaps/AG00028_.gif',
    ]

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.FlexGridSizer(cols=3, hgap=5, vgap=5)
        for name in GIFNames:
            ani = Animation(opj(name))
            ctrl = AnimationCtrl(self, -1, ani)
            ctrl.SetBackgroundColour(self.GetBackgroundColour())
            ctrl.Play()
            sizer.Add(ctrl, 0, wx.ALL, 10)

        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.EXPAND | wx.ALL, 20)
        self.SetSizer(border)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.adv.AnimationCtrl</center></h2>

wx.adv.AnimationCtrl is like a wx.StaticBitmap but is able to
display an animation by extracting frames from a multi-image GIF file.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

