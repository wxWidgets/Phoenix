import unittest
from unittests import wtc
import wx
import wx.adv
import os

gifFile = os.path.join(os.path.dirname(__file__), 'BD13656_.gif')


#---------------------------------------------------------------------------

class animate_Tests(wtc.WidgetTestCase):

    def test_animate1(self):
        ani = wx.adv.Animation()
        ani.LoadFile(gifFile)
        self.assertTrue(ani.IsOk())
        anictrl = wx.adv.AnimationCtrl(self.frame, anim=ani)
        anictrl.Play()
        self.waitFor(500)

    def test_animate2(self):
        ani = wx.adv.Animation(gifFile)
        self.assertTrue(ani.IsOk())
        anictrl = wx.adv.AnimationCtrl(self.frame, anim=ani)
        anictrl.Play()
        self.waitFor(500)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
