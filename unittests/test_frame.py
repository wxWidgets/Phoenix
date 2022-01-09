import unittest
from unittests import wtc
import wx
import os

#---------------------------------------------------------------------------

class frame_Tests(wtc.WidgetTestCase):

    def test_frameStyles(self):
        wx.FRAME_NO_TASKBAR
        wx.FRAME_TOOL_WINDOW
        wx.FRAME_FLOAT_ON_PARENT
        wx.FRAME_SHAPED


    def test_frameCtors(self):
        f = wx.Frame(None)
        f.Show()
        f.Close()
        f = wx.Frame(self.frame, title="Title", pos=(50,50), size=(100,100))
        f.Show()
        f.Close()
        f = wx.Frame()
        f.Create(None, title='2 phase')
        f.Show()
        f.Close()

    def test_frameTopLevelTweaks(self):
        # test a couple tweaks added in wx.TopLevelWidnow
        f = wx.Frame()
        f.MacSetMetalAppearance(True)
        f.Create(None)
        f.Show()
        f.MacGetTopLevelWindowRef()
        f.Close()


    def test_frameProperties(self):
        f = wx.Frame(None)
        f.Show()

        f.DefaultItem
        f.Icon
        f.Title
        f.TmpDefaultItem
        f.OSXModified
        f.MacMetalAppearance

        f.Close()


    def test_frameRestore(self):
        f = wx.Frame(self.frame, title="Title", pos=(50,50), size=(100,100))
        f.Show()
        f.Maximize()
        self.waitFor(100)
        assert f.IsMaximized()
        if 'wxGTK' in wx.PlatformInfo:
            f.Maximize(False)
        else:
            f.Restore()
        self.waitFor(100)
        assert not f.IsMaximized()
        f.Close()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
