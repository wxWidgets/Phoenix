#---------------------------------------------------------------------------
# Name:        etg/webview.py
# Author:      Robin Dunn
#
# Created:     20-Nov-2012
# Copyright:   (c) 2012-2020 by Total Control Software
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
           'wxWebViewIE',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("""\
        #include <wx/webview.h>
        #if wxUSE_WEBVIEW_IE && defined(__WXMSW__)
            #include <wx/msw/webview_ie.h>
            #include <wx/msw/webview_edge.h>
        #endif
        """)
    module.addHeaderCode('#include <wx/filesys.h>')

    module.addGlobalStr('wxWebViewBackendDefault', 0)
    module.addGlobalStr('wxWebViewBackendIE', 0)
    module.addGlobalStr('wxWebViewBackendEdge', 0)
    module.addGlobalStr('wxWebViewBackendWebKit', 0)
    module.addGlobalStr('wxWebViewNameStr', 0)
    module.addGlobalStr('wxWebViewDefaultURLStr', 0)

    module.addHeaderCode("""\
        #if wxUSE_WEBVIEW && !defined(wxWebViewIE_H)
        enum wxWebViewIE_EmulationLevel
        {
            wxWEBVIEWIE_EMU_DEFAULT =    0,
            wxWEBVIEWIE_EMU_IE7 =        7000,
            wxWEBVIEWIE_EMU_IE8 =        8000,
            wxWEBVIEWIE_EMU_IE8_FORCE =  8888,
            wxWEBVIEWIE_EMU_IE9 =        9000,
            wxWEBVIEWIE_EMU_IE9_FORCE =  9999,
            wxWEBVIEWIE_EMU_IE10 =       10000,
            wxWEBVIEWIE_EMU_IE10_FORCE = 10001,
            wxWEBVIEWIE_EMU_IE11 =       11000,
            wxWEBVIEWIE_EMU_IE11_FORCE = 11001
        };
        #endif
        """)

    module.addPyCode(order=15, code="""\
        # On Windows we need to ensure that the wx package folder is on on the
        # PATH, so the MS Edge Loader DLLs can be found when they are dynamically
        # loaded.
        import os
        if os.name == 'nt':
            _path = os.environ.get('PATH')
            _pkg_path = os.path.abspath(os.path.dirname(wx.__file__))
            if _pkg_path.lower() not in _path.lower():
                os.environ['PATH'] = _path + os.pathsep + _pkg_path
        """)

    # Pull out the obj for wxWebViewIE so we can use it later, but not include it in the stubs
    wvie = module.find('wxWebViewIE')
    module.items.remove(wvie)

    # This tweak is needed only for the stub code
    module.find('wxWebViewHandler.wxWebViewHandler').argsString = '(const wxString& scheme="")'

    # Documented wrongly in 3.1.6 (needs to be fixed in stubs too)
    c = module.find('wxWebViewFactory')
    c.find('GetVersionInfo').argsString = '()'
    c.find('GetVersionInfo').items = []

    tools.generateStubs('wxUSE_WEBVIEW', module,
                        typeValMap={
                            'wxWebViewNavigationActionFlags': 'wxWEBVIEW_NAV_ACTION_NONE',
                            'wxWebViewZoom': 'wxWEBVIEW_ZOOM_MEDIUM',
                            'wxVersionInfo': 'wxVersionInfo()',
                            })

    c = module.find('wxWebView')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    c.abstract = True

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

    c.find('RunScript.output').out = True


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


    # Add the MSW methods in wxWebViewIE into the main WebView class like they were before.
    c.addItem(wvie.find('MSWSetEmulationLevel'))
    c.addItem(wvie.find('MSWSetModernEmulationLevel'))

    # Give them an implementation that doesn't matter which class they are actually located in.
    c.find('MSWSetEmulationLevel').setCppCode("""\
        #if wxUSE_WEBVIEW_IE && defined(__WXMSW__)
            return _do_MSWSetEmulationLevel(level);
        #else
            return false;
        #endif
        """)

    c.find('MSWSetModernEmulationLevel').setCppCode("""\
        #if wxUSE_WEBVIEW_IE && defined(__WXMSW__)
            return _do_MSWSetEmulationLevel(modernLevel ? wxWEBVIEWIE_EMU_IE8
                                                        : wxWEBVIEWIE_EMU_DEFAULT);
        #else
            return false;
        #endif
        """)

    # The emulation level is set as a per-application value in the Windows
    # Registry. The way this is implemented in the C++ code we end up with the
    # name of the _core extransion module in the Reistry instead of the .exe
    # name, which is what is really needed.
    #
    # So instead of doing simple wrappers with #if checks like normal, replace
    # these methods with a new implementation that does the RightThing using
    # sys.executable.
    c.addCppCode(r"""
        #if wxUSE_WEBVIEW_IE && defined(__WXMSW__)
        #include <wx/msw/webview_ie.h>
        #include <wx/msw/registry.h>

        bool _do_MSWSetEmulationLevel(wxWebViewIE_EmulationLevel level)
        {
            wxString programName;
            wxPyBLOCK_THREADS(
                programName = Py2wxString(PySys_GetObject("executable")));
            programName = programName.AfterLast('\\');

            // Registry key where emulation level for programs are set
            static const wxChar* IE_EMULATION_KEY =
                wxT("SOFTWARE\\Microsoft\\Internet Explorer\\Main")
                wxT("\\FeatureControl\\FEATURE_BROWSER_EMULATION");

            wxRegKey key(wxRegKey::HKCU, IE_EMULATION_KEY);
            if ( !key.Exists() )
            {
                wxLogWarning(_("Failed to find web view emulation level in the registry"));
                return false;
            }
            if ( level != wxWEBVIEWIE_EMU_DEFAULT )
            {
                if ( !key.SetValue(programName, level) )
                {
                    wxLogWarning(_("Failed to set web view to modern emulation level"));
                    return false;
                }
            }
            else
            {
                if ( !key.DeleteValue(programName) )
                {
                    wxLogWarning(_("Failed to reset web view to standard emulation level"));
                    return false;
                }
            }
            return true;
        }
        #endif
        """)


    c = module.find('wxWebViewEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_WEBVIEW_NAVIGATING = wx.PyEventBinder( wxEVT_WEBVIEW_NAVIGATING, 1 )
        EVT_WEBVIEW_NAVIGATED = wx.PyEventBinder( wxEVT_WEBVIEW_NAVIGATED, 1 )
        EVT_WEBVIEW_LOADED = wx.PyEventBinder( wxEVT_WEBVIEW_LOADED, 1 )
        EVT_WEBVIEW_ERROR = wx.PyEventBinder( wxEVT_WEBVIEW_ERROR, 1 )
        EVT_WEBVIEW_NEWWINDOW = wx.PyEventBinder( wxEVT_WEBVIEW_NEWWINDOW, 1 )
        EVT_WEBVIEW_TITLE_CHANGED = wx.PyEventBinder( wxEVT_WEBVIEW_TITLE_CHANGED, 1 )
        EVT_WEBVIEW_FULLSCREEN_CHANGED = wx.PyEventBinder( wxEVT_WEBVIEW_FULLSCREEN_CHANGED, 1)
        EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED = wx.PyEventBinder( wxEVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, 1)
        EVT_WEBVIEW_SCRIPT_RESULT = wx.PyEventBinder( wxEVT_WEBVIEW_SCRIPT_RESULT, 1)

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

