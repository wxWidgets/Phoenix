import unittest
from unittests import wtc
import wx
import wx.html

import os
helpPath = os.path.join(os.path.dirname(__file__), 'helpfiles')

#---------------------------------------------------------------------------

class helpctrl_Tests(wtc.WidgetTestCase):

    def test_helpctrl1(self):
        hc = wx.html.HtmlHelpController(parentWindow=self.frame)
        hc.AddBook(os.path.join(helpPath, 'testing.hhp'))
        hc.AddBook(os.path.join(helpPath, 'another.hhp'))
        hc.SetShouldPreventAppExit(False)

        hc.DisplayContents()
        self.myYield()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
