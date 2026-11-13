import unittest
import warnings
from unittests import wtc
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin, TextEditMixin

#---------------------------------------------------------------------------

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            CheckListCtrlMixin.__init__(self)
        self.checked = []

    def OnCheckItem(self, index, flag):
        self.checked.append((index, flag))


class EditableListCtrl(wx.ListCtrl, TextEditMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT)
        TextEditMixin.__init__(self)


class lib_mixins_listctrl_Tests(wtc.WidgetTestCase):

    def test_lib_mixins_listctrlCheckItem(self):
        lc = CheckListCtrl(self.frame)
        lc.InsertColumn(0, 'name')
        for i in range(3):
            lc.InsertItem(i, f'item {i}')

        lc.CheckItem(1)
        self.assertTrue(lc.IsChecked(1))
        lc.ToggleItem(1)
        self.assertFalse(lc.IsChecked(1))
        self.assertEqual(lc.checked, [(1, True), (1, False)])
        self.assertFalse(lc.HasCheckBoxes())

    def test_lib_mixins_listctrlCheckItemOverride(self):
        class MyCheckListCtrl(CheckListCtrl):
            def CheckItem(self, index, check=True):
                self.overridden = True
                CheckListCtrlMixin.CheckItem(self, index, check)

        lc = MyCheckListCtrl(self.frame)
        lc.InsertColumn(0, 'name')
        lc.InsertItem(0, 'item')
        lc.CheckItem(0)
        self.assertTrue(lc.overridden)
        self.assertTrue(lc.IsChecked(0))

    def test_lib_mixins_listctrlTextEditFirstClickSelects(self):
        lc = EditableListCtrl(self.frame)
        lc.SetSize((300, 200))
        lc.InsertColumn(0, 'name')
        lc.InsertItem(0, 'only item')
        self.myYield()
        # Where the item rect is relative to depends on the platform
        y = next(y for y in range(100) if lc.HitTest((5, y))[0] == 0)
        evt = wx.MouseEvent(wx.wxEVT_LEFT_DOWN)
        evt.SetPosition((5, y))

        # Clicking an unselected row lets the list control select it
        evt.Skip(False)
        lc.OnLeftDown(evt)
        self.myYield()
        self.assertTrue(evt.GetSkipped())
        self.assertFalse(lc.editor.IsShown())

        # Clicking it again once it's selected starts editing
        lc.Select(0)
        self.myYield()
        evt.Skip(False)
        lc.OnLeftDown(evt)
        self.myYield()
        self.assertFalse(evt.GetSkipped())
        self.assertTrue(lc.editor.IsShown())
        lc.CloseEditor()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
