import unittest
from unittests import wtc
import wx
import wx.propgrid as pg

import six

#---------------------------------------------------------------------------

class pgvariant_Tests(wtc.WidgetTestCase):


    @unittest.skipIf(not hasattr(pg, 'testPGVariantTypemap'), '')
    def test_pgvariant1(self):
        d1 = wx.Point(123,456)
        d2 = pg.testPGVariantTypemap(d1)
        assert isinstance(d2, wx.Point)
        assert d1 == d2

    @unittest.skipIf(not hasattr(pg, 'testPGVariantTypeName'), '')
    def test_pgvariant2(self):
        d1 = wx.Point(123,456)
        assert pg.testPGVariantTypeName(d1) == 'wxPoint'



    @unittest.skipIf(not hasattr(pg, 'testPGVariantTypemap'), '')
    def test_pgvariant3(self):
        d1 = wx.Size(123,456)
        d2 = pg.testPGVariantTypemap(d1)
        assert isinstance(d2, wx.Size)
        assert d1 == d2

    @unittest.skipIf(not hasattr(pg, 'testPGVariantTypeName'), '')
    def test_pgvariant4(self):
        d1 = wx.Size(123,456)
        assert pg.testPGVariantTypeName(d1) == 'wxSize'



    @unittest.skipIf(not hasattr(pg, 'testPGVariantTypemap'), '')
    def test_pgvariant5(self):
        d1 = wx.Font( wx.FontInfo(10).Bold().Underlined() )
        d2 = pg.testPGVariantTypemap(d1)
        assert isinstance(d2, wx.Font)
        assert d2.PointSize == 10

    @unittest.skipIf(not hasattr(pg, 'testPGVariantTypeName'), '')
    def test_pgvariant6(self):
        d1 = wx.Font( wx.FontInfo(10).Bold().Underlined() )
        assert pg.testPGVariantTypeName(d1) == 'wxFont'



    @unittest.skipIf(not hasattr(pg, 'testPGVariantTypemap'), '')
    def test_pgvariant7(self):
        d1 = [0,1,2,3,4,5,6,7,8,9]
        d2 = pg.testPGVariantTypemap(d1)
        assert isinstance(d2, list)
        assert d1 == d2

        d1 = (123,456)
        d2 = pg.testPGVariantTypemap(d1)
        assert isinstance(d2, list)
        assert list(d1) == d2

    @unittest.skipIf(not hasattr(pg, 'testPGVariantTypeName'), '')
    def test_pgvariant8(self):
        d1 = [0,1,2,3,4,5,6,7,8,9]
        assert pg.testPGVariantTypeName(d1) == 'wxArrayInt'

        d1 = (123,456)
        assert pg.testPGVariantTypeName(d1) == 'wxArrayInt'



    @unittest.skipIf(not hasattr(pg, 'testPGVariantTypemap'), '')
    def test_pgvariant9(self):
        d1 = None
        d2 = pg.testPGVariantTypemap(d1)
        self.assertTrue(d2 is None)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
