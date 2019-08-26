#!/usr/bin/env python

import os
import glob
import wx
from wx.svg import SVGimage

#----------------------------------------------------------------------

class SVGBitmapDisplay(wx.Panel):
    """
    A simple panel containing a static box and a rasterized SVG image
    """
    def __init__(self, parent, bmp_size, *args, **kw):
        wx.Panel.__init__(self, parent, *args, **kw)
        self.bmp_size = wx.Size(*bmp_size)
        self.statbmp = wx.StaticBitmap(self, bitmap=wx.Bitmap(*self.bmp_size))
        label='{}x{}'.format(self.bmp_size.width, self.bmp_size.height)
        sbox = wx.StaticBoxSizer(wx.VERTICAL, self, label)
        sbox.Add(self.statbmp)
        self.SetSizer(sbox)


    def UpdateSVG(self, svg_filename):
        img = SVGimage.CreateFromFile(svg_filename)
        bmp = img.ConvertToScaledBitmap(self.bmp_size, self)
        self.statbmp.SetBitmap(bmp)
        #print(bmp.GetSize())


#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.listbox = wx.ListBox(self, style=wx.LB_SINGLE, size=(250, -1))
        self.listbox.AppendItems(glob.glob(os.path.join('data', '*.svg')))

        self.updateables = []
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        topRowSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add a few smallish bitmaps in a row
        for d in [32, 64, 128]:
            sbd = SVGBitmapDisplay(self, (d,d))
            self.updateables.append(sbd)
            topRowSizer.Add(sbd, wx.SizerFlags().Border().Top())

        rightSizer.Add(topRowSizer)

        # and add another, larger one below that row
        sbd = SVGBitmapDisplay(self, (256,256))
        self.updateables.append(sbd)
        rightSizer.Add(sbd)

        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(self.listbox, wx.SizerFlags(1).Border(wx.ALL, 10).Expand())
        self.Sizer.Add(rightSizer, wx.SizerFlags(2).Border(wx.RIGHT|wx.BOTTOM|wx.TOP, 10).Expand())

        self.Bind(wx.EVT_LISTBOX, self.OnSelectItem)
        self.listbox.SetSelection(0)

        # Load the first SVG in the list into the static bitmaps
        self.UpdateAll(self.listbox.GetString(0))


    def OnSelectItem(self, evt):
        filename = self.listbox.GetStringSelection()
        self.UpdateAll(filename)


    def UpdateAll(self, svg_filename):
        for item in self.updateables:
            item.UpdateSVG(svg_filename)
        self.Layout()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>SVGImage</center></h2>

The wx.svg.SVGimage class provides the ability to load, parse and render
Scalable Vector Graphics (SVG) files. The advantage of SVG files is that
they can be used to create bitmaps of any size without loss of quality.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

