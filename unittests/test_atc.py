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

class ATCFrame(wx.Frame, atc.TestWidget):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.NewId(), "ATC Test Frame")
        atc.TestWidget.__init__(self)

    def test_pass(self):
        self.testPassed()

    @unittest.expectedFailure
    def test_fail(self):
        self.testFailed("Deliberate test failure")

atc_BasicTests = atc.createATC(ATCPanel)

if __name__ == "__main__":
    unittest.main()
