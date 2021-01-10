import unittest
from unittests import wtc
import wx
import six

#---------------------------------------------------------------------------

class WindowTests(wtc.WidgetTestCase):

    def test_SimpleWindowCtor(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50), wx.BORDER_NONE)
        self.assertEqual(w.GetWindowStyleFlag(), wx.BORDER_NONE)
        self.assertTrue(w.Parent is self.frame)

    def test_windowHandle(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50))
        hdl = w.GetHandle()
        self.assertTrue(isinstance(hdl, six.integer_types))


    def test_windowProperties(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50))
        # Just test that these properties exist for now. More tests can be
        # added later to ensure that they work correctly.
        w.AcceleratorTable
        w.AutoLayout
        w.BackgroundColour
        w.BackgroundStyle
        w.EffectiveMinSize
        w.BestSize
        w.BestVirtualSize
        w.Border
        w.Caret
        w.CharHeight
        w.CharWidth
        w.Children
        w.ClientAreaOrigin
        w.ClientRect
        w.ClientSize
        w.Constraints
        w.ContainingSizer
        w.Cursor
        w.DefaultAttributes
        w.DropTarget
        w.EventHandler
        w.ExtraStyle
        w.Font
        w.ForegroundColour
        w.GrandParent
        w.TopLevelParent
        w.Handle
        w.HelpText
        w.Id
        w.Label
        w.LayoutDirection
        w.MaxHeight
        w.MaxSize
        w.MaxWidth
        w.MinHeight
        w.MinSize
        w.MinWidth
        w.Name
        w.Parent
        w.Position
        w.Rect
        w.ScreenPosition
        w.ScreenRect
        w.Size
        w.Sizer
        w.ThemeEnabled
        w.ToolTip
        w.UpdateClientRect
        w.UpdateRegion
        w.Validator
        w.VirtualSize
        w.WindowStyle
        w.WindowStyleFlag
        w.WindowVariant
        w.Shown
        w.Enabled
        w.TopLevel
        w.MinClientSize
        w.MaxClientSize


    def test_windowFunctions(self):
        wx.FindWindowById
        wx.FindWindowByName
        wx.FindWindowByLabel

        self.assertEqual(wx.FindWindowById(self.frame.GetId()),  self.frame)

    def test_windowCoordConvFunctions(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50))
        a = w.ClientToScreen(0, 0)
        b = w.ClientToScreen((0, 0))
        c = w.ScreenToClient(0, 0)
        d = w.ScreenToClient((0, 0))
        self.assertEqual(a[0], b.x)
        self.assertEqual(a[1], b.y)
        self.assertEqual(c[0], d.x)
        self.assertEqual(c[1], d.y)


    def test_DLG_UNIT(self):
        def _check(val, typ):
            assert isinstance(val, typ)
            a, b = val
            assert isinstance(a, int)
            assert isinstance(b, int)

        val = wx.DLG_UNIT(self.frame, wx.Point(10,10))
        _check(val, wx.Point)

        val = wx.DLG_UNIT(self.frame, wx.Size(10,10))
        _check(val, wx.Size)

        val = wx.DLG_UNIT(self.frame, (10,10))
        _check(val, tuple)

        val = wx.DLG_UNIT(self.frame, [10,10])
        _check(val, tuple)

        val = self.frame.DLG_UNIT(wx.Point(10, 10))
        _check(val, wx.Point)

        val = self.frame.DLG_UNIT(wx.Size(10, 10))
        _check(val, wx.Size)

        val = self.frame.DLG_UNIT((10, 10))
        _check(val, tuple)

        val = self.frame.DLG_UNIT([10, 10])
        _check(val, tuple)

        wx.DLG_SZE
        wx.DLG_PNT


    def test_vizattrs1(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50))
        a = w.GetClassDefaultAttributes()
        assert isinstance(a.colBg, wx.Colour)
        assert isinstance(a.colFg, wx.Colour)
        assert isinstance(a.font, wx.Font)


    def test_vizattrs2(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50))
        assert isinstance(w.GetClassDefaultAttributes().colBg, wx.Colour)
        assert isinstance(w.GetClassDefaultAttributes().colFg, wx.Colour)
        assert isinstance(w.GetClassDefaultAttributes().font, wx.Font)


    def test_vizattrs3(self):
        w = wx.Window(self.frame, -1, (10,10), (50,50))
        a = w.GetClassDefaultAttributes()
        with self.assertRaises(AttributeError):
            a.colBg = wx.Colour('blue')
        with self.assertRaises(AttributeError):
            a.colFg = wx.Colour('blue')
        with self.assertRaises(AttributeError):
            a.font = wx.NORMAL_FONT

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
