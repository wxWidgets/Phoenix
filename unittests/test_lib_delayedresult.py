import unittest
from unittests import wtc

import wx.lib.delayedresult as delayedresult

#---------------------------------------------------------------------------

class lib_delayedresult_Tests(wtc.WidgetTestCase):

    def test_lib_delayedresultAbortEvent(self):
        abort = delayedresult.AbortEvent()
        self.assertIsNone(abort())
        abort.set()
        with self.assertRaises(delayedresult.AbortedException):
            abort()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
