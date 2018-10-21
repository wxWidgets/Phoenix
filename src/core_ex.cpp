
#ifdef __WXMSW__             // If building for Windows...

#include <wx/msw/private.h>
#include <wx/msw/winundef.h>
#include <wx/msw/msvcrt.h>

//----------------------------------------------------------------------
// Use an ActivationContext to ensure that the new (themed) version of
// the comctl32 DLL is loaded.
//----------------------------------------------------------------------

// Note that the use of the ISOLATION_AWARE_ENABLED define replaces the
// activation context APIs with wrappers that dynamically load the API
// pointers from the kernel32 DLL so we don't have to do that ourselves.
// Using ISOLATION_AWARE_ENABLED also causes the manifest resource to be put
// in slot #2 as expected for DLLs. (See wx/msw/wx.rc)

#ifdef ISOLATION_AWARE_ENABLED

static ULONG_PTR wxPySetActivationContext()
{

    OSVERSIONINFO info;
    wxZeroMemory(info);
    info.dwOSVersionInfoSize = sizeof(OSVERSIONINFO);
    GetVersionEx(&info);
    if (info.dwMajorVersion < 5)
        return 0;

    ULONG_PTR cookie = 0;
    HANDLE h;
    ACTCTX actctx;
    TCHAR modulename[MAX_PATH];

    GetModuleFileName(wxGetInstance(), modulename, MAX_PATH);
    wxZeroMemory(actctx);
    actctx.cbSize = sizeof(actctx);
    actctx.lpSource = modulename;
    actctx.lpResourceName = MAKEINTRESOURCE(2);
    actctx.hModule = wxGetInstance();
    actctx.dwFlags = ACTCTX_FLAG_HMODULE_VALID | ACTCTX_FLAG_RESOURCE_NAME_VALID;

    h = CreateActCtx(&actctx);
    if (h == INVALID_HANDLE_VALUE) {
        wxLogLastError(wxT("CreateActCtx"));
        return 0;
    }

    if (! ActivateActCtx(h, &cookie))
        wxLogLastError(wxT("ActivateActCtx"));

    return cookie;
}

static void wxPyClearActivationContext(ULONG_PTR cookie)
{
    if (! DeactivateActCtx(0, cookie))
        wxLogLastError(wxT("DeactivateActCtx"));
}

#endif  // ISOLATION_AWARE_ENABLED

#endif // __WXMSW__

void wxPyPreInit(PyObject* moduleDict)
{
#ifdef ISOLATION_AWARE_ENABLED
    wxPySetActivationContext();
#endif
//#ifdef __WXMSW__
////     wxCrtSetDbgFlag(_CRTDBG_LEAK_CHECK_DF
////                     | _CRTDBG_CHECK_ALWAYS_DF
////                     | _CRTDBG_DELAY_FREE_MEM_DF
////         );
//#endif
//
//#ifdef WXP_WITH_THREAD
//#if wxPyUSE_GIL_STATE
//    PyEval_InitThreads();
//#else
//    PyEval_InitThreads();
//    wxPyTStates = new wxPyThreadStateArray;
//    wxPyTMutex = new wxMutex;
//
//    // Save the current (main) thread state in our array
//    PyThreadState* tstate = wxPyBeginAllowThreads();
//    wxPyEndAllowThreads(tstate);
//#endif
//#endif

    // Ensure that the build options in the DLL (or whatever) match this build
    wxApp::CheckBuildOptions(WX_BUILD_OPTIONS_SIGNATURE, "wxPython");
}

void _wxPyCleanup()
{
    wxEntryCleanup();
}

PyObject* wxAssertionError = NULL;      // Exception object raised for wxASSERT failures

