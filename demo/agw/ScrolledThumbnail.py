#!/usr/bin/env python

# ScrolledThumbnail Demo  Michael Eager @ 2020 Oct 23
# Adapted from ThumbnailCtrl Demo Andrea Gavana @ 10 Dec 2005

import wx
import os
import sys
import time
import wx.lib.agw.scrolledthumbnail as TC
from wx.lib.agw.scrolledthumbnail import (ScrolledThumbnail,
                                          Thumb,
                                          NativeImageHandler)

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

from ThumbDemoConfig import ThumbDemoConfig

class ScrolledThumbnailDemo (ThumbDemoConfig):

    def __init__(self, parent, log):

        name = "ScrolledThumbnail"

        msg = "This Is The About Dialog Of The " + name + " Demo.\n\n" + \
              "Author: Michael Eager @ 10 Nov 2020\n\n" + \
              "Adapted from the ThumbnailCtrl Demo\n" + \
              "By Andrea Gavana @ 10 Dec 2005\n\n" + \
              "Please Report Any Bug/Requests Of Improvements\n" + \
              "To Me At The Following Addresses:\n" + \
              "eager@eagercon.com\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        super().__init__ (parent, log, name=name, about=msg)


    def SetScroll(self):
        self.scroll = ScrolledThumbnail(self.splitter, -1, size=(400,300))


    def ShowDir(self, dir):
        files = os.listdir(dir)
        thumbs = []
        for f in files:
            if os.path.splitext(f)[1] in [".jpg", ".gif", ".png"]:
                statinfo = os.stat(os.path.join(dir, f))
                size = statinfo.st_size
                modtime = statinfo.st_mtime
                TIME_FMT = '%d %b %Y, %H:%M:%S'
                lastmod = time.strftime(TIME_FMT, time.localtime(modtime))
                thumbs.append(Thumb(dir, f, caption=f, size=size, lastmod=lastmod,
                                    imagehandler=NativeImageHandler))
        self.scroll.ShowThumbs(thumbs)


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test ScrolledThumbnail", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = ScrolledThumbnailDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):

    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = wx.lib.agw.scrolledthumbnail.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
