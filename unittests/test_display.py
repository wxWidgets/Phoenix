import unittest
from unittests import wtc
import wx
#import os; print(os.getpid())

#---------------------------------------------------------------------------

class display_Tests(wtc.WidgetTestCase):

    def test_display(self):
        d = wx.Display()
        r = d.GetClientArea()
        c = wx.Display.GetCount()
        self.assertTrue(c >= 1)
        m = d.GetModes()
        self.assertTrue(isinstance(m, wx.ArrayVideoModes))
        self.assertTrue(len(m) > 0)
        vm = m[0]
        self.assertTrue(isinstance(vm, wx.VideoMode))
        self.assertTrue(vm.IsOk())

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
