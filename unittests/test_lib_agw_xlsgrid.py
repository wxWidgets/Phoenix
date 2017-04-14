import unittest
from unittests import wtc
import wx

try:
    import wx.lib.agw.xlsgrid as XG
    skipIt = False
except:
    skipIt = False

#---------------------------------------------------------------------------

class lib_agw_xlsgrid_Tests(wtc.WidgetTestCase):

    @unittest.skipIf(skipIt, 'Requires xlrd')
    def test_lib_agw_xlsgridCtor(self):
        xg = XG.XLSGrid(self.frame)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
