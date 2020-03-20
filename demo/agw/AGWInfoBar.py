#!/usr/bin/env python

import wx
import random

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    import agw.infobar as IB
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.infobar as IB

from images import catalog

#----------------------------------------------------------------------

def GetValidImages():

    valid_images = []
    counter = 0

    for key in catalog:
        bmp = catalog[key].GetBitmap()
        if bmp.GetWidth() == 16 and bmp.GetHeight() == 16:
            valid_images.append(bmp)

    return valid_images

#----------------------------------------------------------------------

flags = [ (wx.ICON_NONE,        "ICON_NONE"),
          (wx.ICON_INFORMATION, "ICON_INFORMATION"),
          (wx.ICON_QUESTION,    "ICON_QUESTION"),
          (wx.ICON_WARNING,     "ICON_WARNING"),
          (wx.ICON_ERROR,       "ICON_ERROR")
          ]


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        # Create the InfoBar.  It starts out in a hidden state so it
        # won't be visible until we need it.
        self.info = IB.InfoBar(self)

        panel = wx.Panel(self)

        self.message = wx.TextCtrl(panel, -1, "Hello World", size=(250,-1))
        self.flags = wx.Choice(panel, choices=[f[1] for f in flags])
        self.flags.SetSelection(1) # wx.ICON_INFORMATION is the default

        self.checkBitmap = wx.CheckBox(panel, -1, 'With Bitmap')

        smBtn = wx.Button(panel, -1, "Show Message")
        dmBtn = wx.Button(panel, -1, "Dismiss")
        addBtn = wx.Button(panel, -1, "Add Button")

        fgs = wx.FlexGridSizer(cols=3, vgap=10, hgap=10)
        fgs.Add(wx.StaticText(panel, -1, "Message:"), 0,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        fgs.Add(self.message)
        fgs.Add(self.flags)
        fgs.AddSpacer(5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(smBtn, 0, wx.RIGHT, 5)
        hbox.Add(dmBtn)
        fgs.Add(hbox)
        fgs.AddSpacer(5)
        fgs.AddSpacer(5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        hbox2.Add(addBtn, 0, wx.RIGHT, 10)
        hbox2.Add(self.checkBitmap, 0, wx.ALIGN_CENTER)
        fgs.Add(hbox2)

        panel.Sizer = wx.BoxSizer(wx.VERTICAL)
        text = """\
An info bar is a transient window shown at top or bottom of its parent window
to display non-critical information to the user."""
        panel.Sizer.Add(wx.StaticText(panel, -1, text), 0, wx.TOP|wx.LEFT, 25)
        panel.Sizer.Add(fgs, 1, wx.EXPAND|wx.ALL, 25)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.info, 0, wx.EXPAND)
        self.Sizer.Add(panel, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnShowMessage, smBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDismiss, dmBtn)
        self.Bind(wx.EVT_BUTTON, self.OnAddButton, addBtn)

        self.valid_images = GetValidImages()


    def OnShowMessage(self, event):
        msg = self.message.GetValue()
        flag = flags[self.flags.GetSelection()][0]
        self.info.ShowMessage(msg, flag)


    def OnDismiss(self, event):
        self.info.Dismiss()


    def OnAddButton(self, event):
        btnId = wx.NewIdRef()

        if self.checkBitmap.GetValue():
            bitmap = random.choice(self.valid_images)
        else:
            bitmap = wx.NullBitmap

        self.info.AddButton(btnId, "New Button", bitmap)
        self.info.Bind(wx.EVT_BUTTON, self.OnButtonClicked, id=btnId)


    def OnButtonClicked(self, event):
        wx.MessageBox("New Button clicked")
        # Calling event.Skip() will allow the default handler to run
        # which will dismiss the info bar.  If you don't want it to be
        # dismissed for a particular button then then don't call
        # Skip().
        event.Skip()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.InfoBar</center></h2>

An info bar is a transient window shown at top or bottom of its parent
window to display non-critical information to the user.

<p>This class provides another way to show messages to the user,
intermediate between message boxes and status bar messages. The
message boxes are modal and thus interrupt the users work flow and
should be used sparingly for this reason. However status bar messages
are often too easy not to notice at all. An info bar provides a way to
present the messages which has a much higher chance to be noticed by
the user but without being annoying.

<p>Info bar may show an icon (on the left), text message and, optionally,
buttons allowing the user to react to the information presented. It
always has a close button at the right allowing the user to dismiss it
so it isn't necessary to provide a button just to close it.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

