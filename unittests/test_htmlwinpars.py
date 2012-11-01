import imp_unittest, unittest
import wtc
import wx
import wx.html

#---------------------------------------------------------------------------

class htmlwinpars_Tests(wtc.WidgetTestCase):

    def test_htmlwinpars1(self):
        obj = wx.html.HtmlWinParser()
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
