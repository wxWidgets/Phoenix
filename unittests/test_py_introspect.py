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


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
