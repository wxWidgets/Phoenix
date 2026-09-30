from typing import Any, List

import wx
import wx.adv
import wx.grid
import wx.richtext
import wx.stc
import wx.xml
from typing_extensions import assert_type


# SIP annotations like /Transfer/ in hand written C++ methods are not
# mistaken for the parameter name
def sizerUserData(sizer: wx.Sizer, gbsizer: wx.GridBagSizer) -> None:
    sizer.Add(wx.Size(10, 10), userData={'any': 'object'})
    gbsizer.Add(wx.Size(10, 10), (0, 0), userData=wx.Object())


# SIP mapped types and C++ typedefs are mapped to Python types
def mappedTypes(stc: wx.stc.StyledTextCtrl, stream: wx.InputStream,
                colour: wx.Colour, tree: wx.TreeCtrl, item: wx.TreeItemId) -> None:
    wx.Bitmap.FromBuffer(1, 1, bytearray(3))
    wx.Bitmap.FromBuffer(1, 1, memoryview(b'abc'))
    stc.AddStyledText(b'ab')
    assert_type(stc.GetStyledText(0, 1), memoryview)
    assert_type(stc.GetCurLineRaw(), tuple[bytes, int])
    assert_type(stream.SeekI(0), int)
    assert_type(colour.GetRGB(), int)
    assert_type(tree.GetFirstChild(item), tuple[wx.TreeItemId, Any])
    wx.Bitmap.FromBuffer(1, 1, 'abc')  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def vectors(bundle: wx.adv.AnimationBundle, db: wx.ColourDatabase) -> None:
    assert_type(bundle.GetAll(), List[wx.adv.Animation])
    assert_type(db.GetAllNames(), List[str])


def autoConversions() -> None:
    wx.Colour(None)
    wx.Colour((1, 2, 3))
    wx.Colour('red')
    wx.Colour(1.5)  # type: ignore[call-overload]  # ty: ignore[no-matching-overload]


def nestedEnums(listbox: wx.richtext.RichTextStyleListBox) -> None:
    assert_type(listbox.GetStyleType(), wx.richtext.RichTextStyleListBox.RichTextStyleType)


# Base classes that are given with a wx prefix in the etg scripts
def bases(doc: wx.xml.XmlDocument, stc: wx.stc.StyledTextCtrl) -> None:
    obj: wx.Object = doc
    control: wx.Control = stc
    entry: wx.TextEntry = stc
    assert_type(doc.IsSameAs(wx.Object()), bool)
    assert_type(stc.GetParent(), wx.Window)
