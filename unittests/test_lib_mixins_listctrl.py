import unittest
import warnings
from unittests import wtc
import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin

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

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
