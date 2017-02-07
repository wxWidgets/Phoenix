from unittests import atc
import wx
import unittest

# the testception is strong with this one.
class FrameRestoreTester(atc.TestFrame):
    def __init__(self):
        atc.TestFrame.__init__(self)
        self.SetLabel("Frame Restore Test")

        # enforce a strict schedule
        self.schedule = ("iconize", "restore", "maximize", "restore")

    def test_iconize(self):
        self.Iconize()
        wx.CallLater(250, self.Ensure, "Iconized")

    def test_maximize(self):
        self.Maximize()
        wx.CallLater(250, self.Ensure, "Maximized")

    def test_restore(self):
        self.Restore()
        wx.CallLater(250, self.Ensure, "Restored")

    def Ensure(self, ensurable):
        if ensurable == "Iconized":
            self.Assert(self.IsIconized())
        elif ensurable == "Maximized":
            self.Assert(self.IsMaximized())
        elif ensurable == "Restored":
            self.Assert(not self.IsIconized())
            self.Assert(not self.IsMaximized())

        self.TestDone()

# unittest only finds classes at local module scope that derive
# from TestCase, ways around this should be investigated
tc = atc.ApplicationTestCase

# monkey wrench desired TestFrame class into the test case
tc._frame = FrameRestoreTester

if __name__ == "__main__":
    unittest.main()