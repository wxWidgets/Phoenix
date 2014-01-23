#!/usr/bin/env python

import wx

from Main import opj

#----------------------------------------------------------------------

# AdjustChannels demo. The interesting part is ImageWindow.OnPaint

class TestAdjustChannels(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        topsizer= wx.BoxSizer(wx.HORIZONTAL) # left controls, right image output

        # slider controls controls
        ctrlsizer= wx.BoxSizer(wx.VERTICAL)

        label= wx.StaticText(self, -1, "Factor red in %")
        label.SetForegroundColour("RED")
        ctrlsizer.Add(label, 0, wx.ALL, 5)
        sliderred= wx.Slider(self, wx.NewId(), 100, 0, 200, size=(150, -1), style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        sliderred.SetForegroundColour("RED")
        sliderred.SetTickFreq(50)
        ctrlsizer.Add(sliderred)
        ctrlsizer.AddSpacer(15)

        label= wx.StaticText(self, -1, "Factor green in %")
        label.SetForegroundColour("GREEN")
        ctrlsizer.Add(label, 0, wx.ALL, 5)
        slidergreen= wx.Slider(self, wx.NewId(), 100, 0, 200, size=(150, -1), style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        slidergreen.SetForegroundColour("GREEN")
        slidergreen.SetTickFreq(50)
        ctrlsizer.Add(slidergreen)
        ctrlsizer.AddSpacer(15)

        label= wx.StaticText(self, -1, "Factor blue in %")
        label.SetForegroundColour("BLUE")
        ctrlsizer.Add(label, 0, wx.ALL, 5)
        sliderblue= wx.Slider(self, wx.NewId(), 100, 0, 200, size=(150, -1), style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        sliderblue.SetForegroundColour("BLUE")
        sliderblue.SetTickFreq(50)
        ctrlsizer.Add(sliderblue)
        ctrlsizer.AddSpacer(20)

        label= wx.StaticText(self, -1, "Factor alpha in %")
        ctrlsizer.Add(label, 0, wx.ALL, 5)
        slideralpha= wx.Slider(self, wx.NewId(), 100, 0, 200, size=(150, -1), style = wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS)
        slideralpha.SetTickFreq(50)
        ctrlsizer.Add(slideralpha)

        topsizer.Add(ctrlsizer, 0, wx.ALL, 10)

        # image window
        self.images= ImageWindow(self)
        topsizer.Add(self.images, 1, wx.EXPAND)

        self.SetSizer(topsizer)
        topsizer.Layout()

        # forward the slider change events to the image window
        sliderred.Bind(wx.EVT_SCROLL, self.images.OnScrollRed)
        slidergreen.Bind(wx.EVT_SCROLL, self.images.OnScrollGreen)
        sliderblue.Bind(wx.EVT_SCROLL, self.images.OnScrollBlue)
        slideralpha.Bind(wx.EVT_SCROLL, self.images.OnScrollAlpha)


class ImageWindow(wx.Window):
    def __init__(self, parent):
        wx.Window.__init__(self, parent)
        self.image1= wx.Image(opj('bitmaps/image.bmp'), wx.BITMAP_TYPE_BMP)
        self.image2= wx.Image(opj('bitmaps/toucan.png'), wx.BITMAP_TYPE_PNG)

        # the factors -- 1.0 does not not modify the image
        self.factorred=   1.0
        self.factorgreen= 1.0
        self.factorblue=  1.0
        self.factoralpha= 1.0

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnScrollRed(self, event):
        # position is a int value -- calculate the factor
        self.factorred = event.GetPosition() / 100.0
        self.Refresh()

    def OnScrollGreen(self, event):
        # position is a int value -- calculate the factor
        self.factorgreen = event.GetPosition() / 100.0
        self.Refresh()

    def OnScrollBlue(self, event):
        # position is a int value -- calculate the factor
        self.factorblue = event.GetPosition() / 100.0
        self.Refresh()

    def OnScrollAlpha(self, event):
        # position is a int value -- calculate the factor
        self.factoralpha = event.GetPosition() / 100.0
        self.Refresh()

    def OnPaint(self, event):
        dc= wx.PaintDC(self)
        dc= wx.BufferedDC(dc)

        # paint a background to show the alpha manipulation
        dc.SetBackground(wx.Brush("WHITE"))
        dc.Clear()
        dc.SetBrush(wx.Brush("GREY", wx.BRUSHSTYLE_CROSSDIAG_HATCH))
        windowsize= self.GetSize()
        dc.DrawRectangle(0, 0, windowsize[0], windowsize[1])

        # apply correction to the image channels via wx.Image.AdjustChannels
        image= self.image1.AdjustChannels(self.factorred, self.factorgreen, self.factorblue, self.factoralpha)
        bitmap= wx.Bitmap(image)
        dc.DrawBitmap(bitmap, 10, 10, True)

        image= self.image2.AdjustChannels(self.factorred, self.factorgreen, self.factorblue, self.factoralpha)
        bitmap= wx.Bitmap(image)
        dc.DrawBitmap(bitmap, 10, 110, True)

    def OnSize(self, event):
        self.Refresh()

    def OnEraseBackground(self, event):
        pass


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestAdjustChannels(nb, log)
    return win

#----------------------------------------------------------------------


overview = """<html><body>
<h2>Adjust Channels</h2>

<p>
The <code>wx.Image</code> member function '<code>AdjustChannels</code>' is a fast way to manipulate the four
channels (red, green, blue, alpha) of a <code>wx.Image</code>. It can be used for <b>colour</b> or
<b>gamma correction</b> of a image. It is also possible to <b>add</b> or <b>enhance</b> the <b>transparency</b>
of a image via this function (eg. for fade-in/fade-out effects).
</p>

<p>
The function expects four float values (one for each channel) and multiplies every
byte in the channel with the given factor (written in C++). That means a 1.0 will not alter the channel
and eg. 1.2 will 'enhance' the channel by 20%.
</p>

<pre>
Examples:

# make a image 10% brighter - first three parameters are the factors for red, green and blue
image= image.AdjustChannels(1.1, 1.1, 1.1, 1.0)

# add 20% transparency to a image - the last parameter is the factor for the alpha channel
image= image.AdjustChannels(1.0, 1.0, 1.0, 0.8)
</pre>


</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

