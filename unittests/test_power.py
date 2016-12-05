import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class power_Tests(wtc.WidgetTestCase):

    def test_power1(self):
        wx.POWER_SOCKET
        wx.POWER_BATTERY
        wx.POWER_UNKNOWN

        wx.BATTERY_NORMAL_STATE
        wx.BATTERY_LOW_STATE
        wx.BATTERY_CRITICAL_STATE
        wx.BATTERY_SHUTDOWN_STATE
        wx.BATTERY_UNKNOWN_STATE

        wx.wxEVT_POWER_SUSPENDING
        wx.wxEVT_POWER_SUSPENDED
        wx.wxEVT_POWER_SUSPEND_CANCEL
        wx.wxEVT_POWER_RESUME

        wx.EVT_POWER_SUSPENDING
        wx.EVT_POWER_SUSPENDED
        wx.EVT_POWER_SUSPEND_CANCEL
        wx.EVT_POWER_RESUME

        wx.PowerEvent



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
