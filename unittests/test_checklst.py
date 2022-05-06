import unittest
from unittests import wtc
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

    def test_pyMethods1(self):
        c = wx.CheckListBox(self.frame, choices="one two three four".split())
        self.assertTrue(callable(c.GetChecked))
        self.assertTrue(callable(c.GetCheckedStrings))
        self.assertTrue(callable(c.SetChecked))
        self.assertTrue(callable(c.SetCheckedStrings))

    def test_pyMethods2(self):
        c = wx.CheckListBox(self.frame, choices="one two three four".split())
        c.SetCheckedItems([1,3])
        self.assertTrue(set(c.GetCheckedItems()) == set([1,3]))
        c.SetCheckedStrings(['one', 'two'])
        self.assertTrue(set(c.GetCheckedStrings()) == set(['one', 'two']))
        self.assertTrue(set(c.GetCheckedItems()) == set([0,1]))

    def test_pyProperties(self):
        c = wx.CheckListBox(self.frame, choices="one two three four".split())
        c.SetCheckedItems([1,3])
        self.assertTrue(set(c.CheckedItems) == set([1,3]))

        c.CheckedItems = [2]
        self.assertTrue(set(c.CheckedItems) == set([2]))

        c.SetCheckedStrings(['one', 'two'])
        self.assertTrue(set(c.CheckedStrings) == set(['one', 'two']))

        c.CheckedStrings = ['three']
        self.assertTrue(set(c.GetCheckedItems()) == set([2]))

    def test_GetSelections(self):
        c = wx.CheckListBox(
            self.frame,
            choices="one two three four".split(),
            style=wx.LB_EXTENDED,
        )
        self.assertEqual(c.GetSelections(), [])
        c.SetSelection(2)
        self.assertEqual(c.GetSelections(), [2])


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
