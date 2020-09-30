import unittest
from unittests import wtc
import wx
import wx.aui

#---------------------------------------------------------------------------

class auiframemanager_Tests(wtc.WidgetTestCase):

    def test_auiframemanager01(self):
        wx.aui.AUI_DOCK_NONE
        wx.aui.AUI_DOCK_TOP
        wx.aui.AUI_DOCK_RIGHT
        wx.aui.AUI_DOCK_BOTTOM
        wx.aui.AUI_DOCK_LEFT
        wx.aui.AUI_DOCK_CENTER
        wx.aui.AUI_DOCK_CENTRE

        wx.aui.AUI_MGR_ALLOW_FLOATING
        wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE
        wx.aui.AUI_MGR_TRANSPARENT_DRAG
        wx.aui.AUI_MGR_TRANSPARENT_HINT
        wx.aui.AUI_MGR_VENETIAN_BLINDS_HINT
        wx.aui.AUI_MGR_RECTANGLE_HINT
        wx.aui.AUI_MGR_HINT_FADE
        wx.aui.AUI_MGR_NO_VENETIAN_BLINDS_FADE
        wx.aui.AUI_MGR_LIVE_RESIZE
        wx.aui.AUI_MGR_DEFAULT



    def test_auiframemanager02(self):
        wx.aui.EVT_AUI_PANE_BUTTON
        wx.aui.EVT_AUI_PANE_CLOSE
        wx.aui.EVT_AUI_PANE_MAXIMIZE
        wx.aui.EVT_AUI_PANE_RESTORE
        wx.aui.EVT_AUI_PANE_ACTIVATED
        wx.aui.EVT_AUI_RENDER
        wx.aui.EVT_AUI_FIND_MANAGER

        wx.aui.wxEVT_AUI_PANE_BUTTON
        wx.aui.wxEVT_AUI_PANE_CLOSE
        wx.aui.wxEVT_AUI_PANE_MAXIMIZE
        wx.aui.wxEVT_AUI_PANE_RESTORE
        wx.aui.wxEVT_AUI_PANE_ACTIVATED
        wx.aui.wxEVT_AUI_RENDER
        wx.aui.wxEVT_AUI_FIND_MANAGER



    def test_auiframemanager03(self):
        mgr = wx.aui.AuiManager(self.frame)
        mgr.AddPane( wx.Panel(self.frame),
                     wx.aui.AuiPaneInfo().Top().Caption('caption').Dock())
        mgr.Update()
        self.myYield()
        mgr.UnInit()


    def test_auiframemanager04(self):
        mgr = wx.aui.AuiManager()
        mgr.SetManagedWindow(self.frame)
        mgr.AddPane( wx.Panel(self.frame),
                     wx.aui.AuiPaneInfo().Top().Caption('caption').Dock())
        mgr.Update()
        self.myYield()
        mgr.UnInit()



    def test_auiframemanager05(self):
        pi = wx.aui.AuiPaneInfo()
        pi.BestSize((5,6))
        assert pi.best_size == (5,6)
        pi.BestSize(wx.Size(7,8))
        assert pi.best_size == (7,8)
        pi.BestSize(1, 2)
        assert pi.best_size == (1,2)



    def test_auiframemanager06(self):
        pi = wx.aui.AuiPaneInfo().Center().Caption("hello").DefaultPane().CloseButton().Floatable()


    def test_auiframemanager07(self):
        pi1 = wx.aui.AuiPaneInfo().BestSize(12,34)
        pi2 = wx.aui.AuiPaneInfo(pi1)
        assert pi1 is not pi2
        assert pi1.best_size == pi2.best_size


    def test_auiframemanager08(self):
        obj = wx.aui.AuiDockInfo()


    def test_auiframemanager09(self):
        obj = wx.aui.AuiDockUIPart()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
