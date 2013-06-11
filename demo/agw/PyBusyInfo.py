import wx

import os
import sys

import images

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import pybusyinfo as PBI
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.pybusyinfo as PBI

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test PyBusyInfo ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        
        evt.Skip()
        message = "Please wait 5 seconds, working..."
        busy = PBI.PyBusyInfo(message, parent=None, title="Really Busy",
                              icon=images.Smiles.GetBitmap())

        wx.Yield()
        
        for indx in xrange(5):
            wx.MilliSleep(1000)

        del busy
        
        
#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = PBI.__doc__


if __name__ == '__main__':
    import sys, os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
