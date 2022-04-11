#!/usr/bin/env python

# ThumbnailCtrl Demo  Michael Eager @ 2020 Oct 23
# Adapted from ThumbnailCtrl Demo Andrea Gavana @ 10 Dec 2005

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
    """Demo program for ThumbnailCtrl widget.

    :class:`ThumbnailCtrl` provides an image browser widget in a
    scrollable window containing thumbnail images.  The class reads
    the specified directory, filters by image type, and create
    thumbnail images.  The images can be selected, resized, or rotated.
    Files can be deleted.  Optionally, tooltips can provide information
    about the image file or popups can be displayed when a thumbnail is
    selected.

    The included :class:`Thumb` supports image files like JPEG, GIF, or
    PNG, using either native Python or PIL functions.

    :class:`ScrolledThumbnail` is used by :class:`ThumbnailCtrl`, to
    provide the scrolling thumbnail window.  Many of the methods of
    :class:`ThumbnailCtrl` are actually delegated to
    :class:`ScrolledThumbnail`.

    For full documentation, see the comments in agw/thumbnailctrl.py.

    This class extends the common code in ThumbDemoConfig to work with
    the :class:`ThumbnailCtrl` widget.
    """

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


    # Create ThumbnailCtrl in the left side of the splitter window.
    # Default:  Use native image handling functions, edit to use PIL.
    # Call ThumbnailCtrl:ShowDir() to read directory and display images.
    def SetScroll(self):

        self.scroll = TC.ThumbnailCtrl(self.splitter, -1, imagehandler=TC.NativeImageHandler)
        #scroll = TC.ThumbnailCtrl(self.splitter, -1, imagehandler=TC.PILImageHandler)

        # Display file names with thumbnails.
        self.scroll.ShowFileNames()
        if os.path.isdir("../bitmaps"):
            self.scroll.ShowDir(os.path.normpath(os.getcwd() + "/../bitmaps"))
        else:
            self.scroll.ShowDir(os.getcwd())


    # Following three functions override dummy functions in ThumbDemoConfig
    # to add checkbox for displaying folder path in ThumbnailCtrl widget.
    def DoComboCheckbox(self):
        self.showcombo = wx.CheckBox(self.panel, -1, "Show folder combobox")

    def DoBindCombo(self):
        self.Bind(wx.EVT_CHECKBOX, self.OnShowComboBox, self.showcombo)

    def DoAddCombo(self, customsizer):
        customsizer.Add(self.showcombo, 0, wx.LEFT|wx.BOTTOM|wx.ADJUST_MINSIZE, 3)

    def OnShowComboBox(self, event):

        if self.showcombo.GetValue() == 1:
            self.log.write("OnShowComboBox: Directory comboBox shown\n")
            self.scroll.ShowComboBox(True)
        else:
            self.log.write("OnShowComboBox: Directory comboBox hidden\n")
            self.scroll.ShowComboBox(False)

        event.Skip()

    def ShowDir(self, dir):
        self.scroll.ShowDir(dir)


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
