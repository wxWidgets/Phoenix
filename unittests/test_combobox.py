import unittest
from unittests import wtc
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

    def test_comboboxHasCut(self):
        c = wx.ComboBox(self.frame, value='value', choices="one two three four".split())
        c.Cut  # is it there?  It was lost, once upon a time

    def test_comboboxSetSelection(self):
        c = wx.ComboBox(self.frame, value='value', choices="one two three four".split())
        # Are both overloads present?
        c.SetSelection(2)     # select an item
        c.SetSelection(1,3)   # select a range of text

    def test_comboboxTextSelection(self):
        c = wx.ComboBox(self.frame, value='value', choices="one two three four".split())
        c.SetTextSelection(2,4)
        self.assertEqual(c.GetTextSelection(), (2,4))

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
