import importlib.metadata
import unittest
from unittests import wtc
import wx

import wx.lib.wxcairo as wxcairo

#---------------------------------------------------------------------------

def havePycairo():
    # Not with an import, which cairocffi may have taken over
    try:
        importlib.metadata.version('pycairo')
        return True
    except importlib.metadata.PackageNotFoundError:
        return False


class lib_wxcairo_Tests(wtc.WidgetTestCase):

    def contextFromBitmap(self, bmp):
        dc = wx.MemoryDC(bmp)
        try:
            return dc, wxcairo.ContextFromDC(dc)
        except NotImplementedError:
            self.skipTest('neither pycairo nor cairocffi is installed')

    def test_lib_wxcairoContextFromDC(self):
        bmp = wx.Bitmap(20, 20, 32)
        dc, ctx = self.contextFromBitmap(bmp)
        ctx.set_source_rgb(1, 0, 0)
        ctx.paint()
        del ctx
        dc.SelectObject(wx.NullBitmap)
        img = bmp.ConvertToImage()
        self.assertEqual((img.GetRed(10, 10), img.GetGreen(10, 10), img.GetBlue(10, 10)),
                         (255, 0, 0))

    @unittest.skipIf(not havePycairo(), 'pycairo is not installed')
    @unittest.skipIf('wxMSW' in wx.PlatformInfo, 'cairocffi comes first on Windows')
    def test_lib_wxcairoPrefersPycairo(self):
        # Packages such as PyGObject only work with pycairo, so it's used even
        # when cairocffi is installed too
        dc, ctx = self.contextFromBitmap(wx.Bitmap(20, 20, 32))
        self.assertEqual(type(ctx).__module__, 'cairo')

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
