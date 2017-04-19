import unittest
from unittests import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtexthtml_Tests(wtc.WidgetTestCase):

    def test_richtexthtml1(self):

        handler = wx.richtext.RichTextHTMLHandler()
        wx.richtext.RichTextBuffer.AddHandler(handler)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
