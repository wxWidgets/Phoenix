import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class listbox_Tests(wtc.WidgetTestCase):

    def test_ComboBoxCtors(self):
        c = wx.ListBox(self.frame, choices="one two three four".split())
        c = wx.ListBox(self.frame, -1, wx.Point(10,10), wx.Size(80,-1),
                       "one two three four".split(), 0)
        c = wx.ListBox(self.frame, -1, (10,10), (80,-1), "one two three four".split(), 0)

        self.assertTrue(c.GetCount() == 4)


    def test_ComboBoxDefaultCtor(self):
        c = wx.ListBox()
        c.Create(self.frame, choices="one two three four".split())



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
