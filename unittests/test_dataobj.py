import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class DataObjTests(wtc.WidgetTestCase):
    
    def test_DataFormat(self):
        fmt1 = wx.DataFormat('my custom format')
        fmt2 = wx.DataFormat(wx.DF_TEXT)
        self.assertTrue(fmt1 != fmt2)
        
        
    def test_DataFormatIDsExist(self):
        wx.DF_INVALID
        wx.DF_TEXT
        wx.DF_BITMAP
        wx.DF_METAFILE
        wx.DF_SYLK
        wx.DF_DIF
        wx.DF_TIFF
        wx.DF_OEMTEXT
        wx.DF_DIB
        wx.DF_PALETTE
        wx.DF_PENDATA
        wx.DF_RIFF
        wx.DF_WAVE
        wx.DF_UNICODETEXT
        wx.DF_ENHMETAFILE
        wx.DF_FILENAME
        wx.DF_LOCALE
        wx.DF_PRIVATE
        wx.DF_HTML
        wx.DF_MAX

        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
