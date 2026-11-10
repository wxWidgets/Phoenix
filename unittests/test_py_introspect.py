import sys
import unittest

import wx.py.introspect as inrspct

#---------------------------------------------------------------------------

class py_introspect_Tests(unittest.TestCase):

    def test_getAutoCompleteList(self):
        # introspect is expecting this! usually inited by wx.py.interpreter
        sys.ps2 = '... '
        attributes = inrspct.getAutoCompleteList("wx.")
        self.assertTrue(len(attributes) > 100)

    def test_getAutoCompleteListGetattrRaises(self):
        # Like ctypes.windll before Python 3.12
        class Loader:
            value = 1
            def __getattr__(self, name):
                raise OSError('Could not find module ' + name)

        sys.ps2 = '... '
        attributes = inrspct.getAutoCompleteList('loader.', {'loader': Loader()})
        self.assertIn('value', attributes)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
