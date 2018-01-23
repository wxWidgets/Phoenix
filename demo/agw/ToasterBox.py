#!/usr/bin/env python

# Main ToasterBoxDemo

import wx
import wx.adv
import wx.lib.scrolledpanel as scrolled

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import toasterbox as TB
    bitmapDir = "bitmaps/"
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.toasterbox as TB
    bitmapDir = "agw/bitmaps/"

# In case of TB_COMPLEX style, create a panel that contains an image, some
# text, an hyperlink and a ticker.

from wx.lib.ticker import Ticker

# ------------------------------------------------------------------------------ #
# Class ToasterBoxDemo
#    This class implements the demo for toasterbox control. try to change the
#    style using the radiobox in the upper section of the frame, and see how
#    ToasterBox acts.
# ------------------------------------------------------------------------------ #

class ToasterBoxDemo(scrolled.ScrolledPanel):

    def __init__(self, parent, log):

        scrolled.ScrolledPanel.__init__(self, parent)

        self.log = log

        mainSz = wx.BoxSizer(wx.VERTICAL)

        horSz0 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add((0, 3))
        mainSz.Add(horSz0, 1, wx.EXPAND | wx.BOTTOM, 7)

        sampleList = [" ToasterBox TB_SIMPLE ", " ToasterBox TB_COMPLEX "]
        rb = wx.RadioBox(self, -1, "ToasterBox Style", wx.DefaultPosition,
                         wx.DefaultSize, sampleList, 2, wx.RA_SPECIFY_COLS)

        horSz0.Add(rb, 1, 0, 5)
        rb.SetToolTip(wx.ToolTip("Choose the ToasterBox style"))

        self.radiochoice = rb

        horSz1 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz1, 1, wx.EXPAND | wx.ALL, 5)

        statTxt1 = wx.StaticText(self, -1, "Popup position x/y")
        horSz1.Add(statTxt1, 3)
        txtCtrl1 = wx.TextCtrl(self, -1, "500")
        horSz1.Add(txtCtrl1, 1)
        txtCtrl1b = wx.TextCtrl(self, -1, "500")
        horSz1.Add(txtCtrl1b, 1)

        self.posx = txtCtrl1
        self.posy = txtCtrl1b

        horSz2 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz2, 1, wx.EXPAND | wx.ALL, 5)

        statTxt2 = wx.StaticText(self, -1, "Popup size x/y")
        horSz2.Add(statTxt2, 3)
        txtCtrl2 = wx.TextCtrl(self, -1, "210")
        horSz2.Add(txtCtrl2, 1)
        txtCtrl3 = wx.TextCtrl(self, -1, "130")
        horSz2.Add(txtCtrl3, 1)

        self.sizex = txtCtrl2
        self.sizey = txtCtrl3

        horSz3 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz3, 1, wx.EXPAND | wx.ALL, 5)

        statTxt3 = wx.StaticText(self, -1, "Popup linger")
        horSz3.Add(statTxt3, 3)
        txtCtrl4 = wx.TextCtrl(self, -1, "4000")
        helpstr = "How long the popup will stay\naround after it is launched"
        txtCtrl4.SetToolTip(wx.ToolTip(helpstr))
        horSz3.Add(txtCtrl4, 1)

        self.linger = txtCtrl4

        horSz3b = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz3b, 1, wx.EXPAND | wx.ALL, 5)
        statTxt3b = wx.StaticText(self, -1, "Popup scroll speed")
        horSz3b.Add(statTxt3b, 3)
        txtCtrl4b = wx.TextCtrl(self, -1, "8")
        helpstr = "How long it takes the window to \"fade\" in and out"
        txtCtrl4b.SetToolTip(wx.ToolTip(helpstr))
        horSz3b.Add(txtCtrl4b, 2)

        self.scrollspeed = txtCtrl4b

        horSz3c = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz3c, 1, wx.EXPAND | wx.ALL, 5)
        statTxt3c = wx.StaticText(self, -1, "Popup background picture")
        horSz3c.Add(statTxt3c, 3)
        txtCtrl4c = wx.FilePickerCtrl(self, -1, style=wx.FLP_USE_TEXTCTRL|wx.FLP_OPEN)
        horSz3c.Add(txtCtrl4c, 2)

        self.backimage = txtCtrl4c

        popupText1 = "Hello from wxPython! This is another (probably) useful class. " \
                     "written by Andrea Gavana @ 8 September 2005."
        popupText2 = "I don't know what to write in this message. If you like this " \
                     "class, please let me know!."

        horSz4 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz4, 1, wx.EXPAND | wx.ALL, 5)
        statTxt4 = wx.StaticText(self, -1, "Popup text")
        horSz4.Add(statTxt4, 1)
        txtCtrl5 = wx.TextCtrl(self, -1, popupText1)
        horSz4.Add(txtCtrl5, 2)

        self.showntext = txtCtrl5
        self.popupText1 = popupText1
        self.popupText2 = popupText2
        self.counter = 0

        horSz5 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz5, 1, wx.EXPAND | wx.ALL, 5)
        self.colButton1 = wx.Button(self, -1, "Set BG Colour")
        self.colButton1.SetToolTip(wx.ToolTip("Set the ToasterBox background colour"))
        self.colButton1.Bind(wx.EVT_BUTTON, self.SetColours)
        horSz5.Add(self.colButton1, 1, 0, 5)
        self.colButton2 = wx.Button(self, -1, "Set FG Colour")
        self.colButton2.SetToolTip(wx.ToolTip("Set the ToasterBox text colour"))
        self.colButton2.Bind(wx.EVT_BUTTON, self.SetColours2)
        horSz5.Add(self.colButton2, 1, 0, 5)

        horSz6 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz6, 1, wx.EXPAND | wx.ALL, 5)
        statTxt6 = wx.StaticText(self, -1, "Popup text font")
        horSz6.Add(statTxt6, 1, 0, 5)
        fontbutton = wx.Button(self, -1, "Select font")
        horSz6.Add(fontbutton, 1, 0, 5)

        horSz7 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz7, 1, wx.EXPAND | wx.ALL, 5)
        self.checkcaption = wx.CheckBox(self, -1, "Show with caption")
        horSz7.Add(self.checkcaption, 1, 0, 5)
        self.captiontext = wx.TextCtrl(self, -1, "ToasterBox title!")
        horSz7.Add(self.captiontext, 1, 0, 5)
        self.captiontext.Enable(False)
        self.checkcaption.Bind(wx.EVT_CHECKBOX, self.OnCheckCaption)

        horSz8 = wx.BoxSizer(wx.VERTICAL)
        mainSz.Add(horSz8, 1, wx.EXPAND | wx.ALL, 5)
        self.radiotime = wx.RadioButton(self, -1, "Hide by time", style=wx.RB_GROUP)
        horSz8.Add(self.radiotime, 1, 0, 5)
        self.radioclick = wx.RadioButton(self, -1, "Hide by click")
        horSz8.Add(self.radioclick, 1, 0, 5)

        horSz9 = wx.BoxSizer(wx.HORIZONTAL)
        mainSz.Add(horSz9, 1, wx.EXPAND | wx.ALL, 5)
        goButton = wx.Button(self, -1, "Show ToasterBox!")
        goButton.SetToolTip(wx.ToolTip("Launch ToasterBox. You can click more than once!"))
        horSz9.Add((1,0), 1)
        horSz9.Add(goButton, 2, 0, 5)
        horSz9.Add((1,0), 1)

        self.colButton1.SetBackgroundColour(wx.WHITE)
        self.colButton2.SetBackgroundColour(wx.BLACK)
        self.colButton2.SetForegroundColour(wx.WHITE)

        goButton.Bind(wx.EVT_BUTTON, self.ButtonDown)
        fontbutton.Bind(wx.EVT_BUTTON, self.OnSelectFont)
        rb.Bind(wx.EVT_RADIOBOX, self.OnRadioBox)

        self.curFont = self.GetFont()

        self.SetAutoLayout(True)
        self.SetSizer(mainSz)
        self.Fit()
        self.SetupScrolling()


    def SetColours(self, event):

        cd = wx.ColourDialog(self)
        cd.ShowModal()
        colBg = cd.GetColourData().GetColour()
        colButton1 = event.GetEventObject()
        colButton1.SetBackgroundColour(colBg)


    def SetColours2(self, event):

        cd = wx.ColourDialog(self)
        cd.ShowModal()
        colFg = cd.GetColourData().GetColour()
        colButton2 = event.GetEventObject()
        colButton2.SetBackgroundColour(colFg)


    def OnSelectFont(self, event):

        curFont = self.GetFont()
        curClr = wx.BLACK
        data = wx.FontData()
        data.EnableEffects(True)
        data.SetColour(curClr)
        data.SetInitialFont(curFont)

        dlg = wx.FontDialog(self, data)

        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            colour = data.GetColour()

            self.curFont = font
            self.curClr = colour

        dlg.Destroy()


    def OnRadioBox(self, event):

        mainsizer = self.GetSizer()

        if event.GetInt() == 0:
            self.linger.SetValue("4000")
            self.scrollspeed.SetValue("8")

            for ii in range(5, 10):
                mainsizer.Show(ii, True)

        else:
            for ii in range(5, 10):
                mainsizer.Show(ii, False)

            self.linger.SetValue("10000")
            self.scrollspeed.SetValue("20")

        mainsizer.Layout()
        self.Refresh()

        event.Skip()


    def OnCheckCaption(self, event):

        if self.checkcaption.GetValue():
            self.captiontext.Enable(True)
            self.sizex.SetValue("250")
            self.sizey.SetValue("200")
        else:
            self.captiontext.Enable(False)
            self.sizex.SetValue("250")
            self.sizey.SetValue("200")

        self.sizex.Refresh()
        self.sizey.Refresh()


    def ButtonDown(self, event):

        demochoice = self.radiochoice.GetSelection()

        if self.checkcaption.GetValue():
            txts = self.captiontext.GetValue().strip()
            windowstyle = TB.TB_CAPTION
        else:
            windowstyle = TB.TB_DEFAULT_STYLE

        if demochoice == 1:
            tbstyle = TB.TB_COMPLEX
        else:
            tbstyle = TB.TB_SIMPLE

        if self.radioclick.GetValue():
            closingstyle = TB.TB_ONCLICK
        else:
            closingstyle = TB.TB_ONTIME

        tb = TB.ToasterBox(self, tbstyle, windowstyle, closingstyle,
                           scrollType=TB.TB_SCR_TYPE_FADE
                           )

        if windowstyle == TB.TB_CAPTION:
            tb.SetTitle(txts)

        sizex = int(self.sizex.GetValue())
        sizey = int(self.sizey.GetValue())
        tb.SetPopupSize((sizex, sizey))

        posx = int(self.posx.GetValue())
        posy = int(self.posy.GetValue())
        tb.SetPopupPosition((posx, posy))

        tb.SetPopupPauseTime(int(self.linger.GetValue()))
        tb.SetPopupScrollSpeed(int(self.scrollspeed.GetValue()))

        if demochoice == 0:    # Simple Demo:

            self.RunSimpleDemo(tb)

        else:

            self.RunComplexDemo(tb)

        tb.Play()


    def RunSimpleDemo(self, tb):

        tb.SetPopupBackgroundColour(self.colButton1.GetBackgroundColour())
        tb.SetPopupTextColour(self.colButton2.GetBackgroundColour())
        bmp = self.backimage.GetPath()
        dummybmp = wx.NullBitmap

        if os.path.isfile(bmp):
            dummybmp = wx.Bitmap(bmp)

        if dummybmp.IsOk():
            tb.SetPopupBitmap(bmp)
        else:
            tb.SetPopupBitmap()

        txtshown = self.showntext.GetValue()
        if self.counter == 0:
            if txtshown in [self.popupText1, self.popupText2]:
                self.counter = self.counter + 1
                txtshown = self.popupText1
        else:
            if txtshown in [self.popupText1, self.popupText2]:
                self.counter = 0
                txtshown = self.popupText2

        tb.SetPopupText(txtshown)
        tb.SetPopupTextFont(self.curFont)


    def RunComplexDemo(self, tb):

        # This Is The New Call Style: The Call To GetToasterBoxWindow()
        # Is Mandatory, In Order To Create A Custom Parent On ToasterBox.

        tbpanel = tb.GetToasterBoxWindow()
        panel = wx.Panel(tbpanel, -1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        horsizer1 = wx.BoxSizer(wx.HORIZONTAL)

        myimage = wx.Bitmap(os.path.join(bitmapDir, "sttfont.png"), wx.BITMAP_TYPE_PNG)
        stbmp = wx.StaticBitmap(panel, -1, myimage)
        horsizer1.Add(stbmp, 0)

        strs = "This Is Another Example Of ToasterBox, A Complex One. This Kind Of"
        strs = strs + " ToasterBox Can Be Created Using The Style TB_COMPLEX."
        sttext = wx.StaticText(panel, -1, strs)
        horsizer1.Add(sttext, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        hl = wx.adv.HyperlinkCtrl(panel, -1, label="My Home Page",
                                  url="http://xoomer.alice.it/infinity77/")

        sizer.Add((0,5))
        sizer.Add(horsizer1, 0, wx.EXPAND)

        horsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        horsizer2.Add((5, 0))
        horsizer2.Add(hl, 0, wx.EXPAND | wx.TOP, 10)
        sizer.Add(horsizer2, 0, wx.EXPAND)

        tk = Ticker(panel)
        tk.SetText("Hello From wxPython!")

        horsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        horsizer3.Add((5, 0))
        horsizer3.Add(tk, 1, wx.EXPAND | wx.TOP, 10)
        horsizer3.Add((5,0))
        sizer.Add(horsizer3, 0, wx.EXPAND)

        panel.SetSizer(sizer)
        panel.Layout()

        tb.AddPanel(panel)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = ToasterBoxDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = TB.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
