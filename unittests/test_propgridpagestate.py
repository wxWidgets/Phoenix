import unittest
from unittests import wtc

import wx.propgrid as pg

#---------------------------------------------------------------------------

class propgridpagestate_Tests(wtc.WidgetTestCase):


    def test_propgridpagestate01(self):
        r = pg.PropertyGridHitTestResult()


    def test_propgridpagestate02(self):
        ib = pg.PropertyGridIteratorBase()
        ii = pg.PropertyGridIterator()


    def test_propgridpagestate03(self):
        i = pg.PGVIterator()


    def test_propgridpagestate04(self):
        s = pg.PropertyGridPageState()




#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
