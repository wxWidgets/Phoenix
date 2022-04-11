import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class deadobj_Tests(wtc.WidgetTestCase):

    def test_deadobj__nonzero__1(self):
        # A __nonzero__ method has been added to the wx.Window class that
        # will return True if the C++ part of the object still exists. This
        # can be used with if's or other conditional statements to see if it
        # is still safe to call methods of that window object.
        p = wx.Panel(self.frame)
        self.assertTrue(True if p else False)

        p.Destroy()
        self.assertFalse(True if p else False)

    def test_deadobj__nonzero__2(self):
        # check that it also works with TLWs whose destruction is delayed
        # until there are idle events.
        f = wx.Frame(self.frame)
        f.Show()
        self.assertTrue(True if f else False)

        f.Close()
        self.myYield()

        # TODO: figure out if this is a bug in wxMSW, or just an oddity of
        # the test environment.
        if 'wxMSW' not in wx.PlatformInfo:
            self.assertFalse(True if f else False)


    def test_deadobjException(self):
        # There should be a RuntimeError exception if we try to use an object
        # after it's C++ parts have been destroyed.
        p = wx.Panel(self.frame)
        p.Destroy()
        with self.assertRaises(RuntimeError):
            p.IsShown()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
