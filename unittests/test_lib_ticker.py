import unittest
from unittests import wtc
from wx.lib.ticker import Ticker

#---------------------------------------------------------------------------

class lib_ticker_Tests(wtc.WidgetTestCase):

    def test_lib_ticker(self):
        self.ticker = Ticker(self.frame)

        txt = 'a nice ticker text'
        self.ticker.SetText(txt)
        self.assertEqual(self.ticker.GetText(), txt)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
