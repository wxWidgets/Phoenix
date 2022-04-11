import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class busyinfo_Tests(wtc.WidgetTestCase):

    def test_busyinfo1(self):
        busy = wx.BusyInfo('This is a busy info message')
        self.waitFor(250)
        del busy


    def test_busyinfo2(self):
        with wx.BusyInfo('This is a busy info message'):
            self.waitFor(250)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
