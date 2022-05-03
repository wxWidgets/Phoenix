import unittest
from unittests import wtc
import wx
import os

pngFile = os.path.join(os.path.dirname(__file__), 'toucan.png')

#---------------------------------------------------------------------------

class tglbtn_Tests(wtc.WidgetTestCase):

    def test_tglbtnCtors(self):
        btn = wx.ToggleButton(self.frame, label='label')
        btn = wx.ToggleButton(self.frame, -1, 'label', (10,10), (100,-1), wx.BU_LEFT)
        bmp = wx.BitmapBundle(wx.Bitmap(pngFile))
        btn.SetBitmap(bmp)


    def test_ButtonDefaultCtor(self):
        btn = wx.ToggleButton()
        btn.Create(self.frame, -1, 'button label')


    def test_ButtonDefaultEvt(self):
        wx.wxEVT_COMMAND_TOGGLEBUTTON_CLICKED
        wx.EVT_TOGGLEBUTTON


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
