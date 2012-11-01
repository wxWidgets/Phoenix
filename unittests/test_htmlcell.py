import imp_unittest, unittest
import wtc
import wx
import wx.html


#---------------------------------------------------------------------------

class htmlcell_Tests(wtc.WidgetTestCase):

    def test_htmlcell1(self):
        c = wx.html.HtmlCell()

    def test_htmlcell2(self):
        obj = wx.html.HtmlSelection()
        
    def test_htmlcell3(self):
        obj = wx.html.HtmlRenderingState()
        
    def test_htmlcell4(self):
        obj = wx.html.HtmlRenderingInfo()
        
    def test_htmlcell5(self):
        obj = wx.html.HtmlContainerCell(None)
        
    def test_htmlcell6(self):
        obj = wx.html.HtmlLinkInfo()
        
    def test_htmlcell7(self):
        obj = wx.html.HtmlColourCell(wx.BLACK)
        
    def test_htmlcell8(self):
        obj = wx.html.HtmlWidgetCell(self.frame)
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
