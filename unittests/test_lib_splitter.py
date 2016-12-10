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

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
