import unittest
from unittests import wtc
import wx

import wx.lib.agw.toasterbox as TB

#---------------------------------------------------------------------------

class lib_agw_toasterbox_Tests(wtc.WidgetTestCase):

    @unittest.skip(
        "Skipping because the attempt to destroy the ToasterBox (tb) "
        "instance as it goes out of scope gives: "
        ""
        "    RuntimeError: super-class __init__() of type ToasterBox "
        "    was never called")
    def test_lib_agw_toasterboxCtor(self):
        windowstyle = TB.TB_CAPTION
        tbstyle = TB.TB_COMPLEX
        closingstyle = TB.TB_ONCLICK

        tb = TB.ToasterBox(self.frame, tbstyle, windowstyle, closingstyle,
                           scrollType=TB.TB_SCR_TYPE_FADE)
        tb.Play()


    def test_lib_agw_thumbnailctrlStyles(self):
        TB.TB_SIMPLE
        TB.TB_COMPLEX
        TB.TB_ONTIME
        TB.TB_ONCLICK
        TB.TB_DEFAULT_STYLE
        TB.TB_CAPTION
        TB.TB_SCR_TYPE_UD
        TB.TB_SCR_TYPE_DU
        TB.TB_SCR_TYPE_FADE



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
