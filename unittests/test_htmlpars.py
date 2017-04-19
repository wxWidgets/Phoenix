import unittest
from unittests import wtc
import wx
import wx.html

#---------------------------------------------------------------------------

class htmlpars_Tests(wtc.WidgetTestCase):

    def test_htmlpars1(self):
        class myTagHandler(wx.html.HtmlTagHandler):
            def __init__(self):
                wx.html.HtmlTagHandler.__init__(self)
                self.test = None

            def GetSupportedTags(self):
                return 'FOO,BAR'

            def HandleTag(self, tag):
                self.test = tag.GetTagName()

        wx.html.HtmlWinParser_AddTagHandler(myTagHandler)
        self.myYield()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
