#!/usr/bin/env python

# ----------------------------------------------------------------------------
# BalloonTip Demo Implementation
#
# This Demo Shows How To Use The BalloonTip Control, With Different Styles
# And Behaviors.
# ----------------------------------------------------------------------------


import wx
from wx.lib.stattext import GenStaticText as StaticText
from wx.lib.buttons import GenBitmapButton as BitmapButton
from wx.adv import TaskBarIcon as TaskBarIcon

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import balloontip as BT
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.balloontip as BT

import images

ArtIDs = [ "wx.ART_HELP_PAGE",
           "wx.ART_GO_FORWARD",
           "wx.ART_FILE_OPEN",
           "wx.ART_HELP",
           "wx.ART_ERROR",
           "wx.ART_QUESTION",
           "wx.ART_WARNING",
           "wx.ART_INFORMATION",
           "wx.ART_HELP",
           ]


# ----------------------------------------------------------------------------
# Beginning Of BalloonTip Demo
# ----------------------------------------------------------------------------

class BalloonTipDemo(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent, title="BalloonTip wxPython Demo ;-)")

        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([-2, -1])
        # statusbar fields
        statusbar_fields = [("Welcome To WxPython " + wx.VERSION_STRING),
                            ("BalloonTip Demo")]

        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)

        self.SetIcon(images.Mondrian.GetIcon())
        self.SetMenuBar(self.CreateMenuBar())

        panel = wx.Panel(self, -1)

        mainsizer = wx.FlexGridSizer(3, 4, hgap=2, vgap=2)

        # Add A Button
        button = wx.Button(panel, -1, "Press Me!")
        # Add A TextCtrl
        textctrl = wx.TextCtrl(panel, -1, "I Am A TextCtrl")
        # Add A CheckBox
        checkbox = wx.CheckBox(panel, -1, "3-State Checkbox",
                               style=wx.CHK_3STATE | wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        samplelist=['One', 'Two', 'Three', 'Four', 'Kick', 'The', 'Demo', 'Out',
                    'The', 'Door', ';-)']
        # Add A Choice
        choice = wx.Choice(panel, -1, choices = samplelist)
        # Add A Gauge
        gauge = wx.Gauge(panel, -1, 50, style=wx.GA_SMOOTH)
        # Add A ListBox
        listbox = wx.ListBox(panel, -1, choices=samplelist, style=wx.LB_SINGLE)
        # Add A TreeCtrl
        isz = (16,16)
        treecontrol = wx.TreeCtrl(panel, -1)
        il = wx.ImageList(isz[0], isz[1])
        fldridx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, isz))
        fileidx = il.Add(wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_OTHER, isz))
        treecontrol.SetImageList(il)
        self.il = il
        root = treecontrol.AddRoot("ROOT")
        treecontrol.SetItemData(root, None)
        treecontrol.SetItemImage(root, fldridx, wx.TreeItemIcon_Normal)
        treecontrol.SetItemImage(root, fldropenidx, wx.TreeItemIcon_Expanded)
        for ii in range(11):
            child = treecontrol.AppendItem(root, samplelist[ii])
            treecontrol.SetItemData(child, None)
            treecontrol.SetItemImage(child, fldridx, wx.TreeItemIcon_Normal)
            treecontrol.SetItemImage(child, fldropenidx, wx.TreeItemIcon_Selected)

        # Add A Slider
        slider = wx.Slider(panel, -1, 25, 1, 100,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)# | wx.SL_LABELS)
        slider.SetTickFreq(5)
        # Add Another TextCtrl
        textctrl2 = wx.TextCtrl(panel, -1, "Another TextCtrl")
        # Add A GenStaticText
        statictext = StaticText(panel, -1, "Hello World!")
        statictext.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS,
                                      wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False))
        bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION,
                                       wx.ART_TOOLBAR, (16,16))
        # Add A GenBitmapButton
        bitmapbutton = BitmapButton(panel, -1, bmp)
        button2 = wx.Button(panel, -1, "Disable BalloonTip")

        tbicon = TaskBarIcon()
        tbicon.SetIcon(images.Mondrian.GetIcon())

        controls = list(panel.GetChildren())
        controls.append(tbicon)
        self.tbicon = tbicon

        # Add The Controls To The Main FlexGridSizer
        mainsizer.Add(button, 0, wx.EXPAND | wx.ALL, 10)
        mainsizer.Add(textctrl, 0, wx.EXPAND | wx.ALL, 10)
        mainsizer.Add(checkbox, 0, wx.EXPAND | wx.ALL, 10)
        mainsizer.Add(choice, 0, wx.EXPAND | wx.ALL, 10)
        mainsizer.Add(gauge, 0, wx.ALL, 10)
        mainsizer.Add(listbox, 0, wx.EXPAND | wx.ALL, 10)
        mainsizer.Add(treecontrol, 0, wx.EXPAND, wx.ALL, 10)
        mainsizer.Add(slider, 0, wx.ALL, 10)
        mainsizer.Add(textctrl2, 0, wx.ALL, 10)
        mainsizer.Add(statictext, 0, wx.EXPAND | wx.ALL, 10)
        mainsizer.Add(bitmapbutton, 0, wx.ALL, 10)
        mainsizer.Add(button2, 0, wx.ALL, 10)

        panel.SetSizer(mainsizer)
        mainsizer.Layout()

        # Declare The BalloonTip Background Colours
        bgcolours = [None, wx.WHITE, wx.GREEN, wx.BLUE, wx.CYAN, wx.RED, None, None,
                     wx.LIGHT_GREY, None, wx.WHITE, None, None]

        # Declare The BalloonTip Top-Left Icons
        icons = []
        for ii in range(4):
            bmp = wx.ArtProvider.GetBitmap(eval(ArtIDs[ii]), wx.ART_TOOLBAR, (16,16))
            icons.append(bmp)

        icons.extend([None]*5)

        for ii in range(4, 9):
            bmp = wx.ArtProvider.GetBitmap(eval(ArtIDs[ii]), wx.ART_TOOLBAR, (16,16))
            icons.append(bmp)

        # Declare The BalloonTip Top Titles
        titles = ["Button Help", "Texctrl Help", "CheckBox Help", "Choice Help",
                  "Gauge Help", "", "", "Read Me Carefully!", "SpinCtrl Help",
                  "StaticText Help", "BitmapButton Help", "Button Help", "Taskbar Help"]

        fontone = wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)
        fonttwo = wx.Font(14, wx.FONTFAMILY_SCRIPT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False)
        fontthree = wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False)
        fontfour = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)

        # Declare The BalloonTip Top Titles Fonts
        titlefonts = [None, None, fontone, None, fonttwo, fontthree, None, None,
                      None, fontfour, fontthree, None, None]

        # Declare The BalloonTip Top Titles Colours
        titlecolours = [None, None, wx.WHITE, wx.YELLOW, None, wx.WHITE,
                        wx.BLUE, wx.RED, None, None, wx.LIGHT_GREY, None, None]

        # Declare The BalloonTip Messages
        msg1 = "This Is The Default BalloonTip Window\nYou Can Customize It! "\
               "Look At The Demo!"
        msg2 = "You Can Change The Background Colour\n Of The Balloon Window."
        msg3 = "You Can Also Change The Font And The\nColour For The Title."
        msg4 = "I Have Nothing Special To Suggest!\n\nWelcome To wxPython " + \
               wx.VERSION_STRING + " !"
        msg5 = "What About If I Don't Want The Icon?\nNo Problem!"
        msg6 = "I Don't Have The Icon Nor The Title.\n\nDo You Love Me Anyway?"
        msg7 = "Some Comments On The Window Shape:\n\n- BT_ROUNDED: Creates A "\
               "Rounded Rectangle;\n- BT_RECTANGLE: Creates A Rectangle.\n"
        msg8 = "Some Comments On The BalloonTip Style:\n\n"\
               "BT_LEAVE: The BalloonTip Is Destroyed When\nThe Mouse Leaves"\
               "The Target Widget;\n\nBT_CLICK: The BalloonTip Is Destroyed When\n"\
               "You Click Any Region Of The BalloonTip;\n\nBT_BUTTON: The BalloonTip"\
               " Is Destroyed When\nYou Click On The Top-Right Small Button."
        msg9 = "Some Comments On Delay Time:\n\nBy Default, The Delay Time After Which\n"\
               "The BalloonTip Is Destroyed Is Very Long.\nYou Can Change It By Using"\
               " The\nSetEndDelay() Method."
        msg10 = "I Have Nothing Special To Suggest!\n\nRead Me FAST, You Have Only 3 "\
                "Seconds!"
        msg11 = "I Hope You Will Enjoy BalloonTip!\nIf This Is The Case, Please\n"\
                "Post Some Comments On wxPython\nMailing List!"
        msg12 = "This Button Enable/Disable Globally\nThe BalloonTip On Your Application."
        msg13 = "This Is A BalloonTip For The\nTaskBar Icon Of Your Application.\n"\
                "All The Styles For BalloonTip Work."

        messages = [msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9, msg10,
                    msg11, msg12, msg13]

        # Declare The BalloonTip Tip Messages Colours
        messagecolours = [None, None, None, wx.WHITE, wx.BLUE,
                          None, wx.BLUE, None, None, wx.RED, wx.GREEN,
                          wx.BLUE, None]

        fontone = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, True)
        fonttwo = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL, False)
        fontthree = wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, True)

        # Declare The BalloonTip Tip Messages Fonts
        messagefonts = [None, None, None, fontone, None, None, fonttwo, None,
                       fontthree, None, None, None, None]

        # Declare The BalloonTip Frame Shapes
        windowshapes = [BT.BT_ROUNDED, BT.BT_RECTANGLE, BT.BT_ROUNDED, BT.BT_RECTANGLE,
                        BT.BT_ROUNDED, BT.BT_RECTANGLE, BT.BT_ROUNDED, BT.BT_ROUNDED,
                        BT.BT_ROUNDED, BT.BT_RECTANGLE, BT.BT_ROUNDED, BT.BT_RECTANGLE, BT.BT_RECTANGLE]

        # Declare The BalloonTip Destruction Style
        tipstyles = [BT.BT_LEAVE, BT.BT_CLICK, BT.BT_BUTTON, BT.BT_LEAVE, BT.BT_CLICK,
                       BT.BT_LEAVE, BT.BT_CLICK, BT.BT_BUTTON, BT.BT_BUTTON, BT.BT_CLICK,
                       BT.BT_LEAVE, BT.BT_LEAVE, BT.BT_BUTTON]

        # Set The Targets/Styles For The BalloonTip
        for ii, widget in enumerate(controls):
            tipballoon = BT.BalloonTip(topicon=icons[ii], toptitle=titles[ii],
                                       message=messages[ii], shape=windowshapes[ii],
                                       tipstyle=tipstyles[ii])
            # Set The Target
            tipballoon.SetTarget(widget)
            # Set The Balloon Colour
            tipballoon.SetBalloonColour(bgcolours[ii])
            # Set The Font For The Top Title
            tipballoon.SetTitleFont(titlefonts[ii])
            # Set The Colour For The Top Title
            tipballoon.SetTitleColour(titlecolours[ii])
            # Set The Font For The Tip Message
            tipballoon.SetMessageFont(messagefonts[ii])
            # Set The Colour For The Tip Message
            tipballoon.SetMessageColour(messagecolours[ii])
            # Set The Delay After Which The BalloonTip Is Created
            tipballoon.SetStartDelay(1000)
            if ii == 9:
                # Set The Delay After Which The BalloonTip Is Destroyed
                tipballoon.SetEndDelay(3000)

        # Store The Last BalloonTip Reference To Enable/Disable Globall The
        # BalloonTip. You Can Store Any Of Them, Not Necessarily The Last One.
        self.lasttip = tipballoon
        self.gauge = gauge
        self.count = 0

        button2.Bind(wx.EVT_BUTTON, self.OnActivateBalloon)
        self.Bind(wx.EVT_IDLE, self.IdleHandler)

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        frameSizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        frameSizer.Layout()
        self.Fit()

        self.CenterOnParent()


    def IdleHandler(self, event):

        self.count = self.count + 1

        if self.count >= 50:
            self.count = 0

        self.gauge.SetValue(self.count)


    def CreateMenuBar(self):

        # Make a menubar
        file_menu = wx.Menu()
        help_menu = wx.Menu()

        TEST_QUIT = wx.NewIdRef()
        TEST_ABOUT = wx.NewIdRef()

        file_menu.Append(TEST_QUIT, "&Exit")
        help_menu.Append(TEST_ABOUT, "&About")

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&File")
        menu_bar.Append(help_menu, "&Help")

        self.Bind(wx.EVT_MENU, self.OnAbout, id=TEST_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=TEST_QUIT)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        return menu_bar


    def OnQuit(self, event):

        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        self.Destroy()


    def OnAbout(self, event):

        msg = "This is the about dialog of the BalloonTip demo.\n\n" + \
              "Author: Andrea Gavana @ 29 May 2005\n\n" + \
              "Please report any bug/requests or improvements\n" + \
              "to me at the following addresses:\n\n" + \
              "andrea.gavana@agip.it\n" + "andrea_gavana@tin.it\n\n" + \
              "Welcome To wxPython " + wx.VERSION_STRING + "!!"

        dlg = wx.MessageDialog(self, msg, "BalloonTip Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Verdana"))
        dlg.ShowModal()
        dlg.Destroy()


    def OnActivateBalloon(self, event):

        button = event.GetEventObject()
        label = button.GetLabel()
        tips = self.lasttip

        if label == "Disable BalloonTip":
            button.SetLabel("Enable BalloonTip")
            tips.EnableTip(False)
        else:
            button.SetLabel("Disable BalloonTip")
            tips.EnableTip(True)

        event.Skip()


#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test BalloonTip ", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        self.win = BalloonTipDemo(self, self.log)
        self.win.Show(True)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------


overview = BT.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

