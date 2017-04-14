import unittest
from unittests import wtc
import wx
import wx.html2 as webview

#---------------------------------------------------------------------------

class webview_Tests(wtc.WidgetTestCase):

    def test_webview1(self):
        wv = webview.WebView.New()
        wv.Create(self.frame)

    def test_webview2(self):
        wv = webview.WebView.New(self.frame)

    def test_webview3(self):
        wv = webview.WebView.New(self.frame)
        self.frame.SendSizeEvent()
        wv.LoadURL('file://' + __file__)
        while wv.IsBusy():
            self.myYield()
        h = wv.GetBackwardHistory()
        self.assertTrue(isinstance(h, list))
        if len(h):
            self.assertTrue(isinstance(h[0], webview.WebViewHistoryItem))


    def test_webview5(self):
        webview.WEBVIEW_ZOOM_TINY
        webview.WEBVIEW_ZOOM_SMALL
        webview.WEBVIEW_ZOOM_MEDIUM
        webview.WEBVIEW_ZOOM_LARGE
        webview.WEBVIEW_ZOOM_LARGEST
        webview.WEBVIEW_ZOOM_TYPE_LAYOUT
        webview.WEBVIEW_ZOOM_TYPE_TEXT
        webview.WEBVIEW_NAV_ERR_CONNECTION
        webview.WEBVIEW_NAV_ERR_CERTIFICATE
        webview.WEBVIEW_NAV_ERR_AUTH
        webview.WEBVIEW_NAV_ERR_SECURITY
        webview.WEBVIEW_NAV_ERR_NOT_FOUND
        webview.WEBVIEW_NAV_ERR_REQUEST
        webview.WEBVIEW_NAV_ERR_USER_CANCELLED
        webview.WEBVIEW_NAV_ERR_OTHER
        webview.WEBVIEW_RELOAD_DEFAULT
        webview.WEBVIEW_RELOAD_NO_CACHE
        webview.WEBVIEW_FIND_WRAP
        webview.WEBVIEW_FIND_ENTIRE_WORD
        webview.WEBVIEW_FIND_MATCH_CASE
        webview.WEBVIEW_FIND_HIGHLIGHT_RESULT
        webview.WEBVIEW_FIND_BACKWARDS
        webview.WEBVIEW_FIND_DEFAULT

        webview.WebViewBackendDefault
        webview.WebViewBackendIE
        webview.WebViewBackendWebKit


    def test_webview6(self):
        webview.wxEVT_COMMAND_WEBVIEW_NAVIGATING
        webview.wxEVT_COMMAND_WEBVIEW_NAVIGATED
        webview.wxEVT_COMMAND_WEBVIEW_LOADED
        webview.wxEVT_COMMAND_WEBVIEW_ERROR
        webview.wxEVT_COMMAND_WEBVIEW_NEWWINDOW
        webview.wxEVT_COMMAND_WEBVIEW_TITLE_CHANGED

        webview.EVT_WEBVIEW_NAVIGATING
        webview.EVT_WEBVIEW_NAVIGATED
        webview.EVT_WEBVIEW_LOADED
        webview.EVT_WEBVIEW_ERROR
        webview.EVT_WEBVIEW_NEWWINDOW
        webview.EVT_WEBVIEW_TITLE_CHANGED



#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
