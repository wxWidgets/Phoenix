import sys
import os
from six import BytesIO

import wx
import wx.html2 as webview

HERE = os.path.abspath(os.path.dirname(__file__))
BASE = 'file://{}/'.format(HERE.replace('\\', '/'))
URL = BASE + 'webview_sample.html'
LOGO = os.path.join(HERE, 'logo.png')

# We need to be in the HERE folder for the archive link to work since the sample
# page does not use a full path
os.chdir(HERE)

#--------------------------------------------------------------------------

class SampleFrame(wx.Frame):
    def __init__(self, parent, url=URL):
        wx.Frame.__init__(self, parent, title="html2.WebView Sample", size=(800,900))
        # add a statusbar
        self.CreateStatusBar()

        # Add a menubar with just a quit item
        mb = wx.MenuBar()
        menu = wx.Menu()
        menu.Append(wx.ID_EXIT, '&Quit')
        mb.Append(menu, "File")
        self.SetMenuBar(mb)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=wx.ID_EXIT)

        # Create the main panel
        pnl = WebViewPanel(self, url)

    # Menu event handler to close the frame
    def OnQuit(self, evt):
        self.Close(force=True)

#--------------------------------------------------------------------------

class WebViewPanel(wx.Panel):
    def __init__(self, parent, url):
        wx.Panel.__init__(self, parent)

        self.current = url
        self.frame = self.GetTopLevelParent()
        self.titleBase = self.frame.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Ensure that a newer version of the IE/Edge control will be used
        #  on Windows
        webview.WebView.MSWSetEmulationLevel()

        # Create the webView control
        self.wv = webview.WebView.New(self)

        # Register a handler for the memory: file system
        self.wv.RegisterHandler(webview.WebViewFSHandler("memory"))

        # This handler takes care of links that are in zip files
        self.wv.RegisterHandler(webview.WebViewArchiveHandler("wxzip"))

        # And this one is for the custom: file system implemented by the
        # CustomWebViewHandler class below
        self.wv.RegisterHandler(CustomWebViewHandler())

        self.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.OnWebViewNavigating, self.wv)
        self.Bind(webview.EVT_WEBVIEW_NAVIGATED, self.OnWebViewNavigated, self.wv)
        self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)
        self.Bind(webview.EVT_WEBVIEW_TITLE_CHANGED, self.OnWebViewTitleChanged, self.wv)

        btn = wx.Button(self, -1, "Open", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnOpenButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "◀︎", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnPrevPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanGoBack, btn)

        btn = wx.Button(self, -1, "▶︎", style=wx.BU_EXACTFIT)
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
        if evt.GetURL() == 'https://www.microsoft.com/':
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
        #for i in self.wv.GetBackwardHistory():
        #    print("%s %s" % (i.Url, i.Title))
        self.wv.GoBack()

    def OnNextPageButton(self, event):
        #for i in self.wv.GetForwardHistory():
        #    print("%s %s" % (i.Url, i.Title))
        self.wv.GoForward()

    def OnCheckCanGoBack(self, event):
        event.Enable(self.wv.CanGoBack())

    def OnCheckCanGoForward(self, event):
        event.Enable(self.wv.CanGoForward())

    def OnStopButton(self, evt):
        self.wv.Stop()

    def OnRefreshPageButton(self, evt):
        self.wv.Reload()



#--------------------------------------------------------------------------

def SetupMemoryFiles():
    # Set up an in-memory file system with virtual "files" that can be
    # loaded into the webview just like network or local file sources.
    # These "files" can be access using a protocol specifier of "memory:"
    wx.FileSystem.AddHandler(wx.MemoryFSHandler())
    wx.FileSystem.AddHandler(wx.ArchiveFSHandler())
    wx.MemoryFSHandler.AddFile(
        "page1.html",
        "<html><head><title>File System Example</title>"
        "<link rel='stylesheet' type='text/css' href='memory:test.css'>"
        "</head><body><h1>Page 1</h1>"
        "<p><img src='memory:logo.png'></p>"
        "<p>This file was loaded directly from a virtual in-memory filesystem.</p>"
        "<p>Here's another page: <a href='memory:page2.html'>Page 2</a>.</p></body>")
    wx.MemoryFSHandler.AddFile(
        "page2.html",
        "<html><head><title>File System Example</title>"
        "<link rel='stylesheet' type='text/css' href='memory:test.css'>"
        "</head><body><h1>Page 2</h1>"
        "<p><a href='memory:page1.html'>Page 1</a> was better.</p></body>")
    wx.MemoryFSHandler.AddFile(
        "test.css",
        "h1 {color: red;}")
    wx.MemoryFSHandler.AddFile('logo.png', wx.Bitmap(LOGO), wx.BITMAP_TYPE_PNG)

#--------------------------------------------------------------------------

class CustomWebViewHandler(webview.WebViewHandler):
    # This shows how to make a custom handler for providing content to the
    # WebView for a specific scheme ("custom:" in this case).  This handler
    # class simply needs to implement the GetFile method, which will be called
    # whenever a resource with a matching scheme is to be loaded, and it needs
    # to respond by returning a wx.FSFile object.  This means that, unlike the
    # wx.MemoryFSHandler, content can be generated on the fly rather than
    # needing to be preloaded into a filesystem.
    #

    def __init__(self):
        wx.html2.WebViewHandler.__init__(self, 'custom')
        self.count = 0

    def GetFile(self, uri):
        # We'll just provide the same content for every URI in this example, but
        # normally you would generate or fetch appropriate content that is
        # referenced by the given URI.
        self.count += 1
        content = """\
            <html><head><title>Custom Handler Example</title></head>
            <body><h1>Custom Handler Example</h1>
            <p>This page is provided dynamically from the CustomWebViewHandler class.</p>
            <p>It has been loaded {} times.</p>
            </body></html>""".format(self.count)
        stream = BytesIO(content.encode('utf-8'))
        fsfile = wx.FSFile(stream, uri, 'page1.html', 'text/html', wx.DateTime.Now())
        return fsfile

#--------------------------------------------------------------------------

def main():
    app = wx.App()
    SetupMemoryFiles()
    frm = SampleFrame(None)
    frm.Show()
    app.MainLoop()


#--------------------------------------------------------------------------

if __name__ == '__main__':
    main()
