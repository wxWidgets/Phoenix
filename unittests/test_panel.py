import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class panel_Tests(wtc.WidgetTestCase):

    def test_panelCtor(self):
        p = wx.Panel(self.frame)

    def test_panelDefaultCtor(self):
        p = wx.Panel()
        p.Create(self.frame)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
