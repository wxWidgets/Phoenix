import wx
import wx.dataview
import wx.grid
import wx.ribbon
import wx.xml
import wx.xrc
from typing_extensions import assert_type


# Classes that have a different name in Python than in C++
def renamed(matrix: wx.AffineMatrix2DBase) -> None:
    assert_type(matrix.TransformPoint(wx.Point2D(1, 2)), wx.Point2D)
    matrix.TransformPoint((1.0, 2.0))


# Classes from other modules
def otherModules(handler: wx.xrc.XmlResourceHandler) -> None:
    assert_type(handler.GetNode(), wx.xml.XmlNode)


# Typedefs that aren't classes in Python
def typedefs(grid: wx.grid.Grid, data: wx.PrintData) -> None:
    assert_type(grid.GetGridWindow(), wx.Window)
    assert_type(data.GetQuality(), int)


# The list and array classes made by SIP
def sequences(dc: wx.DC, ctrl: wx.dataview.DataViewCtrl) -> None:
    dc.DrawLines([(0, 0), (10, 10)])
    dc.DrawLines([wx.Point(0, 0), wx.Point(10, 10)])
    selections = ctrl.GetSelections()
    assert_type(selections, wx.dataview.DataViewItemArray)
    assert_type(selections[0], wx.dataview.DataViewItem)
    assert_type(len(selections), int)
    for item in selections:
        assert_type(item, wx.dataview.DataViewItem)
    dc.DrawLines([1, 2])  # type: ignore[list-item]  # ty: ignore[invalid-argument-type]


# Classes that SIP creates from forward declarations
def forwardDeclarations(bar: wx.ribbon.RibbonButtonBar, bitmap: wx.Bitmap) -> None:
    assert_type(bar.AddButton(1, 'label', bitmap, 'help'), wx.ribbon.RibbonButtonBarButtonBase)
