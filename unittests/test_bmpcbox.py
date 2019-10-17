import unittest
from unittests import wtc
import wx
import wx.adv
import os

imgFiles = [os.path.join(os.path.dirname(__file__), 'LB01.png'),
            os.path.join(os.path.dirname(__file__), 'LB02.png'),
            os.path.join(os.path.dirname(__file__), 'LB03.png'),
            os.path.join(os.path.dirname(__file__), 'LB04.png'),
            ]

#---------------------------------------------------------------------------

class bmpcbox_Tests(wtc.WidgetTestCase):

    @unittest.skipIf('wxMac' in wx.PlatformInfo, 'Needs a real MainLoop on wxMac')
    def test_bmpcbox1(self):
        pnl = wx.Panel(self.frame)

        bcb = wx.adv.BitmapComboBox(pnl)
        for idx, name in enumerate(imgFiles):
            bmp = wx.Bitmap(name)
            bcb.Append(os.path.basename(name), bmp)

        bcb.GetItemBitmap(0)
        bcb.SetItemBitmap(0, wx.NullBitmap)

        bcb.SetClientObject(2, "Hello")
        self.assertEqual(bcb.GetClientObject(2), "Hello")

        bcb.SetClientData(2, "Bye")
        self.assertEqual(bcb.GetClientData(2), "Bye")

        self.waitFor(300)


    @unittest.skipIf('wxMac' in wx.PlatformInfo, 'Needs a real MainLoop on wxMac')
    def test_bmpcbox2(self):
        pnl = wx.Panel(self.frame)

        bcb = wx.adv.BitmapComboBox(pnl)
        for idx, name in enumerate(imgFiles):
            bmp = wx.Bitmap(name)
            bcb.Append(os.path.basename(name), bmp, str(idx))

        self.assertEqual(bcb.GetClientData(2), "2")

        self.waitFor(300)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
