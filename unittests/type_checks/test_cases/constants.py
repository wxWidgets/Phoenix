import wx
from typing_extensions import assert_type

# Constants that core's Python code adds to the wx namespace (#2559)
assert_type(wx.BOLD, int)
assert_type(wx.NORMAL, int)
assert_type(wx.DEFAULT, int)
assert_type(wx.SOLID, int)
assert_type(wx.CROSS_HATCH, int)
wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
