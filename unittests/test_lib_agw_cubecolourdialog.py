import unittest
from unittests import wtc
import wx

import wx.lib.agw.cubecolourdialog as CCD

#---------------------------------------------------------------------------

class lib_agw_cubecolourdialog_Tests(wtc.WidgetTestCase):

    def test_lib_agw_cubecolourdialogCtor(self):
        colourData = wx.ColourData()
        colourData.SetColour(wx.RED)
        dlg = CCD.CubeColourDialog(self.frame, colourData, agwStyle=0)
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

    def test_lib_agw_cubecolourdialogMethods(self):
        colourData = wx.ColourData()
        colourData.SetColour(wx.BLUE)
        dlg = CCD.CubeColourDialog(self.frame, colourData, agwStyle=0)

        self.assertTrue(dlg.GetAGWWindowStyleFlag() == 0)
        dlg.SetAGWWindowStyleFlag(CCD.CCD_SHOW_ALPHA)
        self.assertTrue(dlg.GetAGWWindowStyleFlag() > 0)

        colour = dlg.GetRGBAColour()
        self.assertEqual(colour, wx.Colour('blue'))

        ccd_colour = CCD.Colour(wx.Colour(colour))
        html = CCD.rgb2html(ccd_colour)
        self.assertTrue(html in CCD.HTMLCodes)
        wx.CallLater(250, dlg.EndModal, wx.ID_OK)
        dlg.ShowModal()
        dlg.Destroy()

    def test_lib_agw_cubecolourdialogConstantsExist(self):
        # CubeColourDialog agwStyle
        CCD.CCD_SHOW_ALPHA

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
