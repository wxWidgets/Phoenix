from typing import Optional

import wx
from typing_extensions import assert_type


# Methods whose return value can be None (#2810)
class VirtualListCtrl(wx.ListCtrl):
    def OnGetItemAttr(self, item: int) -> Optional[wx.ItemAttr]:
        return None


def callers(ctrl: wx.ListCtrl) -> None:
    assert_type(ctrl.OnGetItemAttr(0), Optional[wx.ItemAttr])


# Slicing a wrapped list or array gives a Python list (#737)
def sequences(win: wx.Window) -> None:
    assert_type(win.GetChildren()[0], wx.Window)
    assert_type(win.GetChildren()[1:], list[wx.Window])
