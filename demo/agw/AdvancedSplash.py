import wx
import wx.lib.buttons

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

try:
    from agw import advancedsplash as AS
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.advancedsplash as AS

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test AdvancedSplash ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        pn = os.path.normpath(os.path.join(bitmapDir, "advancedsplash.png"))
        bitmap = wx.Bitmap(pn, wx.BITMAP_TYPE_PNG)
        shadow = wx.WHITE
        
        frame = AS.AdvancedSplash(self, bitmap=bitmap, timeout=5000,
                                  agwStyle=AS.AS_TIMEOUT |
                                  AS.AS_CENTER_ON_PARENT |
                                  AS.AS_SHADOW_BITMAP,
                                  shadowcolour=shadow)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = AS.__doc__


if __name__ == '__main__':
    import sys, os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
