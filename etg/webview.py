#---------------------------------------------------------------------------
# Name:        etg/webview.py
# Author:      Robin Dunn
#
# Created:     20-Nov-2012
# Copyright:   (c) 2012-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_html2"
NAME      = "webview"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxWebViewHistoryItem',
           'wxWebViewHandler',
           'wxWebViewArchiveHandler',
           'wxWebViewFSHandler',
           'wxWebView',
           'wxWebViewEvent',
           'wxWebViewFactory',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/webview.h>')

    module.addGlobalStr('wxWebViewBackendDefault')
    module.addGlobalStr('wxWebViewBackendIE')
    module.addGlobalStr('wxWebViewBackendWebKit')

    c = module.find('wxWebView')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    c.abstract = True

    module.addGlobalStr('wxWebViewNameStr', c)
    module.addGlobalStr('wxWebViewDefaultURLStr', c)

    for m in c.find('New').all():
        m.factory = True
    c.find('New.id').default = 'wxID_ANY'
    c.find('New.parent').transferThis = True


    c.find('RegisterHandler.handler').type = 'wxWebViewHandler*'
    c.find('RegisterHandler.handler').transfer = True
    c.find('RegisterHandler').setCppCode_sip(
        "sipCpp->RegisterHandler(wxSharedPtr<wxWebViewHandler>(handler));")


    c.find('RegisterFactory.factory').type = 'wxWebViewFactory*'
    c.find('RegisterFactory.factory').transfer = True
    c.find('RegisterFactory').setCppCode_sip(
        "wxWebView::RegisterFactory(*backend, wxSharedPtr<wxWebViewFactory>(factory));")


    # Custom code to deal with the
    # wxVector<wxSharedPtr<wxWebViewHistoryItem>> return type of these two
    # methods. We'll just convert them to a Python list of history items.
    code = """\
        wxPyThreadBlocker blocker;
        PyObject* result = PyList_New(0);
        wxVector<wxSharedPtr<wxWebViewHistoryItem> >  vector = self->{method}();
        for (size_t idx=0; idx < vector.size(); idx++) {{
            PyObject* obj;
            wxWebViewHistoryItem* item = new wxWebViewHistoryItem(*vector[idx].get());
            obj = wxPyConstructObject((void*)item, "wxWebViewHistoryItem", true);
            PyList_Append(result, obj);
            Py_DECREF(obj);
        }}
        return result;
        """
    c.find('GetBackwardHistory').type = 'PyObject*'
    c.find('GetBackwardHistory').setCppCode(code.format(method='GetBackwardHistory'))
    c.find('GetForwardHistory').type = 'PyObject*'
    c.find('GetForwardHistory').setCppCode(code.format(method='GetForwardHistory'))


    # Since LoadHistoryItem expects to get an actual item in the history
    # list, and since we make copies of the items in the cppCode above, then
    # this won't be possible to do from the Python wrappers. However, it's
    # just as easy to use LoadURL to reload a history item so it's not a
    # great loss.
    c.find('LoadHistoryItem').ignore()
    ##c.find('LoadHistoryItem.item').type = 'wxWebViewHistoryItem*'
    ##c.find('LoadHistoryItem.item').transfer = True
    ##c.find('LoadHistoryItem').setCppCode_sip(
    ##    "sipCpp->LoadHistoryItem(wxSharedPtr<wxWebViewHistoryItem>(item));")





    c = module.find('wxWebViewEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_WEBVIEW_NAVIGATING = wx.PyEventBinder( wxEVT_WEBVIEW_NAVIGATING, 1 )
        EVT_WEBVIEW_NAVIGATED = wx.PyEventBinder( wxEVT_WEBVIEW_NAVIGATED, 1 )
        EVT_WEBVIEW_LOADED = wx.PyEventBinder( wxEVT_WEBVIEW_LOADED, 1 )
        EVT_WEBVIEW_ERROR = wx.PyEventBinder( wxEVT_WEBVIEW_ERROR, 1 )
        EVT_WEBVIEW_NEWWINDOW = wx.PyEventBinder( wxEVT_WEBVIEW_NEWWINDOW, 1 )
        EVT_WEBVIEW_TITLE_CHANGED = wx.PyEventBinder( wxEVT_WEBVIEW_TITLE_CHANGED, 1 )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_WEBVIEW_NAVIGATING     = wxEVT_WEBVIEW_NAVIGATING
        wxEVT_COMMAND_WEBVIEW_NAVIGATED      = wxEVT_WEBVIEW_NAVIGATED
        wxEVT_COMMAND_WEBVIEW_LOADED         = wxEVT_WEBVIEW_LOADED
        wxEVT_COMMAND_WEBVIEW_ERROR          = wxEVT_WEBVIEW_ERROR
        wxEVT_COMMAND_WEBVIEW_NEWWINDOW      = wxEVT_WEBVIEW_NEWWINDOW
        wxEVT_COMMAND_WEBVIEW_TITLE_CHANGED  = wxEVT_WEBVIEW_TITLE_CHANGED
        """)


    c = module.find('wxWebViewHistoryItem')
    tools.addAutoProperties(c)


    for name in [ 'wxWebViewHandler',
                  'wxWebViewArchiveHandler',
                  'wxWebViewFSHandler' ]:
        c = module.find(name)
        c.find('GetFile').factory = True


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

