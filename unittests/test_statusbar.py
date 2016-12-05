import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class statusbar_Tests(wtc.WidgetTestCase):

    def test_statusbarFlags(self):
        wx.STB_SIZEGRIP
        wx.STB_SHOW_TIPS
        wx.STB_ELLIPSIZE_START
        wx.STB_ELLIPSIZE_MIDDLE
        wx.STB_ELLIPSIZE_END
        wx.STB_DEFAULT_STYLE
        wx.SB_NORMAL
        wx.SB_FLAT
        wx.SB_RAISED


    def test_statusbarCtor(self):
        sb = wx.StatusBar(self.frame)

    def test_statusbarDefaultCtor(self):
        sb = wx.StatusBar()
        sb.Create(self.frame)


    def test_statusbarFrameUse1(self):
        sb = self.frame.CreateStatusBar(number=2)
        self.assertTrue(isinstance(sb, wx.StatusBar))
        self.assertTrue(self.frame.GetStatusBar() is sb)
        sb.SetStatusText('hello', 0)
        sb.SetStatusText('world', 1)


    def test_statusbarFrameUse2(self):
        sb = wx.StatusBar(self.frame)
        self.frame.SetStatusBar(sb)
        self.assertTrue(self.frame.GetStatusBar() is sb)


    def test_statusbarFrameUse3(self):
        class MyFrame(wx.Frame):
            def __init__(self, *args, **kw):
                wx.Frame.__init__(self, *args, **kw)
                self.sbCreated = False
            def OnCreateStatusBar(self, num, style, id, name):
                sb = wx.StatusBar(self, id, style, name)
                sb.SetFieldsCount(num)
                self.sbCreated = True
                return sb

        frm = MyFrame(self.frame)
        frm.CreateStatusBar()
        self.assertTrue(frm.sbCreated)
        frm.Show()


    def test_statusbarStatusBarPane(self):
        sb = self.frame.CreateStatusBar(number=2)
        pane = sb.GetField(0)
        self.assertTrue(isinstance(pane, wx.StatusBarPane))
        pane.Width
        pane.Style
        pane.Text


    def test_statusbarWidths1(self):
        sb = wx.StatusBar(self.frame)
        sb.SetFieldsCount(3)
        sb.SetStatusWidths([200, -1, 100])
        self.frame.SetStatusBar(sb)

        self.frame.SendSizeEvent()
        self.myYield()

        widths = [sb.GetStatusWidth(i) for i in range(sb.GetFieldsCount())]
        self.assertEqual(widths, [200, -1, 100])


    def test_statusbarWidths2(self):
        sb = self.frame.CreateStatusBar(3)
        self.frame.SetStatusWidths([200, -1, 100])

        self.frame.SendSizeEvent()
        self.myYield()

        widths = [sb.GetStatusWidth(i) for i in range(sb.GetFieldsCount())]
        self.assertEqual(widths, [200, -1, 100])


    def test_statusbarWidths3(self):
        sb = wx.StatusBar(self.frame)
        sb.SetFieldsCount(3, [200, -1, 100])
        self.frame.SetStatusBar(sb)

        self.frame.SendSizeEvent()
        self.myYield()

        widths = [sb.GetStatusWidth(i) for i in range(sb.GetFieldsCount())]
        self.assertEqual(widths, [200, -1, 100])


    def test_statusbarGetFielRect(self):
        # Test that GetFieldRect has been tweaked to be compatible with Classic
        sb = self.frame.CreateStatusBar(3)
        self.frame.SetStatusWidths([200, -1, 100])

        r = sb.GetFieldRect(1)
        self.assertTrue(isinstance(r, wx.Rect))


    def test_statusbarStyles(self):
        sb = wx.StatusBar(self.frame)
        sb.SetFieldsCount(4)
        styles = [wx.SB_NORMAL, wx.SB_FLAT, wx.SB_RAISED, wx.SB_SUNKEN]
        sb.SetStatusStyles(styles)
        self.frame.SetStatusBar(sb)

        self.frame.SendSizeEvent()
        self.myYield()

        current = [sb.GetStatusStyle(i) for i in range(sb.GetFieldsCount())]
        self.assertEqual(current, styles)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
