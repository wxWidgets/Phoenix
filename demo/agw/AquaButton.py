import wx

if wx.VERSION < (2, 8, 9, 0):
    raise Exception("This demo requires wxPython version greater than 2.8.9.0")

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

try:
    from agw import aquabutton as AB
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.aquabutton as AB

            
class AquaButtonDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)
        self.log = log

        self.mainPanel = wx.Panel(self)
        self.mainPanel.SetBackgroundColour(wx.WHITE)
        
        # Initialize AquaButton 1 (with image)
        bitmap = wx.Bitmap(
            os.path.normpath(os.path.join(bitmapDir, "aquabutton.png")), 
            wx.BITMAP_TYPE_PNG)
        self.btn1 = AB.AquaButton(self.mainPanel, -1, bitmap, "AquaButton")
        # Initialize AquaButton 2 (no image)
        self.btn2 = AB.AquaButton(self.mainPanel, -1, None, "Hello World!")

        self.backColour = wx.ColourPickerCtrl(self.mainPanel, col=self.btn2.GetBackgroundColour())
        self.hoverColour = wx.ColourPickerCtrl(self.mainPanel, col=self.btn2.GetHoverColour())
        self.textColour = wx.ColourPickerCtrl(self.mainPanel, col=self.btn2.GetForegroundColour())
        self.pulseCheck = wx.CheckBox(self.mainPanel, -1, "Pulse On Focus")

        self.DoLayout()
        self.BindEvents()
        

    def DoLayout(self):

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)        
        btnSizer = wx.FlexGridSizer(2, 2, 15, 15)

        colourSizer = wx.FlexGridSizer(2, 3, 1, 10)

        btnSizer.Add(self.btn1, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        btnSizer.Add(self.pulseCheck, 0, wx.ALIGN_CENTER_VERTICAL)
        
        btnSizer.Add(self.btn2, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        
        labelBack = wx.StaticText(self.mainPanel, -1, "Background Colour")
        labelHover = wx.StaticText(self.mainPanel, -1, "Hover Colour")
        labelText = wx.StaticText(self.mainPanel, -1, "Text Colour")

        colourSizer.Add(labelBack)
        colourSizer.Add(labelHover)
        colourSizer.Add(labelText)

        colourSizer.Add(self.backColour, 0, wx.EXPAND)
        colourSizer.Add(self.hoverColour, 0, wx.EXPAND)
        colourSizer.Add(self.textColour, 0, wx.EXPAND)

        btnSizer.Add(colourSizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        label1 = wx.StaticText(self.mainPanel, -1, "Welcome to the AquaButton demo for wxPython!")
        
        mainSizer.Add(label1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)
        mainSizer.Add(btnSizer, 1, wx.EXPAND|wx.ALL, 30)

        boldFont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        boldFont.SetWeight(wx.BOLD)
        
        for child in self.mainPanel.GetChildren():
            if isinstance(child, wx.StaticText):
                child.SetFont(boldFont)
        
        self.mainPanel.SetSizer(mainSizer)
        mainSizer.Layout()
        frameSizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        frameSizer.Layout()


    def BindEvents(self):

        self.Bind(wx.EVT_CHECKBOX, self.OnPulse, self.pulseCheck)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnPickColour)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn1)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.btn2)


    def OnPulse(self, event):

        self.btn1.SetPulseOnFocus(event.IsChecked())


    def OnPickColour(self, event):

        obj = event.GetEventObject()
        colour = event.GetColour()
        if obj == self.backColour:
            self.btn2.SetBackgroundColour(colour)
        elif obj == self.hoverColour:
            self.btn2.SetHoverColour(colour)
        else:
            self.btn2.SetForegroundColour(colour)

            
    def OnButton(self, event):

        obj = event.GetEventObject()
        self.log.write("You clicked %s\n"%obj.GetLabel())

        
#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = AquaButtonDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = AB.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


