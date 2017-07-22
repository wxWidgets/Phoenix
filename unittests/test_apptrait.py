import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class AppTraitsTests(wtc.WidgetTestCase):

    def test_AppTraits(self):
        t = self.app.GetTraits()
        self.assertTrue(t is not None)

        v = t.GetToolkitVersion()
        self.assertTrue( len(v) == 3)

        t.HasStderr()
        t.IsUsingUniversalWidgets()


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
