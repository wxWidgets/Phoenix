import wx
import wx.grid
import wx.propgrid
from typing_extensions import assert_type


# Enums are classes derived from int, whose members are in the class and in
# the enclosing scope
def enums(font: wx.Font, value: object) -> None:
    assert_type(wx.FONTWEIGHT_BOLD, wx.FontWeight)
    assert_type(wx.FontWeight.FONTWEIGHT_BOLD, wx.FontWeight)
    assert_type(font.GetWeight(), wx.FontWeight)
    if isinstance(value, wx.FontWeight):
        assert_type(value, wx.FontWeight)
    font.SetWeight(wx.FONTWEIGHT_BOLD)
    font.SetWeight(700)
    assert_type(wx.ALL | wx.EXPAND, int)
    assert_type(wx.grid.GridCellAttr.Cell, wx.grid.GridCellAttr.AttrKind)
    assert_type(wx.grid.GridCellAttr.AttrKind.Cell, wx.grid.GridCellAttr.AttrKind)
    font.SetWeight('bold')  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


# Except scoped enums, which are IntEnums
def scopedEnums() -> None:
    wx.propgrid.PGPropValFormatFlags.FullValue
