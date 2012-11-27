import imp_unittest, unittest
import wtc
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
        webview.WEB_VIEW_ZOOM_TINY
        webview.WEB_VIEW_ZOOM_SMALL
        webview.WEB_VIEW_ZOOM_MEDIUM
        webview.WEB_VIEW_ZOOM_LARGE
        webview.WEB_VIEW_ZOOM_LARGEST
        webview.WEB_VIEW_ZOOM_TYPE_LAYOUT
        webview.WEB_VIEW_ZOOM_TYPE_TEXT
        webview.WEB_NAV_ERR_CONNECTION
        webview.WEB_NAV_ERR_CERTIFICATE
        webview.WEB_NAV_ERR_AUTH
        webview.WEB_NAV_ERR_SECURITY
        webview.WEB_NAV_ERR_NOT_FOUND
        webview.WEB_NAV_ERR_REQUEST
        webview.WEB_NAV_ERR_USER_CANCELLED
        webview.WEB_NAV_ERR_OTHER
        webview.WEB_VIEW_RELOAD_DEFAULT
        webview.WEB_VIEW_RELOAD_NO_CACHE
        webview.WEB_VIEW_FIND_WRAP
        webview.WEB_VIEW_FIND_ENTIRE_WORD
        webview.WEB_VIEW_FIND_MATCH_CASE
        webview.WEB_VIEW_FIND_HIGHLIGHT_RESULT
        webview.WEB_VIEW_FIND_BACKWARDS
        webview.WEB_VIEW_FIND_DEFAULT
        webview.WEB_VIEW_BACKEND_DEFAULT
        webview.WEB_VIEW_BACKEND_WEBKIT
        webview.WEB_VIEW_BACKEND_IE


    def test_webview6(self):
        webview.wxEVT_COMMAND_WEB_VIEW_NAVIGATING
        webview.wxEVT_COMMAND_WEB_VIEW_NAVIGATED
        webview.wxEVT_COMMAND_WEB_VIEW_LOADED
        webview.wxEVT_COMMAND_WEB_VIEW_ERROR
        webview.wxEVT_COMMAND_WEB_VIEW_NEWWINDOW
        webview.wxEVT_COMMAND_WEB_VIEW_TITLE_CHANGED
        
        webview.EVT_WEB_VIEW_NAVIGATING
        webview.EVT_WEB_VIEW_NAVIGATED
        webview.EVT_WEB_VIEW_LOADED
        webview.EVT_WEB_VIEW_ERROR
        webview.EVT_WEB_VIEW_NEWWINDOW
        webview.EVT_WEB_VIEW_TITLE_CHANGED
        
        

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
