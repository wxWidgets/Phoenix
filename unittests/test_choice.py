import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class ChoiceTests(wtc.WidgetTestCase):

    def test_ChoiceCtors(self):
        c = wx.Choice(self.frame, choices="one two three four".split())
        c = wx.Choice(self.frame, -1, wx.Point(10,10), wx.Size(80,-1),
                      "one two three four".split(), 0)
        c = wx.Choice(self.frame, -1, (10,10), (80,-1), "one two three four".split(), 0)

        self.assertTrue(c.GetCount() == 4)


    def test_ChoiceDefaultCtor(self):
        c = wx.Choice()
        c.Create(self.frame, choices="one two three four".split())


    def test_ChoiceProperties(self):
        c = wx.Choice(self.frame, choices="one two three four".split())

        # do the properties exist?
        c.Columns
        c.Count
        c.CurrentSelection
        c.Selection


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
