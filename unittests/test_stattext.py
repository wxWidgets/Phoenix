import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class stattext_Tests(wtc.WidgetTestCase):

    def test_stattextFlags(self):
        wx.ST_NO_AUTORESIZE
        wx.ST_ELLIPSIZE_START
        wx.ST_ELLIPSIZE_MIDDLE
        wx.ST_ELLIPSIZE_END


    def test_stattextCtor(self):
        t = wx.StaticText(self.frame, -1, "static text label")
        t = wx.StaticText(self.frame, label='label', style=wx.ST_NO_AUTORESIZE)


    def test_stattextDefaultCtor(self):
        t = wx.StaticText()
        t.Create(self.frame)



#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
