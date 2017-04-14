import unittest
from unittests import wtc
import wx
import wx.html

import os
helpPath = os.path.join(os.path.dirname(__file__), 'helpfiles')


#---------------------------------------------------------------------------

class helpwnd_Tests(wtc.WidgetTestCase):

    def test_helpwnd1(self):
        hc = wx.html.HtmlHelpController(wx.html.HF_EMBEDDED)
        hw = wx.html.HtmlHelpWindow()
        hc.SetHelpWindow(hw)
        hw.Create(self.frame)
        hc.AddBook(os.path.join(helpPath, 'testing.hhp'))
        hc.AddBook(os.path.join(helpPath, 'another.hhp'))

        self.frame.SendSizeEvent()
        self.waitFor(50)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
