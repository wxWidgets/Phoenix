#!/usr/bin/env python

import wx
import images

#import wx.lib.buttons
#wx.BitmapButton = wx.lib.buttons.GenBitmapButton

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1,
                         style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.log = log

        if 0:  # a test case for catching wx.PyAssertionError

            #wx.GetApp().SetAssertMode(wx.PYAPP_ASSERT_SUPPRESS)
            #wx.GetApp().SetAssertMode(wx.PYAPP_ASSERT_EXCEPTION)
            #wx.GetApp().SetAssertMode(wx.PYAPP_ASSERT_DIALOG)
            #wx.GetApp().SetAssertMode(wx.PYAPP_ASSERT_EXCEPTION | wx.PYAPP_ASSERT_DIALOG)

            try:
                bmp = wx.Bitmap("nosuchfile.bmp", wx.BITMAP_TYPE_BMP)
                mask = wx.Mask(bmp, wx.BLUE)
            except wx.PyAssertionError:
                self.log.write("Caught wx.PyAssertionError!  I will fix the problem.\n")
                bmp = images.Test2.GetBitmap()
                mask = wx.MaskColour(bmp, wx.BLUE)
        else:
            bmp = images.Test2.GetBitmap()
            mask = wx.Mask(bmp, wx.BLUE)

        bmp.SetMask(mask)
        b = wx.BitmapButton(self, -1, bmp, (20, 20),
                       (bmp.GetWidth()+10, bmp.GetHeight()+10))
        b.SetToolTip("This is a bitmap button.")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)

        b = wx.BitmapButton(self, -1, bmp, (20, 120),
                            style = wx.NO_BORDER)

        # hide a little surprise in the button...
        img = images.Robin.GetImage()
        # we need to make it be the same size as the primary image, so
        # grab a subsection of this new image
        cropped = img.GetSubImage((20, 20, bmp.GetWidth(), bmp.GetHeight()))
        b.SetBitmapPressed(wx.BitmapBundle(cropped.ConvertToBitmap()))

        b.SetToolTip("This is a bitmap button with \nwx.NO_BORDER style.")
        self.Bind(wx.EVT_BUTTON, self.OnClick, b)


    def OnClick(self, event):
        self.log.write("Click! (%d)\n" % event.GetId())


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = """<html><body>
<h2>BitmapButton</h2>

<p>A BitmapButton control displays a bitmap. It can have a separate bitmap for each button state: normal, selected, disabled.</p>

<p>The bitmaps to be displayed should have a small number of colours, such as 16,
to avoid palette problems.</p>

<p>A bitmap can be derived from most image formats using the wx.Image class.</p>

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

