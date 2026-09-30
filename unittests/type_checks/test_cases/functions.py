import wx
from typing_extensions import assert_type

# Functions added to the module with addCppFunction must not take a self
# parameter (#2793)
assert_type(wx.IsMainThread(), bool)
assert_type(wx.FindWindowById(wx.ID_OK), wx.Window)
wx.IsMainThread(None)  # type: ignore[call-arg]  # ty: ignore[too-many-positional-arguments]
