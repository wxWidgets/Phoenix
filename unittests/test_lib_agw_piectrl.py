import unittest
from unittests import wtc
import wx

import wx.lib.agw.piectrl as PC

#---------------------------------------------------------------------------

class lib_agw_piectrl_Tests(wtc.WidgetTestCase):

    def test_lib_agw_piectrlCtor(self):
        pie = PC.PieCtrl(self.frame)


    def test_lib_agw_piectrlMethods(self):
        # create a simple PieCtrl with 2 sectors
        mypie = PC.PieCtrl(self.frame)

        part1 = PC.PiePart()

        part1.SetLabel("Label 1")
        part1.SetValue(300)
        part1.SetColour(wx.Colour(200, 50, 50))
        mypie._series.append(part1)

        part2 = PC.PiePart()

        part2.SetLabel("Label 2")
        part2.SetValue(200)
        part2.SetColour(wx.Colour(50, 200, 50))
        mypie._series.append(part2)

        self.assertEqual(part1.GetLabel(), 'Label 1')
        self.assertEqual(part2.GetLabel(), 'Label 2')
        self.assertEqual(part1.GetValue(), 300)
        self.assertEqual(part2.GetValue(), 200)

        self.assertEqual(mypie.GetRotationAngle(), 0)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
