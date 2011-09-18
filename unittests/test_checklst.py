import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class CheckListBoxTests(wtc.WidgetTestCase):
    
    def test_CheckBoxCtors(self):
        c = wx.CheckListBox(self.frame, choices="one two three four".split())
        c = wx.CheckListBox(self.frame, -1, wx.Point(10,10), wx.Size(80,-1),
                            "one two three four".split(),)                
                
        
    def test_CheckListBoxDefaultCtor(self):
        c = wx.CheckListBox()
        c.Create(self.frame, choices="one two three four".split())

        
      
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
