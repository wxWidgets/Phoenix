import imp_unittest, unittest
import wtc
import wx

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')
pngFile2 = os.path.join(os.path.dirname(__file__), 'pointy.png')


#---------------------------------------------------------------------------

class statbmp_Tests(wtc.WidgetTestCase):

    def test_statbmpCtor(self):
        bmp = wx.Bitmap(pngFile)
        sb = wx.StaticBitmap(self.frame, -1, bmp)
        sb = wx.StaticBitmap(self.frame, label=bmp)
        
        
    def test_statbmpDefaultCtor(self):
        bmp = wx.Bitmap(pngFile)
        sb = wx.StaticBitmap()
        sb.Create(self.frame, -1, bmp)
        

    def test_statbmpProperties(self):
        bmp = wx.Bitmap(pngFile)
        sb = wx.StaticBitmap(self.frame, label=bmp)
        
        sb.Icon
        sb.Bitmap
        sb.Bitmap = wx.Bitmap(pngFile2)
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
