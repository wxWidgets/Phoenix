import unittest
from unittests import wtc
import wx
import wx.html

#---------------------------------------------------------------------------

class htmlwinpars_Tests(wtc.WidgetTestCase):

    def test_htmlwinpars1(self):
        obj = wx.html.HtmlWinParser()

    def test_htmlwinpars_AddTagHandlerWrongType(self):
        class WrongTypeTagHandler(wx.html.HtmlTagHandler):
            def GetSupportedTags(self):
                return 'HTMLWINPARSWRONGTYPETAG'

        tags = []
        class MyTagHandler(wx.html.HtmlWinTagHandler):
            def GetSupportedTags(self):
                return 'HTMLWINPARSVALIDTAG'
            def HandleTag(self, tag):
                tags.append(tag.GetName())
                return False

        # A handler class that can't be used should not stop the handler
        # classes added after it from being used
        wx.html.HtmlWinParser_AddTagHandler(WrongTypeTagHandler)
        wx.html.HtmlWinParser_AddTagHandler(MyTagHandler)
        htmlwin = wx.html.HtmlWindow(self.frame)
        htmlwin.SetPage('<html><body><htmlwinparsvalidtag></body></html>')
        self.assertIn('HTMLWINPARSVALIDTAG', tags)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
