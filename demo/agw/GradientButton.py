#!/usr/bin/env python

import wx

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import gradientbutton as GB
    bitmapDir = "bitmaps/"
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.gradientbutton as GB
    bitmapDir = "agw/bitmaps/"


class GradientButtonDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)

        self.log = log
        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour(wx.WHITE)
        # Initialize GradientButton 1 (no image)
        self.btn1 = GB.GradientButton(self.mainPanel, -1, None, "Hello World!")
        # Initialize GradientButton 2 (with image)
        bitmap = wx.Bitmap(os.path.normpath(bitmapDir+"gradientbutton.png"), wx.BITMAP_TYPE_PNG)
        self.btn2 = GB.GradientButton(self.mainPanel, -1, bitmap, "GradientButton")

        self.topStartColour = wx.ColourPickerCtrl(self.mainPanel, colour=self.btn2.GetTopStartColour(),
                                                  name="Top Start")
        self.topEndColour = wx.ColourPickerCtrl(self.mainPanel, colour=self.btn2.GetTopEndColour(),
                                                name="Top End")
        self.bottomStartColour = wx.ColourPickerCtrl(self.mainPanel, colour=self.btn2.GetBottomStartColour(),
                                                     name="Bottom Start")
        self.bottomEndColour = wx.ColourPickerCtrl(self.mainPanel, colour=self.btn2.GetBottomEndColour(),
                                                   name="Bottom End")
        self.pressedTopColour = wx.ColourPickerCtrl(self.mainPanel, colour=self.btn2.GetPressedTopColour(),
                                                    name="Pressed Top")
        self.pressedBottomColour = wx.ColourPickerCtrl(self.mainPanel, colour=self.btn2.GetPressedBottomColour(),
                                                       name="Pressed Bottom")
        self.textColour = wx.ColourPickerCtrl(self.mainPanel, colour=self.btn2.GetForegroundColour(),
                                              name="Text Colour")

        self.DoLayout()
        self.BindEvents()


    def DoLayout(self):

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        colourSizer = wx.FlexGridSizer(4, 4, 1, 10)

        label1 = wx.StaticText(self.mainPanel, -1, "Welcome to the GradientButton demo for wxPython!")
        mainSizer.Add(label1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)

        mainSizer.Add(self.btn1, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 15)
        btnSizer.Add(self.btn2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        btnSizer.Add((20, 0))

        firstStrings = ["Top Start", "Bottom Start", "Pressed Top", "Text Colour"]
        secondStrings = ["Top End", "Bottom End", "Pressed Bottom", ""]

        for strings in firstStrings:
            label = wx.StaticText(self.mainPanel, -1, strings)
            colourSizer.Add(label, 0, wx.ALIGN_CENTER|wx.EXPAND)
        for strings in firstStrings:
            colourSizer.Add(self.FindWindowByName(strings), 0, wx.ALIGN_CENTER|wx.BOTTOM|wx.EXPAND, 10)

        for strings in secondStrings:
            label = wx.StaticText(self.mainPanel, -1, strings)
            colourSizer.Add(label, 0, wx.ALIGN_CENTER|wx.EXPAND)
        for strings in secondStrings[:-1]:
            colourSizer.Add(self.FindWindowByName(strings), 0, wx.ALIGN_CENTER|wx.EXPAND, 10)

        btnSizer.Add(colourSizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        btnSizer.Add((10, 0))
        mainSizer.Add(btnSizer, 0, wx.EXPAND|wx.ALL, 10)

        boldFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldFont.SetWeight(wx.FONTWEIGHT_BOLD)

        for child in self.mainPanel.GetChildren():
            if isinstance(child, wx.StaticText):
                child.SetFont(boldFont)

        buttonFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        buttonFont.SetWeight(wx.FONTWEIGHT_BOLD)
        try:
            buttonFont.SetFaceName("Tahoma")
            self.btn1.SetFont(buttonFont)
            self.btn2.SetFont(buttonFont)
        except:
            self.btn1.SetFont(boldFont)
            self.btn2.SetFont(boldFont)

        self.mainPanel.SetSizer(mainSizer)
        mainSizer.Layout()
        frameSizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        frameSizer.Layout()


    def BindEvents(self):

        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnPickColour)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn2)


    def OnPickColour(self, event):

        obj = event.GetEventObject()
        colour = event.GetColour()
        name = obj.GetName()

        if obj == self.textColour:
            self.btn2.SetForegroundColour(colour)
        else:
            method = "Set%sColour"%(name.replace(" ", ""))
            method = getattr(self.btn2, method)
            method(colour)


    def OnButton(self, event):

        obj = event.GetEventObject()
        self.log.write("You clicked %s\n"%obj.GetLabel())


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = GradientButtonDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = GB.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


