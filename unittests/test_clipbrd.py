import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class clipbrd_Tests(wtc.WidgetTestCase):

    def test_clipbrd1(self):
        # copy
        data1 = wx.TextDataObject('This is some data.')
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data1)
            wx.TheClipboard.Close()
              
        # paste  
        data2 = wx.TextDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(data2)
            wx.TheClipboard.Close()
        
        self.assertEqual(data2.GetText(), 'This is some data.')
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
