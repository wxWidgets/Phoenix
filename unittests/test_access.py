import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

isMSW = 'wxMSW' in wx.PlatformInfo


class MyAccessible(wx.Accessible):
    pass


def makeAccessibleClass(base):
    class AccessibleWindow(base):
        createCount = 0
        def CreateAccessible(self):
            self.createCount += 1
            return MyAccessible(self)
    return AccessibleWindow


class access_Tests(wtc.WidgetTestCase):

    def checkCreateAccessible(self, base):
        win = makeAccessibleClass(base)(self.frame)
        acc = win.GetOrCreateAccessible()
        self.assertIsInstance(acc, MyAccessible)
        self.assertEqual(win.createCount, 1)

        self.assertIs(win.GetOrCreateAccessible(), acc)
        self.assertIs(win.GetAccessible(), acc)
        self.assertEqual(win.createCount, 1)

    # See https://github.com/wxWidgets/Phoenix/issues/2851
    @unittest.skipIf(not isMSW, "Accessibility is only implemented on Windows")
    def test_access_CreateAccessibleWindow(self):
        self.checkCreateAccessible(wx.Window)

    @unittest.skipIf(not isMSW, "Accessibility is only implemented on Windows")
    def test_access_CreateAccessibleTextCtrl(self):
        self.checkCreateAccessible(wx.TextCtrl)

    @unittest.skipIf(not isMSW, "Accessibility is only implemented on Windows")
    def test_access_CreateAccessibleGrid(self):
        import wx.grid
        self.checkCreateAccessible(wx.grid.Grid)

    @unittest.skipIf(not isMSW, "Accessibility is only implemented on Windows")
    def test_access_CreateAccessibleRichTextCtrl(self):
        # wxRichTextCtrl declares its CreateAccessible override as protected
        import wx.richtext
        self.checkCreateAccessible(wx.richtext.RichTextCtrl)

    @unittest.skipIf(isMSW, "Accessibility is only implemented on Windows")
    def test_access_NotImplemented(self):
        win = makeAccessibleClass(wx.Window)(self.frame)
        with self.assertRaises(NotImplementedError):
            win.GetOrCreateAccessible()
        self.assertEqual(win.createCount, 0)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
