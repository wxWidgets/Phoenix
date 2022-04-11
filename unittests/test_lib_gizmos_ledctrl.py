import unittest
from unittests import wtc
import wx
import wx.lib.gizmos as gizmos


class lib_gizmos_ledctrl_Tests(wtc.WidgetTestCase):

    def test_defaultCtor(self):
        led = gizmos.LEDNumberCtrl()
        led.Create(self.frame, pos=(25,25), size=(280,50))
        led.SetValue('123456')

    def test_normalCtor(self):
        led = gizmos.LEDNumberCtrl(self.frame, pos=(25,25), size=(280,50))
        led.SetValue('123456')


