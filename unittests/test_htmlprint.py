import imp_unittest, unittest
import wtc
import wx
import wx.html

#---------------------------------------------------------------------------

class htmlprint_Tests(wtc.WidgetTestCase):

    def test_htmlprint1(self):        
        size = (100,100)
        bmp = wx.Bitmap(*size)
        dc = wx.MemoryDC(bmp)
        
        obj = wx.html.HtmlDCRenderer()
        obj.SetDC(dc)
        obj.SetSize(*size)
        obj.SetHtmlText('<body><h1>Hello World</h1></body>')
        
        obj.Render(0,0, [])
        
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
