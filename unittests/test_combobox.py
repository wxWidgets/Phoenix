import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class ComboBoxTests(wtc.WidgetTestCase):
    
    def test_ComboBoxCtors(self):
        c = wx.ComboBox(self.frame, value='value', choices="one two three four".split())
        c = wx.ComboBox(self.frame, -1, 'value', wx.Point(10,10), wx.Size(80,-1), 
                      "one two three four".split(), 0)
        c = wx.ComboBox(self.frame, -1, "", (10,10), (80,-1), "one two three four".split(), 0)
        
        self.assertTrue(c.GetCount() == 4)
        
        
    def test_ComboBoxDefaultCtor(self):
        c = wx.ComboBox()
        c.Create(self.frame, value="value", choices="one two three four".split())

        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
