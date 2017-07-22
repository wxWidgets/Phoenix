import unittest
from unittests import wtc
import wx, wx.adv

#---------------------------------------------------------------------------

class commandlinkbutton_Tests(wtc.WidgetTestCase):

    def test_commandlinkbutton1(self):
        b = wx.adv.CommandLinkButton(self.frame, -1, "mainlabel", "note")

    def test_commandlinkbutton2(self):
        b = wx.adv.CommandLinkButton()
        b.Create(self.frame, -1, "mainlabel", "note")

    def test_commandlinkbutton3(self):
        b = wx.adv.CommandLinkButton(self.frame, -1, "mainlabel", "note")
        b.SetMainLabelAndNote("new main label", "new note")
        # properties
        b.Label
        b.MainLabel
        b.Note

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
