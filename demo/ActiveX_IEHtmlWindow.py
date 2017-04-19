#!/usr/bin/env python

# 11/18/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o Updated for wx namespace


import wx

if wx.Platform == '__WXMSW__':
    import wx.lib.iewin as iewin

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log, frame=None):
        wx.Panel.__init__(
            self, parent, -1,
            style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN|wx.NO_FULL_REPAINT_ON_RESIZE
            )

        self.log = log
        self.current = "http://wxPython.org/"
        self.frame = frame

        if frame:
            self.titleBase = frame.GetTitle()

        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.ie = iewin.IEHtmlWindow(self)


        btn = wx.Button(self, -1, "Open", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnOpenButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "Home", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnHomeButton, btn)
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

        btn = wx.Button(self, -1, "Search", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnSearchPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        btn = wx.Button(self, -1, "Refresh", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.OnRefreshPageButton, btn)
        btnSizer.Add(btn, 0, wx.EXPAND|wx.ALL, 2)

        txt = wx.StaticText(self, -1, "Location:")
        btnSizer.Add(txt, 0, wx.CENTER|wx.ALL, 2)

        self.location = wx.ComboBox(
                            self, -1, "", style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER
                            )

        self.Bind(wx.EVT_COMBOBOX, self.OnLocationSelect, self.location)
        self.location.Bind(wx.EVT_KEY_UP, self.OnLocationKey)
        self.location.Bind(wx.EVT_CHAR, self.IgnoreReturn)
        btnSizer.Add(self.location, 1, wx.EXPAND|wx.ALL, 2)

        sizer.Add(btnSizer, 0, wx.EXPAND)
        sizer.Add(self.ie, 1, wx.EXPAND)

        self.ie.LoadUrl(self.current)
        self.location.Append(self.current)

        self.SetSizer(sizer)
        # Since this is a wx.Window we have to call Layout ourselves
        self.Bind(wx.EVT_SIZE, self.OnSize)


        ## Hook up the event handlers for the IE window.  Using
        ## AddEventSink is how we tell the COM system to look in this
        ## object for method names matching the COM Event names.  They
        ## are automatically looked for in the ActiveXCtrl class, (so
        ## deriving a new class from IEHtmlWindow would also have been
        ## a good appraoch) and now they will be looked for here too.
        self.ie.AddEventSink(self)



    def ShutdownDemo(self):
        # put the frame title back
        if self.frame:
            self.frame.SetTitle(self.titleBase)


    def OnSize(self, evt):
        self.Layout()

    def OnLocationSelect(self, evt):
        url = self.location.GetStringSelection()
        self.log.write('OnLocationSelect: %s\n' % url)
        self.ie.Navigate(url)

    def OnLocationKey(self, evt):
        if evt.GetKeyCode() == wx.WXK_RETURN:
            URL = self.location.GetValue()
            self.location.Append(URL)
            self.ie.Navigate(URL)
        else:
            evt.Skip()


    def IgnoreReturn(self, evt):
        if evt.GetKeyCode() != wx.WXK_RETURN:
            evt.Skip()

    def OnOpenButton(self, event):
        dlg = wx.TextEntryDialog(self, "Open Location",
                                "Enter a full URL or local path",
                                self.current, wx.OK|wx.CANCEL)
        dlg.CentreOnParent()

        if dlg.ShowModal() == wx.ID_OK:
            self.current = dlg.GetValue()
            self.ie.Navigate(self.current)

        dlg.Destroy()

    def OnHomeButton(self, event):
        self.ie.GoHome()    ## ET Phone Home!

    def OnPrevPageButton(self, event):
        self.ie.GoBack()

    def OnNextPageButton(self, event):
        self.ie.GoForward()

    def OnCheckCanGoBack(self, event):
        event.Enable(self.ie.CanGoBack())

    def OnCheckCanGoForward(self, event):
        event.Enable(self.ie.CanGoForward())

    def OnStopButton(self, evt):
        self.ie.Stop()

    def OnSearchPageButton(self, evt):
        self.ie.GoSearch()

    def OnRefreshPageButton(self, evt):
        self.ie.Refresh(iewin.REFRESH_COMPLETELY)


    # Here are some of the event methods for the IE COM events.  See
    # the MSDN docs for DWebBrowserEvents2 for details on what events
    # are available, and what the parameters are.

    def BeforeNavigate2(self, this, pDisp, URL, Flags, TargetFrameName,
                        PostData, Headers, Cancel):
        self.log.write('BeforeNavigate2: %s\n' % URL[0])
        if URL[0] == 'http://www.microsoft.com/':
            if wx.MessageBox("Are you sure you want to visit Microsoft?",
                             style=wx.YES_NO|wx.ICON_QUESTION) == wx.NO:
                # This is how you can cancel loading a page.  The
                # Cancel parameter is defined as an [in,out] type and
                # so setting the value means it will be returned and
                # checked in the COM control.
                Cancel[0] = True


    def NewWindow3(self, this, pDisp, Cancel, Flags, urlContext, URL):
        self.log.write('NewWindow3: %s\n' % URL)
        Cancel[0] = True   # Veto the creation of a  new window.

    #def ProgressChange(self, this, progress, progressMax):
    #    self.log.write('ProgressChange: %d of %d\n' % (progress, progressMax))

    def DocumentComplete(self, this, pDisp, URL):
        self.current = URL[0]
        self.location.SetValue(self.current)

    def TitleChange(self, this, Text):
        if self.frame:
            self.frame.SetTitle(self.titleBase + ' -- ' + Text)

    def StatusTextChange(self, this, Text):
        if self.frame:
            self.frame.SetStatusText(Text)



#----------------------------------------------------------------------
# for the demo framework...

def runTest(frame, nb, log):
    if wx.Platform == '__WXMSW__':
        win = TestPanel(nb, log, frame)
        return win
    else:
        from wx.lib.msgpanel import MessagePanel
        win = MessagePanel(nb, 'This demo only works on Microsoft Windows.',
                           'Sorry', wx.ICON_WARNING)
        return win



overview = """\
<html><body>
<h2>wx.lib.iewin.IEHtmlWindow</h2>

The wx.lib.iewin.IEHtmlWindow class is one example of using ActiveX
controls from wxPython using the new wx.activex module.  This allows
you to use an ActiveX control as if it is a wx.Window, you can call
its methods, set/get properties, and receive events from the ActiveX
control in a very intuitive way.

<p> Using this class is simpler than ActiveXWrapper, doesn't rely on
the win32all extensions, and is more "wx\'ish", meaning that it uses
events and etc. as would be expected from any other wx window.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])



#----------------------------------------------------------------------

