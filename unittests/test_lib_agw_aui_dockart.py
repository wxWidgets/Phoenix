import unittest
from unittests import wtc
import wx
import os

import wx.lib.agw.aui as aui
import wx.lib.agw.aui.dockart as da

#---------------------------------------------------------------------------

class lib_agw_aui_dockart_Tests(wtc.WidgetTestCase):

    def test_lib_agw_aui_dockartCtor(self):
        da.ModernDockArt(self.frame)

    def test_lib_agw_aui_dockartModernCaption(self):
        art = da.ModernDockArt(self.frame)
        bmp = wx.Bitmap(200, 200)
        dc = wx.MemoryDC(bmp)
        for left in (False, True):
            pane = aui.AuiPaneInfo().Caption('Caption').CaptionVisible(True, left)
            art.DrawCaption(dc, self.frame, 'Caption', wx.Rect(0, 0, 151, 21), pane)
        dc.SelectObject(wx.NullBitmap)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
