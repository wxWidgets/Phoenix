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




#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
