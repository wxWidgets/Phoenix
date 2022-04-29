#!/usr/bin/env python

import wx
import images

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1,
                         style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.log = log

        b = wx.Button(self, 10, "Default Button", (20, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b.SetDefault()
        b.SetSize(b.GetBestSize())

        b = wx.Button(self, 20, "HELLO AGAIN!", (20, 80))
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)
        b.SetToolTip("This is a Hello button...")

        b = wx.Button(self, 40, "Flat Button?", (20,160), style=wx.NO_BORDER)
        b.SetToolTip("This button has a style flag of wx.NO_BORDER.\n"
                           "On some platforms that will give it a flattened look.")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)

        b = wx.Button(self, 50, "wx.Button with icon", (20, 220))
        b.SetToolTip("wx.Button can how have an icon on the left, right,\n"
                           "above or below the label.")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)

        b.SetBitmap(wx.BitmapBundle(images.Mondrian.Bitmap),
                    wx.LEFT    # Left is the default, the image can be on the other sides too
                    #wx.RIGHT
                    #wx.TOP
                    #wx.BOTTOM
                    )
        b.SetBitmapMargins((2,2)) # default is 4 but that seems too big to me.

        # Setting the bitmap and margins changes the best size, so
        # reset the initial size since we're not using a sizer in this
        # example which would have taken care of this for us.
        b.SetInitialSize()

        #b = wx.Button(self, 60, "Multi-line\nbutton", (20, 280))
        #b = wx.Button(self, 70, pos=(160, 280))
        #b.SetLabel("Another\nmulti-line")

    def OnClick(self, event):
        self.log.write("Click! (%d)\n" % event.GetId())

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = """<html><body>
<h2>Button</h2>

A button is a control that contains a text string or a bitmap and can be
placed on nearly any kind of window.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

