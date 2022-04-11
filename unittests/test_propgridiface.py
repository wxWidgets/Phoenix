import unittest
from unittests import wtc

import wx.propgrid as pg

#---------------------------------------------------------------------------

class propgridiface_Tests(wtc.WidgetTestCase):

    def test_propgridiface01(self):
        arg = pg.PGPropArgCls('test_arg')


    def test_propgridiface02(self):
        with self.assertRaises(TypeError):
            iface = pg.PropertyGridInterface()


    def test_propgridiface03(self):
        # Ensure SetPropertyValue doesn't truncate floats
        pgrid = pg.PropertyGrid(self.frame)
        pgrid.Append(pg.FloatProperty('Float', value=123.456))

        value = pgrid.GetPropertyValue('Float')
        assert type(value) is float
        assert value == 123.456

        pgrid.SetPropertyValue('Float', 654.321)
        value = pgrid.GetPropertyValue('Float')
        assert type(value) is float
        assert value == 654.321


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
