#!/usr/bin/env python

import wx
import wx.stc as stc
import keyword

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import rulerctrl as RC
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.rulerctrl as RC

import images

if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Courier New',
              'size' : 9,
              'size2': 7,
              }
elif wx.Platform == '__WXMAC__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 12,
              'size2': 10,
              }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
              }

#----------------------------------------------------------------------
class PythonSTC(stc.StyledTextCtrl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):

        stc.StyledTextCtrl.__init__(self, parent, id, pos, size, style)

        self.SetReadOnly(True)
        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")

        self.SetViewWhiteSpace(False)
        self.SetEdgeColumn(80)
        self.SetMarginWidth(0, 0)
        self.SetMarginWidth(1, 5)
        self.SetMarginWidth(2, 5)
        self.SetScrollWidth(800)

        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        # Python styles
        # Default
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

        self.SetCaretForeground("BLUE")


    # Some methods to make it compatible with how the wxTextCtrl is used
    def SetValue(self, value):
        # if wx.USE_UNICODE:
            # value = value.decode('iso8859_1')

        self.SetReadOnly(False)
        self.SetText(value)
        self.SetReadOnly(True)


class RulerCtrlDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent)
        self.panel = wx.Panel(self, -1)

        statusbar = self.CreateStatusBar(2)
        statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("RulerCtrl wxPython Demo, Andrea Gavana @ 03 Nov 2006"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)

        self.CreateMenu()
        self.LayoutItems()

        self.SetIcon(images.Mondrian.GetIcon())
        sizex = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        sizey = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        self.SetSize((3*sizex/4, 3*sizey/4))
        self.SendSizeEvent()
        self.CenterOnScreen()


    def LayoutItems(self):

        self.stc = PythonSTC(self.panel, -1)
        try:
            with open("RulerCtrl.py", "rt") as fid:
                text = fid.read()
        except:
            with open("agw/RulerCtrl.py", "rt") as fid:
                text = fid.read()

        self.stc.SetValue(text)

        self.ruler1 = RC.RulerCtrl(self.panel, -1, orient=wx.HORIZONTAL, style=wx.SUNKEN_BORDER)
        self.ruler2 = RC.RulerCtrl(self.panel, -1, orient=wx.VERTICAL, style=wx.SUNKEN_BORDER)
        self.ruler3 = RC.RulerCtrl(self.panel, -1, orient=wx.HORIZONTAL)

        self.rightbottomsizer_staticbox1 = wx.StaticBox(self.panel, -1, "Options")
        self.rightbottomsizer_staticbox2 = wx.StaticBox(self.panel, -1, "Messages")

        self.rulerformat = wx.ComboBox(self.panel, -1, choices=["Integer", "Real", "Time", "LinearDB"],
                                       style=wx.CB_DROPDOWN|wx.CB_READONLY)
        self.flip = wx.CheckBox(self.panel, -1, "Flip")
        self.logscale = wx.CheckBox(self.panel, -1, "Log Scale")
        self.labelminor = wx.CheckBox(self.panel, -1, "Label")
        self.alwayslabel = wx.CheckBox(self.panel, -1, "Always Label")
        self.csel1 = wx.ColourPickerCtrl(self.panel, -1, wx.WHITE, style=wx.CLRP_USE_TEXTCTRL)
        self.csel2 = wx.ColourPickerCtrl(self.panel, -1, wx.BLACK, style=wx.CLRP_USE_TEXTCTRL)
        self.csel3 = wx.ColourPickerCtrl(self.panel, -1, wx.BLACK, style=wx.CLRP_USE_TEXTCTRL)
        self.messages = wx.TextCtrl(self.panel, -1, "Here You'll See GUI Messages\n",
                                    style=wx.TE_READONLY|wx.TE_MULTILINE)

        self.SetProperties()
        self.DoLayout()

        self.Bind(wx.EVT_COMBOBOX, self.OnComboFormat, self.rulerformat)
        self.Bind(wx.EVT_CHECKBOX, self.OnFlip, self.flip)
        self.Bind(wx.EVT_CHECKBOX, self.OnLogScale, self.logscale)
        self.Bind(wx.EVT_CHECKBOX, self.OnLabelMinor, self.labelminor)
        self.Bind(wx.EVT_CHECKBOX, self.OnAlwaysLabel, self.alwayslabel)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnBackgroundColour, self.csel1)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnTickColour, self.csel2)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnLabelColour, self.csel3)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.Bind(RC.EVT_INDICATOR_CHANGING, self.OnIndicatorChanging, id=103)
        self.Bind(RC.EVT_INDICATOR_CHANGED, self.OnIndicatorChanged, id=101, id2=104)


    def SetProperties(self):

        self.SetTitle("RulerCtrl wxPython Demo ;-)")
        self.rulerformat.SetSelection(0)
        self.alwayslabel.SetValue(1)

        self.ruler1.SetFormat(RC.IntFormat)
        self.ruler2.SetFormat(RC.IntFormat)
        self.ruler3.SetFormat(RC.IntFormat)

        self.ruler3.SetRange(1, 70)
        self.ruler3.SetLabelEdges(True)

        self.ruler1.LabelMinor(True)
        self.ruler2.LabelMinor(True)
        self.ruler3.LabelMinor(False)

        self.ruler1.AddIndicator(101, 2)
        self.ruler2.AddIndicator(102, 2)
        self.ruler2.AddIndicator(103, 4)
        self.ruler3.AddIndicator(104, 50)

        self.ruler1.SetDrawingParent(self.stc)
        self.ruler2.SetDrawingParent(self.stc)


    def DoLayout(self):

        bottomsizer1 = wx.StaticBoxSizer(self.rightbottomsizer_staticbox1, wx.VERTICAL)
        bottomsizer2 = wx.StaticBoxSizer(self.rightbottomsizer_staticbox2, wx.VERTICAL)

        mainsizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomrightsizer = wx.BoxSizer(wx.VERTICAL)
        gridsizer = wx.FlexGridSizer(8, 2, 10, 10)
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        bottomleftsizer = wx.BoxSizer(wx.HORIZONTAL)
        topsizer = wx.BoxSizer(wx.HORIZONTAL)

        leftsizer.Add((20, 20), 0, wx.ADJUST_MINSIZE, 0)
        topsizer.Add((39, 0), 0, wx.ADJUST_MINSIZE, 0)
        topsizer.Add(self.ruler1, 1, wx.EXPAND, 0)
        leftsizer.Add(topsizer, 0, wx.EXPAND, 0)

        bottomleftsizer.Add((10, 0))
        bottomleftsizer.Add(self.ruler2, 0, wx.EXPAND, 0)
        bottomleftsizer.Add(self.stc, 1, wx.EXPAND, 0)
        leftsizer.Add(bottomleftsizer, 1, wx.EXPAND, 0)
        mainsizer.Add(leftsizer, 3, wx.EXPAND, 0)

        mainsizer.Add((10, 0))
        bottomrightsizer.Add(self.ruler3, 0, wx.EXPAND | wx.ALL, 20)

        label_1 = wx.StaticText(self.panel, -1, "RulerCtrl Format: ")
        gridsizer.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(self.rulerformat, 0, wx.ALL)
        label_2 = wx.StaticText(self.panel, -1, "Set Flipping: ")
        gridsizer.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(self.flip, 0, wx.ALIGN_CENTER_VERTICAL)
        label_3 = wx.StaticText(self.panel, -1, "Set Logarithmic Scale: ")
        gridsizer.Add(label_3, 0, wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(self.logscale, 0, wx.ADJUST_MINSIZE, 5)
        label_5 = wx.StaticText(self.panel, -1, "Label Minor Labels: ")
        gridsizer.Add(label_5, 0, wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(self.labelminor, 0, wx.ALIGN_CENTER_VERTICAL)
        label_6 = wx.StaticText(self.panel, -1, "Always Label End Edges: ")
        gridsizer.Add(label_6, 0, wx.ADJUST_MINSIZE, 5)
        gridsizer.Add(self.alwayslabel, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 6)
        label_7 = wx.StaticText(self.panel, -1, "Change Background Colour: ")
        gridsizer.Add(label_7, 0, wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(self.csel1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_8 = wx.StaticText(self.panel, -1, "Change Tick Colour: ")
        gridsizer.Add(label_8, 0, wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(self.csel2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        label_9 = wx.StaticText(self.panel, -1, "Change Label Colour: ")
        gridsizer.Add(label_9, 0, wx.ALIGN_CENTER_VERTICAL)
        gridsizer.Add(self.csel3, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        bottomsizer1.Add(gridsizer, 1, wx.EXPAND)
        bottomrightsizer.Add(bottomsizer1, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        bottomrightsizer.Add((0, 10))
        bottomsizer2.Add(self.messages, 1, wx.EXPAND | wx.ALL, 5)
        bottomrightsizer.Add(bottomsizer2, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 20)
        bottomrightsizer.Add((0, 10))

        mainsizer.Add(bottomrightsizer, 2, wx.EXPAND, 0)
        self.panel.SetSizer(mainsizer)
        mainsizer.Fit(self.panel)
        mainsizer.SetSizeHints(self.panel)

        framesizer = wx.BoxSizer(wx.VERTICAL)
        framesizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(framesizer)
        framesizer.Layout()


    def OnIndicatorChanging(self, event):

        # Show how to block a changing indicator
        self.Write("NoNoNoNoNo! You Can't Change My Value!")
        return


    def OnIndicatorChanged(self, event):

        self.Write("New Indicator Value Is: %0.2f"%event.GetValue())
        event.Skip()


    def OnSize(self, event):

        event.Skip()

        # Try to emulate the rulers inside a text editor
        wx.CallAfter(self.SizeRulers)


    def Write(self, text):

        self.messages.AppendText(text + "\n")


    def SizeRulers(self):

        dc = wx.MemoryDC()
        width, height = self.stc.GetSize()
        dc.SelectObject(wx.Bitmap(width, height))
        widthMM, heightMM = dc.GetSizeMM()
        dc.SelectObject(wx.NullBitmap)

        self.ruler1.SetRange(0, widthMM/10)
        self.ruler2.SetRange(0, heightMM/10)


    def OnComboFormat(self, event):

        self.ruler3.SetFormat(event.GetSelection()+1)
        event.Skip()


    def OnFlip(self, event):

        self.ruler3.SetFlip(event.IsChecked())
        event.Skip()


    def OnLogScale(self, event):

        self.ruler3.SetLog(event.IsChecked())
        event.Skip()


    def OnLabelMinor(self, event):

        self.ruler3.LabelMinor(event.IsChecked())
        event.Skip()


    def OnAlwaysLabel(self, event):

        self.ruler3.SetLabelEdges(event.IsChecked())
        event.Skip()


    def OnBackgroundColour(self, event):

        self.ruler3.SetBackgroundColour(event.GetEventObject().GetColour())


    def OnTickColour(self, event):

        self.ruler3.SetTickPenColour(event.GetEventObject().GetColour())


    def OnLabelColour(self, event):

        self.ruler3.SetLabelColour(event.GetEventObject().GetColour())


    def CreateMenu(self):

        menuBar = wx.MenuBar(wx.MB_DOCKABLE)
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        item = wx.MenuItem(fileMenu, wx.ID_ANY, "E&xit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        fileMenu.Append(item)

        item = wx.MenuItem(helpMenu, wx.ID_ANY, "About")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        helpMenu.Append(item)

        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)


    def OnQuit(self, event):

        self.Destroy()


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The RulerCtrl Demo.\n\n" + \
            "Author: Andrea Gavana @ 03 Nov 2006\n\n" + \
            "Please Report Any Bug/Requests Of Improvements\n" + \
            "To Me At The Following Addresses:\n\n" + \
            "andrea.gavana@gmail.com\n" + "andrea.gavana@maerskoil.com\n\n" + \
            "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "RulerCtrl wxPython Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test RulerCtrl ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = RulerCtrlDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = RC.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

