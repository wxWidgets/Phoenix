from unittests import atc
import wx
import unittest

class ATCPanel(wx.Panel, atc.TestWidget):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.NewId())
        atc.TestWidget.__init__(self)

    def test_pass(self):
        print("Passing test")
        self.testPassed()

    @unittest.expectedFailure
    def test_fail(self):
        print("Failing test")
        self.testFailed()

    @unittest.expectedFailure
    def test_abort(self):
        print("Aborting test case")
        assert 0

    @unittest.skip("reasons")
    def test_skip(self):
        self.testFailed("test_skip was invoked!")

    @unittest.skip("Takes too long for regular testing")
    def test_watchdog(self):
        print("Letting application loose")
        return

    def test_testcase(self):
        self.getTestCase()
        self.testPassed()

class ATCFrame(wx.Frame, atc.TestWidget):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.NewId(), "ATC Test Frame")
        atc.TestWidget.__init__(self)

    def test_pass(self):
        self.testPassed()

    @unittest.expectedFailure
    def test_fail(self):
        self.testFailed("Deliberate test failure")

class ATCDialog(wx.Dialog, atc.TestWidget):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title = "ATCDialog")
        atc.TestWidget.__init__(self)

    def test_pass(self):
        self.testPassed()

    @unittest.expectedFailure
    def test_fail(self):
        self.testFailed()

    def test_intlw(self):
        assert self in wx.GetTopLevelWindows(), "Dialog is not top level window"
        self.testPassed()

atc_BasicTests = atc.createATC(ATCPanel)
atc_FrameTests = atc.createATC(ATCFrame)
atc_DialogTests = atc.createATC(ATCDialog)


if __name__ == "__main__":
    unittest.main()
