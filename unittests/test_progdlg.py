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

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
