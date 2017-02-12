from unittests import atc
import wx
import unittest

class PanelColorChangeTester(wx.Panel, atc.TestWidget):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.NewId())
        atc.TestWidget.__init__(self)

        self.SetBackgroundColour(wx.BLUE)

    def test_pass(self):
        print("Passing test")
        self.TestDone()

    def test_fail(self):
        print("Failing test")
        self.TestDone(False)

    @atc.TestDependent
    def test_abort(self):
        print("Aborting test case")
        raise AttributeError("Unbound attribute error")


testcase = atc.CreateATC(PanelColorChangeTester)

if __name__ == "__main__":
    testcase.test_abort(testcase)
    unittest.main()
    