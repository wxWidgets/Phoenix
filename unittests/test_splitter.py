import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class splitter_Tests(wtc.WidgetTestCase):

    def test_splitterCtor(self):
        sw = wx.SplitterWindow(self.frame)

    def test_splitterDefaultCtor(self):
        sw = wx.SplitterWindow()
        sw.Create(self.frame)

    def test_splitterSplits(self):
        sw = wx.SplitterWindow(self.frame)
        sw.SplitHorizontally(wx.Window(sw), wx.Window(sw))
        sw.SetMinimumPaneSize(25)
        sw.SetSashPosition(150)
        sw.SetSashGravity(0.75)


    def test_splitterProperties(self):
        sw = wx.SplitterWindow(self.frame)

        # just checks if they exist
        sw.MinimumPaneSize
        sw.SashGravity
        sw.SashPosition
        sw.SashSize
        sw.SplitMode
        sw.Window1
        sw.Window2
        sw.SashInvisible


    def test_splitterFlags(self):
        wx.SP_NOBORDER
        wx.SP_THIN_SASH
        wx.SP_NOSASH
        wx.SP_PERMIT_UNSPLIT
        wx.SP_LIVE_UPDATE
        wx.SP_3DSASH
        wx.SP_3DBORDER
        wx.SP_NO_XP_THEME
        wx.SP_BORDER
        wx.SP_3D

    def test_splitterEventTypes(self):
        wx.wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGED
        wx.wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGING
        wx.wxEVT_COMMAND_SPLITTER_DOUBLECLICKED
        wx.wxEVT_COMMAND_SPLITTER_UNSPLIT

        wx.EVT_SPLITTER_SASH_POS_CHANGED
        wx.EVT_SPLITTER_SASH_POS_CHANGING
        wx.EVT_SPLITTER_DOUBLECLICKED
        wx.EVT_SPLITTER_UNSPLIT
        wx.EVT_SPLITTER_DCLICK


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
