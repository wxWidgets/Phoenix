import unittest
from unittests import wtc
import wx
import wx.propgrid as pg

#---------------------------------------------------------------------------

class propgridmanager_Tests(wtc.WidgetTestCase):

    def test_propgridmanager01(self):
        page = pg.PropertyGridPage()


    def test_propgridmanager02(self):
        mgr = pg.PropertyGridManager(self.frame)
        page1 = mgr.AddPage('label')


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
