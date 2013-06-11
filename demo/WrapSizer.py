
import wx
from wx.lib.buttons import GenButton

import random

#----------------------------------------------------------------------

class WrapSizerTest(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        # Make a title area and sizer for the upper part of the panel
        pnl = wx.Panel(self)
        stx = wx.StaticText(pnl, -1, "wx.WrapSizer Layout")
        stx.SetFont(wx.FFont(28, wx.SWISS))
        sln = wx.StaticLine(pnl)
        upper = wx.BoxSizer(wx.VERTICAL)
        upper.Add(stx, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.TOP, 8)
        upper.Add(sln, 0, wx.EXPAND|wx.ALL, 8)

        # In the lower part of the panel we'll put a bunch of buttons
        # in a WrapSizer
        def _makeButtons(words):
            sizer = wx.WrapSizer()
            for word in words:
                btn = GenButton(pnl, -1, word, style=wx.BU_EXACTFIT)
                sizer.Add(btn, 0, wx.ALL, 4)
                
                # Add a little color to make it interesting
                r = random.randint(128, 255)
                g = random.randint(128, 255)
                b = random.randint(128, 255)
                btn.SetBackgroundColour(wx.Colour(r,g,b))
                btn.Refresh()
                
            return sizer
        
        lower1 = _makeButtons(sampleText.split())
        lower2 = _makeButtons("Try resizing this Frame to see how it works.".split())
        
        pnl.Sizer = wx.BoxSizer(wx.VERTICAL)
        pnl.Sizer.Add(upper, 0, wx.EXPAND)
        pnl.Sizer.Add(lower1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 8)
        pnl.Sizer.Add((16,16))
        pnl.Sizer.Add(lower2, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 8)

        
#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Demonstrate wx.WrapSizer", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        win = WrapSizerTest(self, -1, "wx.WrapSizer Demo", size=(640, 480))
        win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------

sampleText = """\
The wx.WrapSizer implements a commonly requested layout mechanism where
however many items will fit on a "line" are positioned next to each other, and
then the location of the next item in the sizer is on the next logical line of
the parent's layout. """

overview = """<html><body>
<h2><center>WrapSizer</center></h2>
""" + \
sampleText + \
"""
</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

