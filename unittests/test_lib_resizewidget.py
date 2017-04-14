import unittest
from unittests import wtc
import wx
import wx.lib.resizewidget as RW

#---------------------------------------------------------------------------

class lib_resizewidget_Tests(wtc.WidgetTestCase):

    def test_lib_resizewidget(self):
        rw1 = RW.ResizeWidget(self.frame)

    def test_lib_resizewidget_Constants(self):
        RW.RW_FILL
        RW.RW_FILL2
        RW.RW_LENGTH
        RW.RW_PEN
        RW.RW_THICKNESS

        RW.EVT_RW_LAYOUT_NEEDED


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
