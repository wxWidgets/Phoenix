import unittest
from unittests import wtc
import wx
import wx.lib.colourselect

#---------------------------------------------------------------------------

class lib_colourselect_Tests(wtc.WidgetTestCase):

    def test_lib_colourselect1(self):

        btn = wx.lib.colourselect.ColourSelect(self.frame, -1, "Choose...", wx.WHITE)

        self.assertEqual(btn.GetColour(), wx.Colour('white'))

        btn.SetValue(wx.RED)
        self.assertEqual(btn.GetColour(), wx.Colour('red'))

        btn.SetValue('black')
        self.assertEqual(btn.GetColour(), wx.BLACK)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