void wxPyCoreModuleInject(PyObject* moduleDict)
{
    // Create an exception object to use for wxASSERTions
    wxAssertionError = PyErr_NewException("wx._core.wxAssertionError",
                                            PyExc_AssertionError, NULL);
    PyDict_SetItemString(moduleDict, "wxAssertionError", wxAssertionError);

    // An alias that should be deprecated sometime
    PyDict_SetItemString(moduleDict, "PyAssertionError", wxAssertionError);


    // Create an exception object to use when the app object hasn't been created yet
    wxPyNoAppError = PyErr_NewException("wx._core.PyNoAppError",
                                        PyExc_RuntimeError, NULL);
    PyDict_SetItemString(moduleDict, "PyNoAppError", wxPyNoAppError);

#ifdef __WXGTK__
#define wxPort "__WXGTK__"
#define wxPortName "wxGTK"
#endif
#ifdef __WXMSW__
#define wxPort "__WXMSW__"
#define wxPortName "wxMSW"
#endif
#ifdef __WXMAC__
#define wxPort "__WXMAC__"
#define wxPortName "wxMac"
#endif

    wxInitAllImageHandlers();

    // TODO: Find some magic way to deprecate wx.Platform such that it raises
    // a warning when used...  Maybe a class that returns wx.Port for any __getattr__?
    PyDict_SetItemString(moduleDict, "Port", PyUnicode_FromString(wxPort));
    PyDict_SetItemString(moduleDict, "Platform", PyUnicode_FromString(wxPort));

    PyDict_SetItemString(moduleDict, "wxWidgets_version", wx2PyString(wxVERSION_STRING));

    PyDict_SetItemString(moduleDict, "_sizeof_int", PyLong_FromLong(sizeof(int)));
    PyDict_SetItemString(moduleDict, "_sizeof_long", PyLong_FromLong(sizeof(long)));
    PyDict_SetItemString(moduleDict, "_sizeof_longlong", PyLong_FromLong(sizeof(long long)));
    PyDict_SetItemString(moduleDict, "_sizeof_double", PyLong_FromLong(sizeof(double)));
    PyDict_SetItemString(moduleDict, "_sizeof_size_t", PyLong_FromLong(sizeof(size_t)));
    PyDict_SetItemString(moduleDict, "_LONG_MIN", PyLong_FromLong(LONG_MIN));
    PyDict_SetItemString(moduleDict, "_LONG_MAX", PyLong_FromLong(LONG_MAX));
    PyDict_SetItemString(moduleDict, "_LLONG_MIN", PyLong_FromLongLong(PY_LLONG_MIN));
    PyDict_SetItemString(moduleDict, "_LLONG_MAX", PyLong_FromLongLong(PY_LLONG_MAX));

    // Make a tuple of strings that gives more info about the platform and build.
    PyObject* PlatformInfo = PyList_New(0);
    PyObject* obj;

#define _AddInfoString(st) \
    obj = PyUnicode_FromString(st); \
    PyList_Append(PlatformInfo, obj); \
    Py_DECREF(obj)

    _AddInfoString(wxPort);
    _AddInfoString(wxPortName);
#if wxUSE_UNICODE
    _AddInfoString("unicode");
#if wxUSE_UNICODE_WCHAR
    _AddInfoString("unicode-wchar");
#else
    _AddInfoString("unicode-utf8");
#endif
#else
    _AddInfoString("ansi");
#endif

#ifdef __WXOSX__
    _AddInfoString("wxOSX");
#endif
#ifdef __WXOSX_CARBON__
    _AddInfoString("wxOSX-carbon");
#endif
#ifdef __WXOSX_COCOA__
    _AddInfoString("wxOSX-cocoa");
#endif
#ifdef __WXGTK__
#ifdef __WXGTK3__
    _AddInfoString("gtk3");
#elif __WXGTK20__
    _AddInfoString("gtk2");
#else
    _AddInfoString("gtk1");
#endif
#endif
#ifdef __WXDEBUG__
    _AddInfoString("wx-assertions-on");
#else
    _AddInfoString("wx-assertions-off");
#endif
    _AddInfoString("phoenix");

    obj = wx2PyString(wxVERSION_STRING);
    PyList_Append(PlatformInfo, obj);
    Py_DECREF(obj);

#if wxUSE_AUTOID_MANAGEMENT
    _AddInfoString("autoidman");
#endif

    wxString sip_version = wxString("sip-") + wxString(SIP_VERSION_STR);
    obj = wx2PyString(sip_version);
    PyList_Append(PlatformInfo, obj);
    Py_DECREF(obj);

#undef _AddInfoString

    PyObject* PlatformInfoTuple = PyList_AsTuple(PlatformInfo);
    Py_DECREF(PlatformInfo);
    PyDict_SetItemString(moduleDict, "PlatformInfo", PlatformInfoTuple);

}
