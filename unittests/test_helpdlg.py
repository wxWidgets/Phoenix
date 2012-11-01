import imp_unittest, unittest
import wtc
import wx
import wx.html

import os
helpPath = os.path.join(os.path.dirname(__file__), 'helpfiles')

#---------------------------------------------------------------------------

class helpdlg_Tests(wtc.WidgetTestCase):

    def test_helpdlg1(self):
        data = wx.html.HtmlHelpData()
        data.AddBook(os.path.join(helpPath, 'testing.hhp'))
        data.AddBook(os.path.join(helpPath, 'another.hhp'))
        dlg = wx.html.HtmlHelpDialog(data)
        
        self.myYield()
        dlg.Destroy()
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
