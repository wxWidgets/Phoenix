import unittest
from unittests import wtc
import wx
import wx.html

import os
helpPath = os.path.join(os.path.dirname(__file__), 'helpfiles')

#---------------------------------------------------------------------------

class helpfrm_Tests(wtc.WidgetTestCase):

    def test_helpfrm1(self):
        data = wx.html.HtmlHelpData()
        data.AddBook(os.path.join(helpPath, 'testing.hhp'))
        data.AddBook(os.path.join(helpPath, 'another.hhp'))

        hc = wx.html.HtmlHelpController()
        frm = wx.html.HtmlHelpFrame(data)
        frm.SetController(hc)
        frm.Create(self.frame, -1)
        frm.Show()

        self.myYield()
        frm.Close()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
