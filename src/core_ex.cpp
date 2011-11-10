
void wxPyPreInit(PyObject* moduleDict)
{
//#ifdef ISOLATION_AWARE_ENABLED
//    wxPySetActivationContext();
//#endif
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

    wxInitAllImageHandlers();
}



PyObject* wxPyAssertionError = NULL;

void wxPyCoreModuleInject(PyObject* moduleDict)
{
    // Create an exception object to use for wxASSERTions
    wxPyAssertionError = PyErr_NewException("wx._core.PyAssertionError",
                                            PyExc_AssertionError, NULL);
    PyDict_SetItemString(moduleDict, "PyAssertionError", wxPyAssertionError);

//    // Create an exception object to use when the app object hasn't been created yet
//    wxPyNoAppError = PyErr_NewException("wx._core.PyNoAppError",
//                                        PyExc_RuntimeError, NULL);
//    PyDict_SetItemString(moduleDict, "PyNoAppError", wxPyNoAppError);

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

    PyDict_SetItemString(moduleDict, "Port", PyString_FromString(wxPort));
    PyDict_SetItemString(moduleDict, "Platform", PyString_FromString(wxPort));

    // Make a tuple of strings that gives more info about the platform and build.
    PyObject* PortInfo = PyList_New(0);
    PyObject* obj;

#define _AddInfoString(st) \
    obj = PyString_FromString(st); \
    PyList_Append(PortInfo, obj); \
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
#ifdef __WXGTK20__
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

#undef _AddInfoString

    PyObject* PortInfoTuple = PyList_AsTuple(PortInfo);
    Py_DECREF(PortInfo);
    PyDict_SetItemString(moduleDict, "PortInfo", PortInfoTuple);
}
