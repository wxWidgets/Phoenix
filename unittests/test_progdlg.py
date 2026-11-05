import unittest
from unittests import wtc
import wx
import sys

#---------------------------------------------------------------------------

class progdlg_Tests(wtc.WidgetTestCase):

    @unittest.skipIf(sys.platform.startswith("win"), "not running on Windows")
    def test_progdlg1(self):
        max = 50
        dlg = wx.GenericProgressDialog("Progress dialog example",
                                "An informative message",
                                parent=self.frame,
                                maximum=max)

        keepGoing = True
        count = 0

        while keepGoing and count < max:
            count += 1
            #wx.MilliSleep(250)
            self.myYield()
            (keepGoing, skip) = dlg.Update(count)

        dlg.Destroy()

    @unittest.skipIf(sys.platform.startswith("win"), "not running on Windows")
    def test_progdlg2(self):
        max = 50
        dlg = wx.ProgressDialog("Progress dialog example",
                                "An informative message",
                                parent=self.frame,
                                maximum=max)

        keepGoing = True
        count = 0

        while keepGoing and count < max:
            count += 1
            #wx.MilliSleep(250)
            self.myYield()
            (keepGoing, skip) = dlg.Update(count)

        dlg.Destroy()

    def test_progdlgSkip(self):
        dlg = wx.GenericProgressDialog("Progress dialog example",
                                       "An informative message",
                                       parent=self.frame,
                                       style=wx.PD_CAN_SKIP)
        assert dlg.Update(1) == (True, False)
        assert dlg.Pulse() == (True, False)

        skipButton = [w for w in dlg.GetChildren()
                      if isinstance(w, wx.Button) and w.GetLabelText() == "Skip"][0]
        dlg.ProcessEvent(wx.CommandEvent(wx.wxEVT_BUTTON, skipButton.GetId()))
        assert dlg.WasSkipped()
        assert dlg.Update(2) == (True, True)
        assert not dlg.WasSkipped()
        assert dlg.Update(3) == (True, False)

        dlg.Destroy()

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
