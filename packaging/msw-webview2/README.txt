
msw-webview2
------------

This folder contains the DLLs used to interface with the Microsoft Edge browser
and use it as a backend for wx.html2.WebView. The appropriate architecture
version of the DLL will be copied into the wx package folder at build time.

The original copies of the DLLs can be found in the WebView2 SDK nuget:

    https://www.nuget.org/packages/Microsoft.Web.WebView2


The current version of Microsoft.Web.WebView2 being used here is 1.0.622.22.
Note that it may be necessary to have the Beta Channel version of Microsoft Edge
installed for this to work.

