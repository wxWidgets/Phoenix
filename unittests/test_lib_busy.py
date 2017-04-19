import unittest
from unittests import wtc
import wx
import os

from wx.lib.busy import BusyInfo

delay = 100

#---------------------------------------------------------------------------

class lib_busy_Tests(wtc.WidgetTestCase):

    def test_lib_busy1(self):
        with BusyInfo("short message...", self.frame):
            wx.MilliSleep(delay*2)
        wx.MilliSleep(delay)
        self.myYield()

    def test_lib_busy2(self):
        with BusyInfo("This is my longer short message.  Please be patient...", self.frame):
            wx.MilliSleep(delay*2)
        wx.MilliSleep(delay)
        self.myYield()

    def test_lib_busy3(self):
        busy = BusyInfo("Without using the context manager...", self.frame)
        wx.MilliSleep(delay*2)
        del busy
        wx.MilliSleep(delay)
        self.myYield()

    def test_lib_busy4(self):
        with BusyInfo("Without using the parent window..."):
            wx.MilliSleep(delay*2)
        wx.MilliSleep(delay)
        self.myYield()

    def test_lib_busy5(self):
        message = """A long message with line breaks:
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit
esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est
laborum."""
        with BusyInfo(message, self.frame):
            wx.MilliSleep(delay*2)
        wx.MilliSleep(delay)
        self.myYield()




#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()