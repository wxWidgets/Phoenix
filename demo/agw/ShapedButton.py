#!/usr/bin/env python

import wx
import random

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

try:
    import agw.shapedbutton
    from agw.shapedbutton import SButton, SBitmapButton
    from agw.shapedbutton import SBitmapToggleButton, SBitmapTextToggleButton
    docs = agw.shapedbutton.__doc__
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.shapedbutton
    from wx.lib.agw.shapedbutton import SButton, SBitmapButton
    from wx.lib.agw.shapedbutton import SBitmapToggleButton, SBitmapTextToggleButton
    docs = wx.lib.agw.shapedbutton.__doc__

import images

#----------------------------------------------------------------------
# Beginning Of SHAPEDBUTTON Demo wxPython Code
#----------------------------------------------------------------------

class ShapedButtonDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent, title="ShapedButton wxPython Demo ;-)")

        # Create Some Maquillage For The Demo: Icon, StatusBar, MenuBar...

        self.SetIcon(images.Mondrian.GetIcon())
        self.statusbar = self.CreateStatusBar(2)

        self.statusbar.SetStatusWidths([-2, -1])

        statusbar_fields = [("wxPython ShapedButton Demo, Andrea Gavana @ 18 Oct 2005"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)

        self.SetMenuBar(self.CreateMenuBar())

        framesizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self, -1)
        mainsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer0 = wx.BoxSizer(wx.HORIZONTAL)

        sb0 = wx.StaticBox(self.panel, -1)
        recordsizer = wx.StaticBoxSizer(sb0, wx.HORIZONTAL)

        # Make A ToolBar-Like Audio Control With Round Buttons/Toggles
        self.BuildAudioToolBar()

        recordsizer.Add(self.rewind, 0, wx.LEFT, 3)
        recordsizer.Add(self.play, 0, wx.LEFT, 3)
        recordsizer.Add(self.record, 0, wx.LEFT, 3)
        recordsizer.Add(self.pause, 0, wx.LEFT, 3)
        recordsizer.Add(self.stop, 0, wx.LEFT, 3)
        recordsizer.Add(self.ffwd, 0, wx.LEFT | wx.RIGHT, 3)

        for ii in range(6):
            recordsizer.SetItemMinSize(ii, 48, 48)

        self.eventtext = wx.StaticText(self.panel, -1, "Event Recorder",
                                       style=wx.ST_NO_AUTORESIZE)
        self.eventtext.SetBackgroundColour(wx.BLUE)
        self.eventtext.SetForegroundColour(wx.WHITE)
        self.eventtext.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                                       False, "Verdana", wx.FONTENCODING_DEFAULT))

        smallsizer = wx.BoxSizer(wx.VERTICAL)
        smallsizer.Add((0, 1), 1, wx.EXPAND)
        smallsizer.Add(self.eventtext, 1, wx.EXPAND)
        smallsizer.Add((0, 1), 1, wx.EXPAND)

        hsizer0.Add(recordsizer, 1, wx.EXPAND)
        hsizer0.Add(smallsizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        mainsizer.Add(hsizer0, 0, wx.BOTTOM, 5)

        mainsizer.Add((0, 10), 0, wx.EXPAND)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Make 9 SBitmapButtons With Text Rotation And Different Colours
        sb1 = wx.StaticBox(self.panel, -1, "Some Buttons")
        vsizer1 = wx.StaticBoxSizer(sb1, wx.VERTICAL)

        bsizer = self.BuildNineButtons()
        vsizer1.Add((0, 10), 0)
        vsizer1.Add(bsizer, 1, wx.EXPAND)
        vsizer1.Add((0, 10), 0)
        hsizer.Add(vsizer1, 3, wx.EXPAND)

        # Make Some Mixed SButton/SToggle With Bitmap And Text Rotation
        sb2 = wx.StaticBox(self.panel, -1, "Other Buttons")
        vsizer2 = wx.StaticBoxSizer(sb2, wx.VERTICAL)
        btsizer = self.BuildMixedButtons()
        vsizer2.Add((0, 10), 0)
        vsizer2.Add(btsizer, 1, wx.EXPAND)
        vsizer2.Add((0, 10), 0)
        hsizer.Add(vsizer2, 2, wx.EXPAND)

        # Build Buttons With Elliptic Shape
        sb3 = wx.StaticBox(self.panel, -1, "Elliptic Buttons")
        vsizer3 = wx.StaticBoxSizer(sb3, wx.VERTICAL)
        esizer = self.BuildEllipticButtons()
        vsizer3.Add((0, 10), 0)
        vsizer3.Add(esizer, 1, wx.EXPAND)
        vsizer3.Add((0, 10), 0)
        hsizer.Add(vsizer3, 2, wx.EXPAND)

        mainsizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 5)

        self.panel.SetSizer(mainsizer)
        mainsizer.Layout()
        framesizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(framesizer)
        framesizer.Layout()
        self.SetAutoLayout(True)
        self.Fit()

        self.Layout()
        self.CenterOnParent()


    def BuildAudioToolBar(self):

        # The Rewind Button Is A Simple Bitmap Button (SBitmapButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "rewind.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "rewinddisabled.png"), wx.BITMAP_TYPE_PNG)
        self.rewind = SBitmapButton(self.panel, -1, upbmp, (48, 48))
        self.rewind.SetUseFocusIndicator(False)
        self.rewind.SetBitmapDisabled(disbmp)

        self.rewind.Bind(wx.EVT_BUTTON, self.OnRewind)

        # The Play Button Is A Toggle Bitmap Button (SBitmapToggleButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "play.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "playdisabled.png"), wx.BITMAP_TYPE_PNG)
        self.play = SBitmapToggleButton(self.panel, -1, upbmp, (48, 48))
        self.play.SetUseFocusIndicator(False)
        self.play.SetBitmapDisabled(disbmp)

        self.play.Bind(wx.EVT_BUTTON, self.OnPlay)

        # The Record Button Is A Toggle Bitmap Button (SBitmapToggleButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "record.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "recorddisabled.png"), wx.BITMAP_TYPE_PNG)
        self.record = SBitmapToggleButton(self.panel, -1, upbmp, (48, 48))
        self.record.SetUseFocusIndicator(False)
        self.record.SetBitmapDisabled(disbmp)

        self.record.Bind(wx.EVT_BUTTON, self.OnRecord)

        # The Pause Button Is A Toggle Bitmap Button (SBitmapToggleButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "pause.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "pausedisabled.png"), wx.BITMAP_TYPE_PNG)
        self.pause = SBitmapToggleButton(self.panel, -1, upbmp, (48, 48))
        self.pause.SetUseFocusIndicator(False)
        self.pause.SetBitmapDisabled(disbmp)
        self.pause.Enable(False)

        self.pause.Bind(wx.EVT_BUTTON, self.OnPause)

        # The Stop Button Is A Simple Bitmap Button (SBitmapButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "stop.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "stopdisabled.png"), wx.BITMAP_TYPE_PNG)
        self.stop = SBitmapButton(self.panel, -1, upbmp, (48, 48))
        self.stop.SetUseFocusIndicator(False)
        self.stop.SetBitmapDisabled(disbmp)
        self.stop.Enable(False)

        self.stop.Bind(wx.EVT_BUTTON, self.OnStop)

        # The FFWD Button Is A Simple Bitmap Button (SBitmapButton)
        upbmp = wx.Bitmap(os.path.join(bitmapDir, "ffwd.png"), wx.BITMAP_TYPE_PNG)
        disbmp = wx.Bitmap(os.path.join(bitmapDir, "ffwddisabled.png"), wx.BITMAP_TYPE_PNG)
        self.ffwd = SBitmapButton(self.panel, -1, upbmp, (48, 48))
        self.ffwd.SetUseFocusIndicator(False)
        self.ffwd.SetBitmapDisabled(disbmp)

        self.ffwd.Bind(wx.EVT_BUTTON, self.OnFFWD)


    def BuildNineButtons(self):

        # We Build 9 Buttons With Different Colours And A Nice Text Rotation

        colours = [None, wx.BLUE, wx.RED, wx.GREEN, wx.Colour("Gold"),
                   wx.CYAN, wx.YELLOW,
                   wx.Colour("Orange"), wx.Colour("Magenta")]

        labels = ["These", "Are", "Some", "Nice", "Text", "Appended",
                  "To Different", "Buttons", "Nice Eh?"]

        fnt = self.GetFont()

        fonts = [fnt, wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD),
                 wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL),
                 wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True),
                 fnt, wx.Font(9, wx.FONTFAMILY_DECORATIVE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD),
                 wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Tahoma"),
                 fnt, wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True, "Verdana")]

        lcolours = [None, wx.WHITE, wx.Colour("Yellow"), wx.WHITE,
                    None, None, wx.BLUE, wx.WHITE, wx.WHITE]

        bsizer = wx.FlexGridSizer(3, 3, 5, 5)
        rotation = []

        for ii in range(9):

            btn = SButton(self.panel, -1, labels[ii])
            btn.SetButtonColour(colours[ii])
            btn.SetFont(fonts[ii])
            btn.SetLabelColour(lcolours[ii])
            btn.SetUseFocusIndicator(True)
            btn.SetAngleOfRotation(45*ii)
            rotation.append(45*ii)
            btn.Bind(wx.EVT_BUTTON, self.OnNineButtons)

            bsizer.Add(btn, 1, wx.EXPAND | wx.BOTTOM | wx.RIGHT, 5)

        bsizer.AddGrowableRow(0)
        bsizer.AddGrowableRow(1)
        bsizer.AddGrowableRow(2)
        bsizer.AddGrowableCol(0)
        bsizer.AddGrowableCol(1)
        bsizer.AddGrowableCol(2)

        self.buttonlabels = labels
        self.buttonrotation = rotation

        return bsizer


    def BuildMixedButtons(self):

        # Here We Build Some Buttons/Toggles With Different Properties
        # Notice That We Put Some Images Also For The "Selected" State
        # For A Button

        btsizer = wx.FlexGridSizer(2, 2, 5, 5)

        bmp = wx.Bitmap(os.path.join(bitmapDir, "italy.gif"), wx.BITMAP_TYPE_GIF)
        btn1 = SBitmapButton(self.panel, -1, bmp)
        bmp = wx.Bitmap(os.path.join(bitmapDir, "canada.gif"), wx.BITMAP_TYPE_GIF)
        btn1.SetBitmapSelected(bmp)
        btn1.Bind(wx.EVT_BUTTON, self.OnItalyCanada)

        bmp = wx.Bitmap(os.path.join(bitmapDir, "stop.png"), wx.BITMAP_TYPE_PNG)
        btn2 = SBitmapTextToggleButton(self.panel, -1, bmp, "Toggle!")
        bmp = wx.Bitmap(os.path.join(bitmapDir, "play.png"), wx.BITMAP_TYPE_PNG)
        btn2.SetBitmapSelected(bmp)
        btn2.Bind(wx.EVT_BUTTON, self.OnTogglePlayStop)

        btn3 = SButton(self.panel, -1, "Rotated")
        btn3.SetButtonColour(wx.Colour("Cyan"))
        btn3.SetLabelColour(wx.WHITE)
        btn3.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        btn3.SetAngleOfRotation(90)
        btn3.Bind(wx.EVT_BUTTON, self.OnRotated1)

        btn4 = SButton(self.panel, -1, "Button!")
        btn4.SetAngleOfRotation(45)
        btn4.Bind(wx.EVT_BUTTON, self.OnRotated1)

        btsizer.Add(btn1, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        btsizer.Add(btn2, 1, wx.EXPAND | wx.BOTTOM, 5)
        btsizer.Add(btn3, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        btsizer.Add(btn4, 1, wx.EXPAND)

        btsizer.AddGrowableRow(0)
        btsizer.AddGrowableRow(1)
        btsizer.AddGrowableCol(0)
        btsizer.AddGrowableCol(1)

        return btsizer


    def BuildEllipticButtons(self):

        # Here We Build Elliptic Buttons. Elliptic Buttons Are Somewhat
        # More Hostiles To Handle, Probably Because My Implementation
        # Is Lacking Somewhere, But They Look Nice However.

        esizer = wx.FlexGridSizer(2, 2, 5, 5)

        btn1 = SButton(self.panel, -1, "Ellipse 1")
        btn1.SetEllipseAxis(2, 1)
        btn1.SetButtonColour(wx.RED)
        btn1.SetLabelColour(wx.WHITE)
        btn1.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        btn1.Bind(wx.EVT_BUTTON, self.OnEllipse)

        btn2 = SButton(self.panel, -1, "Ellipse 2")
        btn2.SetEllipseAxis(2, 3)
        btn2.SetAngleOfRotation(90)
        btn2.SetLabelColour(wx.BLUE)
        btn2.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True))
        btn2.Bind(wx.EVT_BUTTON, self.OnEllipse)

        bmp = wx.Bitmap(os.path.join(bitmapDir, "ffwd.png"), wx.BITMAP_TYPE_PNG)
        btn3 = SBitmapTextToggleButton(self.panel, -1, bmp, "FFWD")
        bmp = wx.Bitmap(os.path.join(bitmapDir, "rewind.png"), wx.BITMAP_TYPE_PNG)
        btn3.SetBitmapSelected(bmp)
        btn3.SetEllipseAxis(1.4, 1)
        btn3.Bind(wx.EVT_BUTTON, self.OnFFWDRewind)

        bmp = wx.Bitmap(os.path.join(bitmapDir, "round.png"), wx.BITMAP_TYPE_PNG)
        btn4 = SBitmapButton(self.panel, -1, bmp)
        btn4.SetEllipseAxis(1, 1.4)
        btn4.Bind(wx.EVT_BUTTON, self.OnRound)

        esizer.Add(btn1, 1, wx.EXPAND | wx.ALL, 5)
        esizer.Add(btn2, 1, wx.EXPAND | wx.ALL, 5)
        esizer.Add(btn3, 1, wx.EXPAND | wx.ALL, 5)
        esizer.Add(btn4, 1, wx.EXPAND | wx.ALL, 5)

        esizer.AddGrowableRow(0)
        esizer.AddGrowableRow(1)
        esizer.AddGrowableCol(0)
        esizer.AddGrowableCol(1)

        return esizer


    def CreateMenuBar(self):

        file_menu = wx.Menu()

        AS_EXIT = wx.NewId()
        file_menu.Append(AS_EXIT, "&Exit")
        self.Bind(wx.EVT_MENU, self.OnClose, id=AS_EXIT)

        help_menu = wx.Menu()

        AS_ABOUT = wx.NewId()
        help_menu.Append(AS_ABOUT, "&About...")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=AS_ABOUT)

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        return menu_bar


    def OnClose(self, event):

        self.Destroy()


    def OnAbout(self, event):

        msg = "This Is The About Dialog Of The ShapedButton Demo.\n\n" + \
              "Author: Andrea Gavana @ 18 Oct 2005\n\n" + \
              "Please Report Any Bug/Requests Of Improvements\n" + \
              "To Me At The Following Adresses:\n\n" + \
              "andrea.gavana@agip.it\n" + "andrea_gavana@tin.it\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "ShapedButton Demo",
                               wx.OK | wx.ICON_INFORMATION)

        dlg.ShowModal()
        dlg.Destroy()


    def OnRewind(self, event):

        self.eventtext.SetLabel("Rewind Button!")
        self.eventtext.Refresh()

        event.Skip()


    def OnPlay(self, event):

        if not event.GetIsDown():
            self.eventtext.SetLabel('Press "Stop" To Stop The Music!')
            self.eventtext.Refresh()
            self.play.SetToggle(True)
            return

        self.eventtext.SetLabel("We Started To Play")
        self.eventtext.Refresh()

        self.stop.Enable(True)
        self.pause.Enable(True)
        self.rewind.Enable(False)
        self.ffwd.Enable(False)
        self.record.Enable(False)

        event.Skip()


    def OnRecord(self, event):

        if not event.GetIsDown():
            self.eventtext.SetLabel("Recording Stopped")
            self.eventtext.Refresh()
            self.stop.Enable(False)
            self.pause.Enable(False)
            self.rewind.Enable(True)
            self.ffwd.Enable(True)
            self.play.Enable(True)

            event.Skip()
            return

        self.eventtext.SetLabel("What Are You Recording? ;-)")
        self.eventtext.Refresh()
        self.stop.Enable(True)
        self.pause.Enable(True)
        self.rewind.Enable(False)
        self.ffwd.Enable(False)
        self.play.Enable(False)

        event.Skip()


    def OnPause(self, event):

        if event.GetIsDown():
            self.eventtext.SetLabel("Pausing Play Or Recording...")
        else:
            self.eventtext.SetLabel("Playing After A Pause...")

        self.eventtext.Refresh()

        event.Skip()


    def OnStop(self, event):

        self.eventtext.SetLabel("Everything Stopped")
        self.eventtext.Refresh()

        self.stop.Enable(False)
        self.pause.Enable(False)
        self.rewind.Enable(True)
        self.ffwd.Enable(True)
        self.play.Enable(True)
        self.record.Enable(True)
        self.play.SetToggle(False)
        self.pause.SetToggle(False)
        self.record.SetToggle(False)

        event.Skip()


    def OnFFWD(self, event):

        self.eventtext.SetLabel("Fast Forward Button!")
        self.eventtext.Refresh()

        event.Skip()


    def OnNineButtons(self, event):

        btn = event.GetEventObject()
        label = btn.GetLabel()

        mystr = "Button: " + label + ", Rotation: " + \
                str(int(btn.GetAngleOfRotation())) + " Degrees"

        self.eventtext.SetLabel(mystr)
        self.eventtext.Refresh()

        event.Skip()


    def OnItalyCanada(self, event):

        self.eventtext.SetLabel("Italy VS Canada ;-)")
        self.eventtext.Refresh()

        event.Skip()


    def OnTogglePlayStop(self, event):

        if event.GetIsDown():
            label = "You Started To Play!"
        else:
            label = "Why Did You Stop The Music? ;-)"

        self.eventtext.SetLabel(label)
        self.eventtext.Refresh()

        event.Skip()


    def OnRotated1(self, event):

        btn = event.GetEventObject()
        label = btn.GetLabel()
        angle = int(btn.GetAngleOfRotation())

        mystr = "You Clicked: " + label + ", Rotated By: " + str(angle) + " Degrees"
        self.eventtext.SetLabel(mystr)
        self.eventtext.Refresh()

        btn.SetAngleOfRotation(random.randint(0, 359))

        event.Skip()


    def OnEllipse(self, event):

        btn = event.GetEventObject()
        label = btn.GetLabel()
        angle = int(btn.GetAngleOfRotation())

        mystr = "Do You Like Them? (Rotation = " + str(angle) + " Degrees)"
        self.eventtext.SetLabel(mystr)
        self.eventtext.Refresh()

        event.Skip()


    def OnFFWDRewind(self, event):

        btn = event.GetEventObject()

        if event.GetIsDown():
            label = "Let's Rewind Everything"
            btn.SetLabel("REW")
        else:
            label = "Go To The End Of The Tape!"
            btn.SetLabel("FFWD")

        self.eventtext.SetLabel(label)
        self.eventtext.Refresh()

        event.Skip()


    def OnRound(self, event):

        self.eventtext.SetLabel("I Have Nothing To Say Here ;-)")
        self.eventtext.Refresh()

        event.Skip()


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test ShapedButton ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = ShapedButtonDemo(self, self.log)
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


overview = docs


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

