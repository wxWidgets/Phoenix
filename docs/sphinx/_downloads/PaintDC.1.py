##Andrea Gavana
#!/usr/bin/env python

# This sample uses the random module to draw 100 random lines iinside
# a wx.Frame client area, as a demonstration of how to handle a wx.PaintDC

import wx
import random

class PaintFrame(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title)

        # Bind a "paint" event for the frame to the
        # "OnPaint" method
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Show()


    def OnPaint(self, event):

        dc = wx.PaintDC(self)
        w, h = self.GetClientSize()

        # Use a blue pen, for example...

        dc.SetPen(wx.Pen('BLUE'))

        # Remember the signature of wx.DC.DrawLine:
        # DrawLine(x1, y1, x2, y2)

        for i in range(100):
            x1 = random.randint(1, w-1)
            y1 = random.randint(1, h-1)
            x2 = random.randint(1, w-1)
            y2 = random.randint(1, h-1)
            dc.DrawLine(x1, y1, x2, y2)


app = wx.App(False)
frame = PaintFrame(None, 'PaintDC example')
app.MainLoop()