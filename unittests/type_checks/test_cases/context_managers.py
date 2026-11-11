import wx
import wx.grid
from typing_extensions import assert_type


# Classes used in a with statement give the instance itself (#3030)
class MyDialog(wx.Dialog):
    pass


def useDialogs(parent: wx.Window) -> None:
    with wx.Dialog(parent) as dlg:
        assert_type(dlg, wx.Dialog)
    with MyDialog(parent) as mine:
        assert_type(mine, MyDialog)
    with wx.MessageDialog(parent, 'message') as msg:
        assert_type(msg, wx.MessageDialog)


def useOthers(window: wx.Window, grid: wx.grid.Grid) -> None:
    with wx.ClientDC(window) as dc:
        assert_type(dc, wx.ClientDC)
        with wx.DCPenChanger(dc, wx.BLACK_PEN) as changer:
            assert_type(changer, wx.DCPenChanger)
    with wx.BusyCursor() as cursor:
        assert_type(cursor, wx.BusyCursor)
    with wx.grid.GridUpdateLocker(grid) as locker:
        assert_type(locker, wx.grid.GridUpdateLocker)


# They don't suppress exceptions, so the code after the with is reachable
def afterWith() -> int:
    with wx.LogNull():
        return 1
