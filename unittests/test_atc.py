from unittests import atc
import wx
import unittest

class ATCPanel(wx.Panel, atc.TestWidget):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.NewId())
        atc.TestWidget.__init__(self)

    def test_pass(self):
        print("Passing test")
        self.TestDone()

    @unittest.expectedFailure
    @atc.TestCritical
    def test_fail(self):
        print("Failing test")
        self.TestDone(False)

    @unittest.expectedFailure
    @atc.TestCritical
    def test_abort(self):
        print("Aborting test case")
        assert 0

    @unittest.skip("reasons")
    def test_skip(self):
        return


testcase = atc.CreateATC(ATCPanel)

if __name__ == "__main__":
    unittest.main()
