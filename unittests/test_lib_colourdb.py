import unittest
from unittests import wtc
import wx
import wx.lib.colourdb

#---------------------------------------------------------------------------

class lib_colourdb_Tests(wtc.WidgetTestCase):

    def test_lib_colourdb1(self):
        pnl = wx.Panel(self.frame)

        wx.lib.colourdb.updateColourDB()

        self.assertTrue(wx.TheColourDatabase.Find('NAVY').IsOk())
        self.assertTrue(wx.TheColourDatabase.Find('GREY93').IsOk())
        self.assertTrue(wx.TheColourDatabase.Find('MEDIUMPURPLE1').IsOk())

        self.assertEqual(wx.TheColourDatabase.Find('ORANGERED1'),
                         wx.Colour(255, 69, 0, 255))

        self.assertIn(wx.TheColourDatabase.FindName(wx.Colour(255, 69, 0)),
                      ['ORANGE RED', 'ORANGERED'])

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
