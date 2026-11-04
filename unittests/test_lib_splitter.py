import unittest
from unittests import wtc
import wx
import wx.lib.splitter as sp

#---------------------------------------------------------------------------

class splitter_Tests(wtc.WidgetTestCase):

    def test_splitterCtor(self):
        splitter = sp.MultiSplitterWindow(self.frame, style=wx.SP_LIVE_UPDATE)

    def test_splitterMulti(self):
        splitter = sp.MultiSplitterWindow(self.frame, style=wx.SP_LIVE_UPDATE)

        p = wx.Panel(self.frame)
        splitter.AppendWindow(p, 140)

        p = wx.Panel(self.frame)
        splitter.AppendWindow(p, 160)

        p = wx.Panel(self.frame)
        splitter.AppendWindow(p, 180)

        splitter.SetOrientation(wx.VERTICAL)
        self.assertEqual(splitter.GetOrientation(), wx.VERTICAL)

        splitter.SetOrientation(wx.HORIZONTAL)
        self.assertEqual(splitter.GetOrientation(), wx.HORIZONTAL)

    def test_splitterMinimumPaneSize(self):
        splitter = sp.MultiSplitterWindow(self.frame, size=(400, 200))
        for i in range(3):
            splitter.AppendWindow(wx.Panel(splitter))
        splitter.SetSashPosition(0, 100)
        splitter.SetSashPosition(1, 30)

        splitter.SetMinimumPaneSize(50)
        self.assertEqual(splitter.GetSashPosition(1), 50)

        # Dragging a sash shrinks the last window, which must keep the minimum
        newPos, _ = splitter._OnSashPositionChanging(0, 390, 0, False)
        splitter._SetSashPositionAndNotify(0, newPos)
        splitter.SizeWindows()
        self.assertGreaterEqual(splitter.GetWindow(2).GetSize().width, 50)
        self.assertGreaterEqual(splitter.GetSashPosition(0), 50)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
