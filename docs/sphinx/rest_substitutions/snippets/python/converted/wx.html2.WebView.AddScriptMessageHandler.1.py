    
    # Install message handler with the name wx_msg
    self.webView.AddScriptMessageHandler('wx_msg')
    # Bind an event handler to receive those messages
    self.webView.Bind(wx.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self.handleMessage)
