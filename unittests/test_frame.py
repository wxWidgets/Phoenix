import imp_unittest, unittest
import wtc
import wx
import os

#---------------------------------------------------------------------------

class frame_Tests(wtc.WidgetTestCase):

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
        
        
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
