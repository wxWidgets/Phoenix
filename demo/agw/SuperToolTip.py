#!/usr/bin/env python

import wx
import wx.lib.buttons as buttons
import wx.lib.scrolledpanel as scrolled

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

try:
    from agw import supertooltip as STT
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.supertooltip as STT

import images


class SuperToolTipDemo(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE)
        self.mainPanel = scrolled.ScrolledPanel(self, -1)

        self.headerSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Header")
        self.bodySizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Message Body")
        self.footerSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Footer")
        self.otherSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Other Options")
        self.toolTipSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "SuperToolTip Preview")
        self.colourSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Colours")
        self.stylesRadio = wx.RadioButton(self.mainPanel, -1, "Predefined", style=wx.RB_GROUP)
        self.stylesCombo = wx.ComboBox(self.mainPanel, -1, choices=STT.GetStyleKeys(),
                                       style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.customStyles = wx.RadioButton(self.mainPanel, -1, "Custom     ")
        self.topColourPicker = wx.ColourPickerCtrl(self.mainPanel, colour=wx.WHITE)
        system = wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        r, g, b, a = system
        self.middleColourPicker = wx.ColourPickerCtrl(self.mainPanel, colour=wx.Colour((255-r)/2, (255-g)/2, (255-b)/2))
        self.bottomColourPicker = wx.ColourPickerCtrl(self.mainPanel, colour=system)
        self.headerCheck = wx.CheckBox(self.mainPanel, -1, "Show Header")
        self.headerText = wx.TextCtrl(self.mainPanel, -1, "Merge And Center")
        self.headerBitmap = wx.StaticBitmap(self.mainPanel, -1,
                                            wx.Bitmap(os.path.normpath(os.path.join(bitmapDir, "sttheader.png")),
                                                                          wx.BITMAP_TYPE_PNG))
        self.headerFilePicker = wx.FilePickerCtrl(self.mainPanel, path=os.path.normpath(os.path.join(bitmapDir, "sttheader.png")),
                                                  style=wx.FLP_USE_TEXTCTRL)
        self.headerLineCheck = wx.CheckBox(self.mainPanel, -1, "Draw Line After Header")
        self.bodyBitmap = wx.StaticBitmap(self.mainPanel, -1,
                                          wx.Bitmap(os.path.normpath(os.path.join(bitmapDir, "sttfont.png")),
                                                    wx.BITMAP_TYPE_PNG))
        msg = "</b>A Bold Title\n\nJoins the selected cells into one larger cell\nand centers the contents in the new cell.\n" \
              "This is often used to create labels that span\nmultiple columns.\n\n</l>I am a link{http://xoomer.alice.it/infinity77}"
        self.bodyText = wx.TextCtrl(self.mainPanel, -1, msg, style=wx.TE_MULTILINE)
        self.includeCheck = wx.CheckBox(self.mainPanel, -1, "Include Body Image")
        self.footerCheck = wx.CheckBox(self.mainPanel, -1, "Show Footer")
        self.footerText = wx.TextCtrl(self.mainPanel, -1, "Press F1 for more help")
        self.footerBitmap = wx.StaticBitmap(self.mainPanel, -1,
                                            wx.Bitmap(os.path.normpath(os.path.join(bitmapDir, "stthelp.png")),
                                                      wx.BITMAP_TYPE_PNG))
        self.footerFilePicker = wx.FilePickerCtrl(self.mainPanel, path=os.path.normpath(os.path.join(bitmapDir,"stthelp.png")),
                                                  style=wx.FLP_USE_TEXTCTRL)
        self.footerLineCheck = wx.CheckBox(self.mainPanel, -1, "Draw Line Before Footer")
        self.dropShadow = wx.CheckBox(self.mainPanel, -1, "Rounded Corners And Drop Shadow (Windows XP Only)")
        self.useFade = wx.CheckBox(self.mainPanel, -1, "Fade In/Fade Out Effects (Windows XP Only)")
        self.endTimer = wx.SpinCtrl(self.mainPanel, -1, "5")

        btnBmp = wx.Bitmap(os.path.normpath(os.path.join(bitmapDir,"sttbutton.png")), wx.BITMAP_TYPE_PNG)
        self.toolTipButton = buttons.ThemedGenBitmapTextButton(self.mainPanel, -1, btnBmp, " Big Test Button ",
                                                               size=(-1, 130))
        self.generateTip = wx.Button(self.mainPanel, -1, "Generate SuperToolTip")

        self.CreateMenuBar()
        self.SetProperties()
        self.DoLayout()
        self.mainPanel.SetupScrolling()

        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioColours, self.stylesRadio)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadioColours, self.customStyles)
        self.Bind(wx.EVT_CHECKBOX, self.OnShowHeader, self.headerCheck)
        self.Bind(wx.EVT_CHECKBOX, self.OnShowFooter, self.footerCheck)
        self.generateTip.Bind(wx.EVT_BUTTON, self.OnGenerateTip)
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnPickBitmap, self.headerFilePicker)
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.OnPickBitmap, self.footerFilePicker)

        self.enableWidgets = {}

        self.enableWidgets[self.headerCheck] = [self.headerBitmap, self.headerFilePicker,
                                                self.headerLineCheck, self.headerText]
        self.enableWidgets[self.footerCheck] = [self.footerBitmap, self.footerFilePicker,
                                                self.footerLineCheck, self.footerText]
        self.enableWidgets[self.customStyles] = [self.stylesCombo, self.topColourPicker,
                                                 self.middleColourPicker, self.bottomColourPicker]
        self.enableWidgets[self.stylesRadio] = [self.stylesCombo, self.topColourPicker,
                                                self.middleColourPicker, self.bottomColourPicker]

        self.SetSize((700, 600))
        self.CenterOnScreen()
        self.Show()


    def CreateMenuBar(self):

        menuBar = wx.MenuBar(wx.MB_DOCKABLE)
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        item = wx.MenuItem(fileMenu, wx.ID_ANY, "E&xit", "Exit demo")
        self.Bind(wx.EVT_MENU, self.OnClose, item)
        fileMenu.Append(item)

        item = wx.MenuItem(helpMenu, wx.ID_ANY, "About...", "Shows The About Dialog")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        helpMenu.Append(item)

        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)


    def SetProperties(self):

        self.SetTitle("SuperToolTip wxPython Demo ;-)")
        self.stylesRadio.SetValue(1)
        self.headerCheck.SetValue(1)
        self.footerCheck.SetValue(1)
        self.stylesCombo.SetValue("Office 2007 Blue")
        font = wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, "")
        self.generateTip.SetFont(font)
        self.headerCheck.SetFont(font)
        self.footerCheck.SetFont(font)
        self.endTimer.SetRange(1, 100)
        self.toolTipButton.SetFont(wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        for widgets in [self.topColourPicker, self.middleColourPicker, self.bottomColourPicker]:
            widgets.Enable(False)

        self.SetIcon(images.Mondrian.GetIcon())


    def DoLayout(self):

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        otherSizer = wx.StaticBoxSizer(self.otherSizer_staticbox, wx.VERTICAL)
        toolTipSizer = wx.StaticBoxSizer(self.toolTipSizer_staticbox, wx.HORIZONTAL)
        toolTipSizer_1 = wx.BoxSizer(wx.VERTICAL)
        footerSizer = wx.StaticBoxSizer(self.footerSizer_staticbox, wx.VERTICAL)
        footerSizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        footerSizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        bodySizer = wx.StaticBoxSizer(self.bodySizer_staticbox, wx.HORIZONTAL)
        bodySizer_2 = wx.BoxSizer(wx.VERTICAL)
        headerSizer = wx.StaticBoxSizer(self.headerSizer_staticbox, wx.VERTICAL)
        headerSizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        headerSizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        colourSizer = wx.StaticBoxSizer(self.colourSizer_staticbox, wx.VERTICAL)
        colourSizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        colourSizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        colourSizer_1.Add(self.stylesRadio, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        colourSizer_1.Add(self.stylesCombo, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        colourSizer.Add(colourSizer_1, 1, wx.EXPAND, 0)
        colourSizer_2.Add(self.customStyles, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        label_1 = wx.StaticText(self.mainPanel, -1, "Top:")
        colourSizer_2.Add(label_1, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        colourSizer_2.Add(self.topColourPicker, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        label_2 = wx.StaticText(self.mainPanel, -1, "Middle:")
        colourSizer_2.Add(label_2, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        colourSizer_2.Add(self.middleColourPicker, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        label_3 = wx.StaticText(self.mainPanel, -1, "Bottom:")
        colourSizer_2.Add(label_3, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        colourSizer_2.Add(self.bottomColourPicker, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        colourSizer.Add(colourSizer_2, 1, wx.EXPAND, 0)
        mainSizer.Add(colourSizer, 0, wx.ALL|wx.EXPAND, 5)

        headerSizer.Add(self.headerCheck, 0, wx.ALL, 5)
        label_4 = wx.StaticText(self.mainPanel, -1, "Header Text:")
        headerSizer_1.Add(label_4, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        headerSizer_1.Add(self.headerText, 1, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        headerSizer.Add(headerSizer_1, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        label_5 = wx.StaticText(self.mainPanel, -1, "Header Bitmap:")
        headerSizer_2.Add(label_5, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        headerSizer_2.Add(self.headerBitmap, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        headerSizer_2.Add(self.headerFilePicker, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        headerSizer.Add(headerSizer_2, 1, wx.ALL|wx.EXPAND, 5)
        headerSizer.Add(self.headerLineCheck, 0, wx.ALL, 5)

        footerSizer.Add(self.footerCheck, 0, wx.ALL, 5)
        label_6 = wx.StaticText(self.mainPanel, -1, "Footer Text:")
        footerSizer_1.Add(label_6, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        footerSizer_1.Add(self.footerText, 1, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        footerSizer.Add(footerSizer_1, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 5)
        label_7 = wx.StaticText(self.mainPanel, -1, "Footer Bitmap:")
        footerSizer_2.Add(label_7, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        footerSizer_2.Add(self.footerBitmap, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        footerSizer_2.Add(self.footerFilePicker, 1, wx.RIGHT|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        footerSizer.Add(footerSizer_2, 1, wx.ALL|wx.EXPAND, 5)
        footerSizer.Add(self.footerLineCheck, 0, wx.ALL, 5)

        topSizer.Add(headerSizer, 1, wx.EXPAND|wx.ALL, 5)
        topSizer.Add(footerSizer, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(topSizer, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)

        bodySizer.Add(self.bodyBitmap, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        bodySizer_2.Add(self.bodyText, 1, wx.EXPAND, 0)
        bodySizer_2.Add(self.includeCheck, 0, wx.RIGHT|wx.TOP, 5)
        bodySizer.Add(bodySizer_2, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 5)
        mainSizer.Add(bodySizer, 0, wx.ALL|wx.EXPAND, 5)

        otherSizer.Add(self.dropShadow, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        otherSizer.Add(self.useFade, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_VERTICAL, 5)
        label_8 = wx.StaticText(self.mainPanel, -1, "No Of Seconds SuperToolTip Is Shown:")
        otherSizer.Add((0, 5))
        otherSizer.Add(label_8, 0, wx.LEFT|wx.RIGHT, 5)
        otherSizer.Add((0, 2))
        otherSizer.Add(self.endTimer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)
        mainSizer.Add(otherSizer, 0, wx.ALL|wx.EXPAND, 5)

        toolTipSizer.Add(self.toolTipButton, 1, wx.ALL|wx.EXPAND, 5)
        toolTipSizer_1.Add(self.generateTip, 0, wx.ALL, 5)
        toolTipSizer.Add(toolTipSizer_1, 0, wx.EXPAND, 0)
        mainSizer.Add(toolTipSizer, 1, wx.ALL|wx.EXPAND, 5)
        self.mainPanel.SetSizer(mainSizer)
        mainSizer.Layout()
        frameSizer.Add(self.mainPanel, 1, wx.EXPAND, 0)
        self.SetSizer(frameSizer)
        frameSizer.Layout()
        frameSizer.Fit(self)
        self.Layout()

        wx.CallAfter(mainSizer.Layout)


    def OnRadioColours(self, event):

        self.EnableWidgets(event.GetEventObject(), None)


    def OnShowHeader(self, event):

        checked = event.IsChecked()
        self.EnableWidgets(event.GetEventObject(), checked)


    def OnShowFooter(self, event):

        checked = event.IsChecked()
        self.EnableWidgets(event.GetEventObject(), checked)


    def EnableWidgets(self, obj, checked):

        widgets = self.enableWidgets[obj]
        for indx, control in enumerate(widgets):
            if obj == self.customStyles:
                control.Enable(indx > 0)
            elif obj == self.stylesRadio:
                control.Enable(indx < 1)
            else:
                control.Enable(checked)


    def OnPickBitmap(self, event):

        obj = event.GetEventObject()
        path = event.GetPath()

        bmp = wx.Bitmap(path, wx.BITMAP_TYPE_ANY)
        if obj == self.headerFilePicker:
            self.headerBitmap.SetBitmap(bmp)
            self.headerBitmap.Refresh()
        else:
            self.footerBitmap.SetBitmap(bmp)
            self.footerBitmap.Refresh()


    def OnGenerateTip(self, event):

        if self.stylesRadio.GetValue():
            # Using a predefined style
            styleKey = self.stylesCombo.GetValue()
        else:
            topColour, middleColour, bottomColour = self.topColourPicker.GetColour(), \
                                                    self.middleColourPicker.GetColour(), \
                                                    self.bottomColourPicker.GetColour()

        if self.headerCheck.GetValue() == 0:
            headerText, headerBmp, drawHLine = "", wx.NullBitmap, False
        else:
            headerText = self.headerText.GetValue().strip()
            headerBmp = self.headerBitmap.GetBitmap()
            drawHLine = self.headerLineCheck.GetValue()

        message = self.bodyText.GetValue()
        if self.includeCheck.GetValue():
            bodyImage = self.bodyBitmap.GetBitmap()
        else:
            bodyImage = wx.NullBitmap

        if self.footerCheck.GetValue() == 0:
            footerText, footerBmp, drawFLine = "", wx.NullBitmap, False
        else:
            footerText = self.footerText.GetValue().strip()
            footerBmp = self.footerBitmap.GetBitmap()
            drawFLine = self.footerLineCheck.GetValue()

        if not hasattr(self, "tip"):
            self.tip = STT.SuperToolTip(message)
        else:
            self.tip.SetMessage(message)

        self.tip.SetBodyImage(bodyImage)
        self.tip.SetHeader(headerText)
        self.tip.SetHeaderBitmap(headerBmp)
        self.tip.SetFooter(footerText)
        self.tip.SetFooterBitmap(footerBmp)

        self.tip.SetTarget(self.toolTipButton)
        self.tip.SetDrawHeaderLine(drawHLine)
        self.tip.SetDrawFooterLine(drawFLine)

        self.tip.SetDropShadow(self.dropShadow.GetValue())
        self.tip.SetUseFade(self.useFade.GetValue())
        self.tip.SetEndDelay(self.endTimer.GetValue())

        if self.stylesRadio.GetValue():
            self.tip.ApplyStyle(styleKey)
        else:
            self.tip.SetTopGradientColour(topColour)
            self.tip.SetMiddleGradientColour(middleColour)
            self.tip.SetBottomGradientColour(bottomColour)

    def OnClose(self, event):

        wx.CallAfter(self.Destroy)


    def OnAbout(self, event):

        msg = "This is the about dialog of SuperToolTip demo.\n\n" + \
              "Author: Andrea Gavana @ 07 Oct 2008\n\n" + \
              "Please report any bugs/requests of improvements\n" + \
              "to me at the following addresses:\n\n" + \
              "andrea.gavana@gmail.com\n" + "andrea.gavana@maerskoil.com\n\n" + \
              "Welcome to wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "SuperToolTip wxPython Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class TestPanel(wx.Panel):

    def __init__(self, parent, log):

        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Show SuperToolTip Demo", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):

        SuperToolTipDemo(self)


#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = STT.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

