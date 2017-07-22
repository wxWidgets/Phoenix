import unittest
from unittests import wtc
import wx

import wx.lib.agw.floatspin as FS

#---------------------------------------------------------------------------

class lib_agw_floatspin_Tests(wtc.WidgetTestCase):

    def test_lib_agw_floatspinCtor(self):
        floatspin = FS.FloatSpin(self.frame, min_val=0, max_val=1,
                                 increment=0.01, value=0.1, agwStyle=FS.FS_LEFT)
        floatspin.SetFormat('%f')
        floatspin.SetDigits(2)

    def test_lib_agw_floatspinMethods(self):
        floatspin = FS.FloatSpin(self.frame, min_val=0, max_val=1,
                                 increment=0.01, value=0.1, agwStyle=FS.FS_LEFT)
        floatspin.SetFormat('%f')
        floatspin.SetDigits(2)

        # Some methods tests...
        self.assertTrue(floatspin.GetFormat() == '%f')
        self.assertEqual(floatspin.GetDigits(), 2)

        # Should not be possible to set 100...
        floatspin.SetValue(100.0)
        self.assertTrue(floatspin.GetValue() == 0.1)

        floatspin.SetValue(0.2)
        floatspin.SetToDefaultValue()
        self.assertTrue(floatspin.GetValue() == 0.1)

        self.assertTrue(floatspin.IsFinite(floatspin.GetValue()))
        self.assertTrue(not floatspin.InRange(50))
        self.assertTrue(floatspin.HasRange())

        self.assertEqual(floatspin.GetMin(), 0)
        self.assertEqual(floatspin.GetMax(), 1)
        self.assertEqual(floatspin.GetIncrement(), FS.FixedPoint(str(0.01), 20))


    def test_lib_agw_floatspinConstantsExist(self):
        FS.DEFAULT_PRECISION
        FS.FS_CENTRE
        FS.FS_LEFT
        FS.FS_READONLY
        FS.FS_RIGHT

    def test_lib_agw_floatspinEvents(self):
        FS.EVT_FLOATSPIN
        FS.wxEVT_FLOATSPIN

    def test_lib_agw_floatspin_fixedpoint(self):
        f1 = FS.FixedPoint(20)
        f2 = FS.FixedPoint(30)
        f3 = FS.FixedPoint("20", 20)
        f4 = FS.FixedPoint("20", 20)

        self.assertEqual(f1, 20)
        self.assertEqual(f2, 30)
        self.assertEqual(f3, f4)
        self.assertGreaterEqual(f2, f1)
        self.assertGreaterEqual(f2, 20)
        self.assertGreater(f2, 20)
        self.assertLessEqual(f1, f2)
        self.assertLessEqual(f1, 30)
        self.assertLess(f1, 30)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
