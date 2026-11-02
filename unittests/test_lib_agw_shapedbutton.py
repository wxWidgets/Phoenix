import unittest
from unittests import wtc
import wx
import os

try:
    import wx.lib.agw.shapedbutton as SB
    skipIt = False
except:
    skipIt = True

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class lib_agw_shapedbuttons_Tests(wtc.WidgetTestCase):

    @unittest.skipIf(skipIt, 'Requires PIL')
    def test_lib_agw_shapedbutton1(self):

        btn = SB.SButton(self.frame, label='label')
        btn = SB.SButton(self.frame, -1, 'label', (10,10), (100,-1))

        bmp = wx.Bitmap(pngFile)
        btn = SB.SBitmapButton(self.frame, -1, bitmap=bmp)
        btn = SB.SBitmapTextButton(self.frame, -1, label='label', bitmap=bmp)

        btn.SetBitmapFocus(bmp)
        btn.SetBitmapDisabled(bmp)
        btn.SetBitmapSelected(bmp)

        btn = SB.SBitmapToggleButton(self.frame, -1, bitmap=bmp)
        btn.SetToggle(True)

        self.assertTrue(btn.GetValue())
        self.assertEqual(btn.GetBitmapLabel(), bmp)

    @unittest.skipIf(skipIt, 'Requires PIL')
    def test_lib_agw_shapedbutton2(self):

        btn = SB.SButton(self.frame, label='label')
        btn.SetEllipseAxis(2.0, 1.0)

        bmp = wx.Bitmap(pngFile)
        btn = SB.SBitmapButton(self.frame, -1, bitmap=bmp)
        btn.SetEllipseAxis(2.0, 1.0)
        self.assertEqual(btn.GetEllipseAxis(), (2.0, 1.0))

    @unittest.skipIf(skipIt, 'Requires PIL')
    def test_lib_agw_shapedbuttonRotatedLabel(self):
        btn = SB.SBitmapTextButton(self.frame, -1, wx.Bitmap(16, 16), 'Label')
        btn.SetAngleOfRotation(45)
        bmp = wx.Bitmap(101, 101)
        dc = wx.MemoryDC(bmp)
        btn.DrawLabel(dc, 101, 101)
        dc.SelectObject(wx.NullBitmap)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()