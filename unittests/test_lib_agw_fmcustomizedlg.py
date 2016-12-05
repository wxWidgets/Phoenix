import unittest
from unittests import wtc
import wx

import wx.lib.agw.flatmenu as FM
import wx.lib.agw.fmcustomizedlg as FDLG

#---------------------------------------------------------------------------

class lib_agw_fmcustomizedlg_Tests(wtc.WidgetTestCase):

    def test_lib_agw_fmcustomizedlgCtor(self):
        minibarPanel= wx.Panel(self.frame, wx.ID_ANY)
        self._mtb = FM.FlatMenuBar(minibarPanel, wx.ID_ANY, 16, 6, options = FM.FM_OPT_SHOW_TOOLBAR|FM.FM_OPT_MINIBAR)

        fileMenu  = FM.FlatMenu()
        styleMenu = FM.FlatMenu()

        self._mtb.Append(fileMenu, "&File")
        self._mtb.Append(styleMenu, "&Style")

        # above is to excersize OrderedDict
        self._dlg = FDLG.FMCustomizeDlg(self._mtb)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
