import unittest
from unittests import wtc
import wx

from wx.lib.agw.artmanager import ArtManager, RendererMSOffice2007
from wx.lib.agw.fmresources import ControlFocus

#---------------------------------------------------------------------------

class lib_agw_artmanager_Tests(wtc.WidgetTestCase):

    def test_lib_agw_artmanagerDrawing(self):
        renderer = RendererMSOffice2007()
        artMgr = ArtManager.Get()
        raiseToolbar = artMgr.GetRaiseToolbar()
        self.addCleanup(artMgr.SetRaiseToolbar, raiseToolbar)
        artMgr.SetRaiseToolbar(True)
        bmp = wx.Bitmap(101, 101)
        dc = wx.MemoryDC(bmp)
        rect = wx.Rect(0, 0, 101, 21)
        renderer.DrawButtonColour(dc, rect, ControlFocus, wx.BLUE)
        renderer.DrawMenuBarBg(dc, rect)
        renderer.DrawToolBarBg(dc, rect)
        artMgr.PaintCrescentGradientBox(dc, rect, wx.BLACK, wx.WHITE)
        self.assertEqual(artMgr.MixColours(wx.BLACK, wx.WHITE, 50), wx.Colour(127, 127, 127))
        dc.SelectObject(wx.NullBitmap)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
