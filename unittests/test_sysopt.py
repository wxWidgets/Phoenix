import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class sysopt_Tests(wtc.WidgetTestCase):

    def test_sysopt1(self):
        opt = 'exit-on-assert'
        wx.SystemOptions.HasOption(opt)
        val = wx.SystemOptions.GetOption(opt)
        wx.SystemOptions.GetOptionInt(opt)
        wx.SystemOptions.SetOption(opt, 123)
        wx.SystemOptions.SetOption(opt, val)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
