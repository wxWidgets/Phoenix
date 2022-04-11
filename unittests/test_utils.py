import unittest
from unittests import wtc
import wx
import os


#---------------------------------------------------------------------------

class utils_Tests(wtc.WidgetTestCase):

    def test_utilsWindowDisabler(self):
        wd = wx.WindowDisabler()
        self.assertTrue(not self.frame.IsEnabled())
        del wd

        wd = wx.WindowDisabler(self.frame)
        self.assertTrue(    self.frame.IsEnabled())

    def test_utilsBusyCursor(self):
        self.assertTrue(not wx.IsBusy())
        bc = wx.BusyCursor()
        self.assertTrue(   wx.IsBusy())
        del bc
        self.assertTrue(not wx.IsBusy())

    def test_utilsBusyCursor2(self):
        self.assertTrue(not wx.IsBusy())
        wx.BeginBusyCursor()
        self.assertTrue(   wx.IsBusy())
        wx.EndBusyCursor()
        self.assertTrue(not wx.IsBusy())

    def test_utilsBusyCursor3(self):
        with wx.BusyCursor():
            self.myYield()

    def test_utilsSomeOtherStuff(self):
        wx.GetBatteryState()
        wx.GetPowerType()
        wx.GetKeyState(wx.WXK_F1)
        wx.GetMousePosition()
        wx.GetMouseState()
        wx.EnableTopLevelWindows(True)
        wx.FindWindowAtPoint((1,1))
        wx.Window.NewControlId()
        wx.RegisterId(12345)
        wx.GetUserName()
        wx.GetUserId()
        wx.GetOsDescription()


    def test_utilsVersionInfo(self):
        vi = wx.GetLibraryVersionInfo()
        assert isinstance(vi, wx.VersionInfo)
        vi.ToString()
        vi.Major
        vi.Minor
        vi.Micro
        vi.Copyright
        vi.Description
        vi.Name
        vi.VersionString



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
