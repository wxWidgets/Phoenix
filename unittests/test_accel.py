import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class accel_Tests(wtc.WidgetTestCase):


    def test_accelFlags(self):
        wx.ACCEL_ALT
        wx.ACCEL_CTRL
        wx.ACCEL_SHIFT
        wx.ACCEL_NORMAL
        wx.ACCEL_RAW_CTRL
        wx.ACCEL_CMD

    def test_accelNullObj(self):
        wx.NullAcceleratorTable
        self.assertTrue( not wx.NullAcceleratorTable.IsOk() )


    def test_accelEntry1(self):
        entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('A'), 123)
        self.assertTrue(entry.IsOk())
        self.assertTrue(entry.GetFlags() == wx.ACCEL_CTRL)
        self.assertTrue(entry.GetKeyCode() == ord('A'))
        self.assertTrue(entry.GetCommand() == 123)

    def test_accelEntry2(self):
        entry = wx.AcceleratorEntry(wx.ACCEL_CTRL, ord('A'), 123)
        self.assertTrue(entry.IsOk())
        self.assertTrue(entry.Flags == wx.ACCEL_CTRL)
        self.assertTrue(entry.KeyCode == ord('A'))
        self.assertTrue(entry.Command == 123)



    def test_accelTable1(self):
        tbl = wx.AcceleratorTable([ wx.AcceleratorEntry(wx.ACCEL_ALT,    ord('X'),   123),
                                    wx.AcceleratorEntry(wx.ACCEL_CTRL,   ord('H'),   234),
                                    wx.AcceleratorEntry(wx.ACCEL_CTRL,   ord('F'),   345),
                                    wx.AcceleratorEntry(wx.ACCEL_NORMAL, wx.WXK_F3,  456)
                                    ])
        self.frame.SetAcceleratorTable(tbl)

    def test_accelTable2(self):
        tbl = wx.AcceleratorTable([ (wx.ACCEL_ALT,    ord('X'),   123),
                                    (wx.ACCEL_CTRL,   ord('H'),   234),
                                    (wx.ACCEL_CTRL,   ord('F'),   345),
                                    (wx.ACCEL_NORMAL, wx.WXK_F3,  456)
                                    ])
        self.frame.SetAcceleratorTable(tbl)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
