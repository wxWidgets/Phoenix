from typing import Tuple

import wx
from typing_extensions import assert_type


# The virtual methods that window classes can override
class MyControl(wx.Control):
    def DoGetBestSize(self) -> wx.Size:
        return wx.Size(10, 10)

    def DoGetSize(self) -> Tuple[int, int]:
        return super().DoGetSize()

    def GetDefaultBorder(self) -> wx.Border:
        return wx.BORDER_NONE


def virtuals(ctrl: MyControl) -> None:
    assert_type(ctrl.DoGetSize(), Tuple[int, int])
    assert_type(ctrl.GetMainWindowOfCompositeControl(), wx.Window | None)


# Classes that are only defined for SIP
def sipOnlyClasses() -> None:
    config = wx.Config('app')
    assert_type(config.Read('key'), str)
