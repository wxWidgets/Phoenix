from unittests import atc
import wx
import unittest
import random

random.seed()

class PanelColorChangeTester(wx.Panel, atc.TestWidget):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.NewId())
        atc.TestWidget.__init__(self)

        self.SetBackgroundColour(wx.BLUE)

    def test_dummy(self):
        self.TestDone(True)

testcase = atc.CreateATC(PanelColorChangeTester)

if __name__ == "__main__":
    unittest.main()