import unittest
from unittests import wtc
import wx

import wx.lib.agw.balloontip as BT

#---------------------------------------------------------------------------

class lib_agw_balloontip_Tests(wtc.WidgetTestCase):

    def test_lib_agw_balloontipCtor(self):
        tip = BT.BalloonTip(toptitle='Balloon', message='Hello wxPython',
                            shape=BT.BT_ROUNDED, tipstyle=BT.BT_BUTTON)

    def test_lib_agw_balloontipMethods(self):
        tip = BT.BalloonTip(toptitle='Balloon', message='Hello wxPython',
                            shape=BT.BT_ROUNDED, tipstyle=BT.BT_BUTTON)

        self.assertTrue(tip.GetBalloonShape() == BT.BT_ROUNDED)
        self.assertTrue(tip.GetBalloonTipStyle() == BT.BT_BUTTON)

        tip.SetBalloonShape(BT.BT_RECTANGLE)
        tip.SetBalloonTipStyle(BT.BT_LEAVE)
        self.assertTrue(tip.GetBalloonShape() == BT.BT_RECTANGLE)
        self.assertTrue(tip.GetBalloonTipStyle() == BT.BT_LEAVE)

    def test_lib_agw_balloontipConstantsExist(self):
        BT.BT_ROUNDED
        BT.BT_RECTANGLE
        BT.BT_LEAVE
        BT.BT_CLICK
        BT.BT_BUTTON


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
