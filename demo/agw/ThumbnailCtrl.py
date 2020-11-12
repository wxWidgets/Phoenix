#!/usr/bin/env python

import wx
import os

import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

import wx.lib.agw.thumbnailctrl as TC

from wx.lib.agw.scrolledthumbnail import (EVT_THUMBNAILS_SEL_CHANGED, EVT_THUMBNAILS_POINTED,
                                          EVT_THUMBNAILS_DCLICK)

from ThumbDemoConfig import ThumbDemoConfig


class ThumbnailCtrlDemo(ThumbDemoConfig):

    def __init__(self, parent, log):

        name = "ThumbnailCtrl"

        msg = "This Is The About Dialog Of The " + name + " Demo.\n\n" + \
              "Author: Andrea Gavana @ 10 Dec 2005\n\n" + \
              "Modified: Michael Eager @ 15 Oct 2020\n\n" + \
              "Please Report Any Bug/Requests Of Improvements\n" + \
              "To Me At The Following Addresses:\n\n" + \
              "eager@eagercon.com\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        super().__init__ (parent, log, name=name, about=msg)


    def SetScroll(self):

        self.scroll = TC.ThumbnailCtrl(self.splitter, -1, imagehandler=TC.NativeImageHandler)
        #scroll = TC.ThumbnailCtrl(self.splitter, -1, imagehandler=TC.PILImageHandler)

        self.scroll.ShowFileNames()
        if os.path.isdir("../bitmaps"):
            self.scroll.ShowDir(os.path.normpath(os.getcwd() + "/../bitmaps"))
        else:
            self.scroll.ShowDir(os.getcwd())


    def DoComboCheckbox(self):
        self.showcombo = wx.CheckBox(self.panel, -1, "Show folder combobox")


    def DoBindCombo(self):
        self.Bind(wx.EVT_CHECKBOX, self.OnShowComboBox, self.showcombo)

    def DoAddCombo(self, customsizer):
        customsizer.Add(self.showcombo, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)

    def ShowDir(self, dir):
        self.scroll.ShowDir(dir)


    def OnShowComboBox(self, event):

        if self.showcombo.GetValue() == 1:
            self.log.write("OnShowComboBox: Directory comboBox shown\n")
            self.scroll.ShowComboBox(True)
        else:
            self.log.write("OnShowComboBox: Directory comboBox hidden\n")
            self.scroll.ShowComboBox(False)

        event.Skip()


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test ThumbnailCtrl ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = ThumbnailCtrlDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):

    try:
        import PIL.Image
        win = TestPanel(nb, log)
        return win

    except ImportError:

        from Main import MessagePanel
        win = MessagePanel(nb, 'This demo requires PIL (Python Imaging Library).',
                           'Sorry', wx.ICON_WARNING)
        return win

#----------------------------------------------------------------------


overview = TC.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
