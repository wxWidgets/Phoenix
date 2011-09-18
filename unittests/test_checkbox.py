import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class CheckBoxTests(wtc.WidgetTestCase):
    
    def test_CheckBoxCtors(self):
        c = wx.CheckBox(self.frame, label="checkbox")
        c = wx.CheckBox(self.frame, -1, "checkbox", wx.Point(10,10), wx.Size(80,-1))                
                
        
    def test_CheckBoxDefaultCtor(self):
        c = wx.CheckBox()
        c.Create(self.frame, label="checkbox")

        
      
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
