#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from collections import OrderedDict

import wx
import wx.adv

import images

TipKindDict = OrderedDict([
    (0, ["TipKind_None",
         "Don't show any tip, the tooltip will be (roughly) rectangular."]),
    (1, ["TipKind_TopLeft",
         "Show a right triangle tip in the top left corner of the tooltip."]),
    (2, ["TipKind_Top",
         "Show an equilateral triangle tip in the middle of the tooltip top side."]),
    (3, ["TipKind_TopRight",
         "Show a right triangle tip in the top right corner of the tooltip."]),
    (4, ["TipKind_BottomLeft",
         "Show a right triangle tip in the bottom left corner of the tooltip."]),
    (5, ["TipKind_Bottom",
         "Show an equilateral triangle tip in the middle of the tooltip bottom side."]),
    (6, ["TipKind_BottomRight",
         "Show a right triangle tip in the bottom right corner of the tooltip."]),
    (7, ["TipKind_Auto",
         "Choose the appropriate tip shape and position automatically."]),
    ])

HEX = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

randBmps = ['phoenix_title.png','new_folder.png','lbroll.png','lbnews.png',
            'filesave.png','canada.gif','toucan.png','sttbutton.png']

randStrs = ['wxPython Rocks!', 'Python is the best', 'IOIOI\nOIOIO\n'*3, 'Test',
            'mooo','Fork','Class API','meh',':)']

def GetRandomColorHexStr():
    random.shuffle(HEX) # Order is random now
    # print(HEX)
    hexstr = ''
    for item in range(0,6):
        random.shuffle(HEX) # Twice for doubles and good luck :)
        # print(HEX[item])
        hexstr = hexstr + str(HEX[item])
    return '#%s'%hexstr


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.btn1 = wx.Button(self, -1, "Click me for a RichToolTip!", pos=(50,50))
        self.btn2 = wx.Button(self, -1, "RightClick me for a RichToolTip!", pos=(50,100))
        self.btn3 = wx.Button(self, -1, "MiddleClick me for a RichToolTip!", pos=(50,150))
        self.btn4 = wx.Button(self, -1, "Click me for a RichToolTip!", pos=(50,200))
        self.btn5 = wx.Button(self, -1, "Click me for a Gradient RichToolTip!", pos=(50,250))
        self.btn6 = wx.Button(self, -1, "Click me for a Random RichToolTip!", pos=(50,300))

        #Note: DONT use wx.EVT_LEFT_UP, it is crashy with RichToolTip
        self.btn1.Bind(wx.EVT_BUTTON, self.OnButton1)
        self.btn2.Bind(wx.EVT_RIGHT_UP, self.OnButton2)
        self.btn3.Bind(wx.EVT_MIDDLE_UP, self.OnButton3)
        self.btn4.Bind(wx.EVT_BUTTON, self.OnButton4)
        self.btn5.Bind(wx.EVT_BUTTON, self.OnButton5)
        self.btn6.Bind(wx.EVT_BUTTON, self.OnButton6)

    def OnButton1(self, event):
        tip = wx.adv.RichToolTip("Smile :)","Have you brushed your teeth today?")
        tip.SetIcon(images.Smiles.GetIcon())
        tip.ShowFor(self.btn1)

    def OnButton2(self, event):
        tip = wx.adv.RichToolTip("WARNING!","bla bla bla\nmeh\n*cough*\nmwaHaHaHa camelCase")
        tip.SetIcon(wx.ICON_WARNING)
        tip.SetBackgroundColour(wx.RED)
        tip.ShowFor(self.btn2)

    def OnButton3(self, event):
        tip = wx.adv.RichToolTip("White","maybe the most overused color...")
        tip.SetIcon(wx.ICON_INFORMATION)
        tip.SetBackgroundColour(col='#000000', colEnd='#FFFFFF')
        tip.SetTipKind(wx.adv.TipKind_TopRight)
        tip.ShowFor(self.btn3)

    def OnButton4(self, event):
        tip = wx.adv.RichToolTip("OK","Are you ...?")
        tip.SetIcon(wx.Icon('bitmaps/sttbutton.png'))
        tip.SetTipKind(wx.adv.TipKind_Bottom)
        font = wx.Font(48, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        tip.SetTitleFont(font)
        tip.SetBackgroundColour(wx.Colour(0,80,135))
        tip.SetTimeout(millisecondsTimeout=5000, millisecondsDelay=2)
        tip.ShowFor(self.btn4)

    def OnButton5(self, event):
        tip = wx.adv.RichToolTip("Ooooh","Nice Curves")
        tip.SetIcon(wx.Icon('bitmaps/view2.png'))
        tip.SetTipKind(wx.adv.TipKind_Top)
        tip.SetBackgroundColour(wx.Colour('#FFFFFF'),wx.Colour('#FF8000'))
        tip.ShowFor(self.btn5)

    def OnButton6(self, event):
        randint = random.randint(0,7)
        random.shuffle(randBmps)
        random.shuffle(randStrs)
        tip = wx.adv.RichToolTip("Randomly RichToolTip",randStrs[randint])
        tip.SetIcon(wx.Icon("bitmaps/%s" %randBmps[randint]))
        tip.SetTipKind(randint)
        tip.SetBackgroundColour(GetRandomColorHexStr())
        tip.ShowFor(self.btn6)

    # def OnChangeTipKind(self, event):


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = """\
Allows to show a tool tip with more customizations than ToolTip.

Currently this class has generic implementation that can be used with any
window and implements all the functionality but doesn't exactly match the
appearance of the native tooltips (even though it makes some efforts to use
the style most appropriate for the current platform) and a native MSW version
which can be only used with text controls and doesn't provide as much in the
way of customization. Because of this, it's inadvisable to customize the tooltips
unnecessarily as doing this turns off auto-detection of the native style in
the generic version and may prevent the native MSW version from being used at all.
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])


