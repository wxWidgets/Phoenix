#!/usr/bin/env python

import wx

import os
import sys
import glob
import random

from wx.lib import masked

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

try:
    from agw import zoombar as ZB
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.zoombar as ZB


_buttonStatus = {True: "Disable First Button",
                 False: "Enable First Button"}

#----------------------------------------------------------------------

class TestPanel(wx.Panel):

    def __init__(self, parent, log):

        self.log = log
        self.enabled = True

        wx.Panel.__init__(self, parent, -1)

        self.sizer_1_staticbox = wx.StaticBox(self, -1, "ZoomBar Options")
        self.zoomSpin = wx.SpinCtrl(self, -1, "3", min=1, max=5)

        self.colourzoom = wx.ColourPickerCtrl(self, colour=wx.Colour(97, 97, 97))
        self.buttonSize = masked.NumCtrl(self, value=32, allowNegative=False,
                                         min=32, max=72)

        self.centerZoom = wx.CheckBox(self, -1, "Center Zoom")
        self.showReflections = wx.CheckBox(self, -1, "Show Reflections")
        self.showLabels = wx.CheckBox(self, -1, "Show Labels")
        self.enableButton = wx.Button(self, -1, "Disable First Button")

        self.zbp = ZB.ZoomBar(self, -1)

        standard = glob.glob(bitmapDir + "/*96.png")
        reflections = glob.glob(bitmapDir + "/*96Flip40.png")

        separatorImage = bitmapDir + "/separator.gif"
        separatorReflection = bitmapDir + "/separatorFlip.png"
        count = 0

        for std, ref in zip(standard, reflections):
            if random.randint(0, 1) == 1 and count > 0:
                sep1 = wx.Bitmap(separatorImage, wx.BITMAP_TYPE_GIF)
                sep2 = wx.Bitmap(separatorReflection, wx.BITMAP_TYPE_PNG)
                self.zbp.AddSeparator(sep1, sep2)

            bname = os.path.split(std)[1][0:-6]
            self.zbp.AddButton(wx.Bitmap(std, wx.BITMAP_TYPE_PNG), wx.Bitmap(ref, wx.BITMAP_TYPE_PNG), bname)
            count += 1

        self.zbp.ResetSize()

        self.SetProperties()
        self.DoLayout()

        self.Bind(wx.EVT_SPINCTRL, self.OnZoomFactor, self.zoomSpin)
        self.Bind(wx.EVT_CHECKBOX, self.OnCenterZoom, self.centerZoom)
        self.Bind(wx.EVT_CHECKBOX, self.OnShowReflections, self.showReflections)
        self.Bind(wx.EVT_CHECKBOX, self.OnShowLabels, self.showLabels)
        self.Bind(wx.EVT_BUTTON, self.OnEnable, self.enableButton)

        self.Bind(masked.EVT_NUM, self.OnButtonSize, self.buttonSize)

        self.colourzoom.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnZoomColour)

        self.Bind(ZB.EVT_ZOOMBAR, self.OnZoomBar)


    def SetProperties(self):

        self.centerZoom.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.showReflections.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.showLabels.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))

        self.centerZoom.Enable(False)
        self.showLabels.SetValue(1)
        self.showReflections.SetValue(1)


    def DoLayout(self):

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        centerSizer = wx.BoxSizer(wx.VERTICAL)
        sizer_1 = wx.StaticBoxSizer(self.sizer_1_staticbox, wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.FlexGridSizer(3, 2, 5, 5)
        mainSizer.Add((20, 20), 1, wx.EXPAND, 0)
        centerSizer.Add((20, 20), 1, 0, 0)
        label_1 = wx.StaticText(self, -1, "Zoom Factor:")
        label_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_3.Add(label_1, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.zoomSpin, 1, wx.ALIGN_CENTER_VERTICAL, 0)

        label_2 = wx.StaticText(self, -1, "Bar Colour:")
        label_2.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_3.Add(label_2, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.colourzoom, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        label_3 = wx.StaticText(self, -1, "Button Size:")
        label_3.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_3.Add(label_3, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.buttonSize, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        sizer_2.Add(sizer_3, 0, wx.EXPAND|wx.ALL, 5)

        sizer_2.Add(self.centerZoom, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.showReflections, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.showLabels, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.enableButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        centerSizer.Add(sizer_1, 0, wx.EXPAND, 0)
        centerSizer.Add(self.zbp, 0, wx.TOP|wx.EXPAND, 20)
        centerSizer.Add((0, 0), 1, 0, 0)
        mainSizer.Add(centerSizer, 10, wx.EXPAND, 0)
        mainSizer.Add((0, 0), 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)


    def OnZoomBar(self, event):

        self.log.write("Selected button index and label: %d, %s\n"%(event.GetSelection(), event.GetLabel()))


    def OnZoomFactor(self, event):

        value = event.GetInt()
        self.zbp.SetZoomFactor(value)

        event.Skip()


    def OnZoomColour(self, event):

        colour = event.GetEventObject().GetColour()
        self.zbp.SetBarColour(colour)


    def OnCenterZoom(self, event):

        self.zbp.SetCenterZoom(event.IsChecked())
        wx.CallAfter(self.ReLayout)


    def OnShowReflections(self, event):

        if event.IsChecked():
            self.centerZoom.SetValue(0)
            self.centerZoom.Enable(False)
            self.zbp.SetCenterZoom(False)
            self.zbp.SetShowReflections(True)
        else:
            self.centerZoom.Enable(True)
            self.zbp.SetShowReflections(False)

        wx.CallAfter(self.ReLayout)


    def OnShowLabels(self, event):

        self.zbp.SetShowLabels(event.IsChecked())
        wx.CallAfter(self.ReLayout)


    def OnEnable(self, event):

        self.zbp.EnableButton(0, not self.enabled)
        self.enabled = not self.enabled

        obj = event.GetEventObject()
        obj.SetLabel(_buttonStatus[self.enabled])
        obj.Refresh()


    def OnButtonSize(self, event):

        value = event.GetValue()
        event.Skip()

        if value < 32 or value > 72:
            return

        self.zbp.SetButtonSize(value)
        wx.CallAfter(self.ReLayout)


    def ReLayout(self):

        self.Layout()
        self.Refresh()
        self.Update()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = ZB.__doc__


if __name__ == '__main__':
    import sys, os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

