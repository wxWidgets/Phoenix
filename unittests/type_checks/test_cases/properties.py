import wx
import wx.richtext
from typing_extensions import assert_type


# Properties return what their getter does, and accept what their setter's
# overloads with one argument do (#2733)
def properties(win: wx.Window) -> None:
    assert_type(win.Size, wx.Size)
    assert_type(win.Position, wx.Point)
    win.Size = wx.Size(10, 20)
    win.Size = (10, 20)
    win.Size = wx.Rect(0, 0, 10, 20)
    win.Position = (5, 5)
    win.Size = 10  # type: ignore[assignment]  # ty: ignore[invalid-assignment]


# A class member with the same name as a class used in the class's
# annotations, like the Size property in Window, doesn't hide that class
def shadowedNames(win: wx.Window, button: wx.Button, rect: wx.Rect,
                  box: wx.richtext.RichTextParagraphLayoutBox) -> None:
    assert_type(win.GetSize(), wx.Size)
    win.SetSize(wx.Size(10, 20))
    button.SetBitmap(wx.Bitmap())
    button.SetBitmap('bitmap.png')  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
    assert_type(button.Bitmap, wx.Bitmap)
    # Rect has a Union method
    rect.Contains((1, 2))
    rect.Contains('point')  # type: ignore[call-overload]  # ty: ignore[no-matching-overload]
    assert_type(box.GetRichTextCtrl(), wx.richtext.RichTextCtrl)
