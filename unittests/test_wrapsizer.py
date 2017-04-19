import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class wrapsizer_Tests(wtc.WidgetTestCase):

    def test_wrapsize(self):
        ws = wx.WrapSizer()
        ws.Add(wx.Panel(self.frame))
        ws.Add(wx.Panel(self.frame))
        ws.Add(wx.Panel(self.frame))


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
