import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class editlbox_Tests(wtc.WidgetTestCase):

    def test_editlbox1(self):
        wx.adv.EL_ALLOW_NEW
        wx.adv.EL_ALLOW_EDIT
        wx.adv.EL_ALLOW_DELETE
        wx.adv.EL_NO_REORDER
        wx.adv.EL_DEFAULT_STYLE

    def test_editlbox2(self):
        elb = wx.adv.EditableListBox(self.frame, label="EditableListBox")
        strings = "one two three four five".split()
        elb.SetStrings(strings)
        self.assertEqual(strings, elb.GetStrings())
        self.assertEqual(strings, elb.Strings)

    def test_editlbox3(self):
        elb = wx.adv.EditableListBox()
        elb.Create(self.frame, label="EditableListBox")
        strings = "one two three four five".split()
        elb.SetStrings(strings)
        self.assertEqual(strings, elb.GetStrings())
        self.assertEqual(strings, elb.Strings)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
