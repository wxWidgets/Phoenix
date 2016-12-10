import sys
import wx
import wx.html2 as webview

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.current = "http://wxPython.org"
        self.frame = self.GetTopLevelParent()
        self.titleBase = self.frame.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.wv = webview.WebView.New(self)
        self.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.OnWebViewNavigating, self.wv)
        self.Bind(webview.EVT_WEBVIEW_NAVIGATED, self.OnWebViewNavigated, self.wv)
        self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)
        self.Bind(webview.EVT_WEBVIEW_TITLE_CHANGED, self.OnWebViewTitleChanged, self.wv)

        btn = wx.Button(self, -1, "Open", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnOpenButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "<--", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoBack, btn)

        btn = wx.Button(self, -1, "-->", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnNextPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoForward, btn)

        btn = wx.Button(self, -1, "Stop", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnStopButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "Refresh", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        txt = wx.StaticText(self, -1, "Location:")
        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)

        self.location = wx.ComboBox(
            self, -1, "", style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
        self.location.AppendItems(['http://wxPython.org',
                                   'http://wxwidgets.org',
                                   'http://google.com'])

        #for url in ['http://wxPython.org',
        #            'http://wxwidgets.org',
        #            'http://google.com']:
        #    item = webview.WebViewHistoryItem(url, url)
        #    self.wv.LoadHistoryItem(item)

        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_TEXT_ENTER, self.OnLocationEnter)
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)


        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.wv, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.wv.LoadURL(self.current)



    # WebView events
    def OnWebViewNavigating(self, evt):
        # this event happens prior to trying to get a resource
        if evt.GetURL() == 'http://www.microsoft.com/':
            if wx.MessageBox("Are you sure you want to visit Microsoft?",
                             style=wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
                # This is how you can cancel loading a page.
                evt.Veto()


    def OnWebViewNavigated(self, evt):
        self.frame.SetStatusText("Loading %s..." % evt.GetURL())


    def OnWebViewLoaded(self, evt):
        # The full document has loaded
        self.current = evt.GetURL()
        self.location.SetValue(self.current)
        self.frame.SetStatusText("Loaded")


    def OnWebViewTitleChanged(self, evt):
        # Set the frame's title to include the document's title
        self.frame.SetTitle("%s -- %s" % (self.titleBase, evt.GetString()))


    # Control bar events
    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        print('OnLocationSelect: %s\n' % url)
        self.wv.LoadURL(url)

    def OnLocationEnter(self, evt):
        url = self.location.GetValue()
        self.location.Append(url)
        self.wv.LoadURL(url)


    def OnOpenButton(self, event):
        dlg = wx.TextEntryDialog(self, "Open Location",
                                "Enter a full URL or local path",
                                self.current, wx.OK|wx.CANCEL)
        dlg.CentreOnParent()

        if dlg.ShowModal() == wx.ID_OK:
            self.current = dlg.GetValue()
            self.wv.LoadURL(self.current)

        dlg.Destroy()

    def OnPrevPageButton(self, event):
        for i in self.wv.GetBackwardHistory():
            print("%s %s" % (i.Url, i.Title))
        self.wv.GoBack()

    def OnNextPageButton(self, event):
        for i in self.wv.GetForwardHistory():
            print("%s %s" % (i.Url, i.Title))
        self.wv.GoForward()

    def OnCheckCanGoBack(self, event):
        event.Enable(self.wv.CanGoBack())

    def OnCheckCanGoForward(self, event):
        event.Enable(self.wv.CanGoForward())

    def OnStopButton(self, evt):
        self.wv.Stop()

    def OnRefreshPageButton(self, evt):
        self.wv.Reload()


#----------------------------------------------------------------------


def main():
    app = wx.App()
    frm = wx.Frame(None, title="html2.WebView sample", size=(700,500))
    frm.CreateStatusBar()
    pnl = TestPanel(frm)
    frm.Show()
    app.MainLoop()


#----------------------------------------------------------------------

if __name__ == '__main__':
    main()
