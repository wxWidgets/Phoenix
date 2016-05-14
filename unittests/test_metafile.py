import unittest
import wtc
import wx
import wx.msw


#---------------------------------------------------------------------------

class MetafileDCTests(wtc.WidgetTestCase):

    @unittest.skipIf('wxMSW' not in wx.PlatformInfo, "Metafile classes only imsplemented on Windows")
    def test_MetafileDC1(self):
        # Not testing with output file because it is not released soon enough
        # for this tests to be able to delete the file in this test, resulting
        # in permission errors.
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
