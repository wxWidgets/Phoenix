
    # In Python the value returned will be a sip wrapper around a void* type,
    # and it can be converted to the address being pointed to with int().
    webview_ptr = self.webview.GetNativeBackend()

    # Assuming you are able to get a ctypes, cffi or similar access to the
    # webview library, you can use that pointer value to give it access to the
    # WebView backend to operate upon.
    theWebViewLib.doSomething(int(webview_ptr))
