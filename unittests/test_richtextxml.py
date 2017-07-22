import unittest
from unittests import wtc
import wx
import wx.richtext

#---------------------------------------------------------------------------

class richtextxml_Tests(wtc.WidgetTestCase):

    def test_richtextxml1(self):
        handler = wx.richtext.RichTextXMLHandler()
        wx.richtext.RichTextBuffer.AddHandler(handler)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
