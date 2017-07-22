import unittest
from unittests import wtc

import wx
import wx.propgrid as pg

#---------------------------------------------------------------------------

class propgridadvprops_Tests(wtc.WidgetTestCase):


    def test_propgridadvprops01(self):
        pg.PG_COLOUR_WEB_BASE
        pg.PG_COLOUR_CUSTOM
        pg.PG_COLOUR_UNSPECIFIED


    def test_propgridadvprops02(self):
        cv1 = pg.ColourPropertyValue()
        cv2 = pg.ColourPropertyValue(cv1)
        cv3 = pg.ColourPropertyValue(wx.RED)


    def test_propgridadvprops03(self):
        pass


    def test_propgridadvprops04(self):
        fp1 = pg.FontProperty()
        fp2 = pg.FontProperty('label', 'name',
                    wx.Font(wx.FontInfo(10).Family(wx.SWISS).Bold()))


    def test_propgridadvprops05(self):
        p = pg.SystemColourProperty()


    def test_propgridadvprops06(self):
        p = pg.ColourProperty()


    def test_propgridadvprops07(self):
        p = pg.CursorProperty()


    def test_propgridadvprops08(self):
        p = pg.ImageFileProperty()


    def test_propgridadvprops09(self):
        p = pg.MultiChoiceProperty()
        p = pg.MultiChoiceProperty('label', 'name',
                                   choices=['The', 'Quick', 'Brown', 'Fox'],
                                   value=['Brown', 'Fox'])


    def test_propgridadvprops10(self):
        p = pg.DateProperty()




#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
