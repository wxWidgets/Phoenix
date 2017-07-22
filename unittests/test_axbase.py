import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class axbase_Tests(wtc.WidgetTestCase):

    @unittest.skipIf('wxMSW' not in wx.PlatformInfo,
                     'PyAxBaseWindow only available on Windows')
    def test_axbase1(self):
        import wx.msw
        w = wx.msw.PyAxBaseWindow(self.frame)


    @unittest.skipIf('wxMSW' not in wx.PlatformInfo,
                     'PyAxBaseWindow only available on Windows')
    def test_axbase2(self):
        import wx.msw
        w = wx.msw.PyAxBaseWindow()
        w.Create(self.frame)


    @unittest.skipIf('wxMSW' not in wx.PlatformInfo,
                     'PyAxBaseWindow only available on Windows')
    def test_axbase3(self):
        import wx.msw
        w = wx.msw.PyAxBaseWindow(self.frame,
                                  id=-1,
                                  pos=wx.DefaultPosition,
                                  size=wx.DefaultSize,
                                  style=0,
                                  name='testing')



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
