import unittest
from unittests import wtc
import wx


#---------------------------------------------------------------------------

class MetafileDCTests(wtc.WidgetTestCase):

    @unittest.skipIf('wxMSW' not in wx.PlatformInfo, "Metafile classes only implemented on Windows")
    def test_MetafileDC1(self):
        import wx.msw
        # Not testing with output file because the file resource is not released
        # soon enough to be able to delete the file in this test, resulting in
        # permission errors.
        dc = wx.msw.MetafileDC()
        dc.DrawLine(0,0, 50,50)
        metafile = dc.Close()
        del dc

        self.assertTrue(isinstance(metafile, wx.msw.Metafile))
        metafile.SetClipboard(50,50)
        metafile.Play(wx.ClientDC(self.frame))
        del metafile


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
