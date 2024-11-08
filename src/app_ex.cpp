
#ifdef __WXGTK__
#include <gtk/gtk.h>
#endif

#ifdef __WXMAC__
#include <wx/osx/private.h>
#endif

#ifdef __WXMSW__
#include <wx/msw/private.h>
#include <wx/msw/winundef.h>
#include <wx/msw/msvcrt.h>
#endif


#ifdef __WXMSW__             // If building for Windows...

//----------------------------------------------------------------------
// This gets run when the DLL is loaded.  We just need to save the
// instance handle.
//----------------------------------------------------------------------

extern "C"
BOOL WINAPI DllMain(
    HINSTANCE   hinstDLL,    // handle to DLL module
    DWORD       fdwReason,   // reason for calling function
    LPVOID      lpvReserved  // reserved
   )
{
    // If wxPython is embedded in another wxWidgets app then
    // the instance has already been set.
    if (! wxGetInstance())
        wxSetInstance(hinstDLL);

    return TRUE;
}
#endif  // __WXMSW__

//----------------------------------------------------------------------
// Classes for implementing the wxp main application shell.
//----------------------------------------------------------------------


class wxPyApp : public wxApp
{
    DECLARE_ABSTRACT_CLASS(wxPyApp)

public:
    wxPyApp() : wxApp() {
        m_assertMode = wxAPP_ASSERT_EXCEPTION;
        m_startupComplete = false;
        //m_callFilterEvent = false;
        wxApp::SetInstance(this);
    }

    ~wxPyApp() {
        wxApp::SetInstance(NULL);
    }


#ifndef __WXMAC__
    virtual void MacNewFile() {}
    virtual void MacOpenFile(const wxString &) {}
    virtual void MacOpenFiles(const wxArrayString& fileNames) {}
    virtual void MacOpenURL(const wxString &) {}
    virtual void MacPrintFile(const wxString &) {}
    virtual void MacReopenApp() {}
    virtual bool OSXIsGUIApplication() { return true; }
    void OSXEnableAutomaticTabbing(bool) {}
#endif

#ifdef __WXMAC__
    static long GetMacAboutMenuItemId()               { return s_macAboutMenuItemId; }
    static long GetMacPreferencesMenuItemId()         { return s_macPreferencesMenuItemId; }
    static long GetMacExitMenuItemId()                { return s_macExitMenuItemId; }
    static wxString GetMacHelpMenuTitleName()         { return s_macHelpMenuTitleName; }
    static void SetMacAboutMenuItemId(long val)       { s_macAboutMenuItemId = val; }
    static void SetMacPreferencesMenuItemId(long val) { s_macPreferencesMenuItemId = val; }
    static void SetMacExitMenuItemId(long val)        { s_macExitMenuItemId = val; }
    static void SetMacHelpMenuTitleName(const wxString& val) { s_macHelpMenuTitleName = val; }
#else
    static long GetMacAboutMenuItemId()               { return 0; }
    static long GetMacPreferencesMenuItemId()         { return 0; }
    static long GetMacExitMenuItemId()                { return 0; }
    static wxString GetMacHelpMenuTitleName()         { return wxEmptyString; }
    static void SetMacAboutMenuItemId(long)           { }
    static void SetMacPreferencesMenuItemId(long)     { }
    static void SetMacExitMenuItemId(long)            { }
    static void SetMacHelpMenuTitleName(const wxString&) { }
#endif

    wxAppAssertMode  GetAssertMode() { return m_assertMode; }
    void SetAssertMode(wxAppAssertMode mode) {
        m_assertMode = mode;
        if (mode & wxAPP_ASSERT_SUPPRESS)
            wxDisableAsserts();
        else
            wxSetDefaultAssertHandler();
    }

    virtual void OnAssertFailure(const wxChar *file,
                                 int line,
                                 const wxChar *func,
                                 const wxChar *cond,
                                 const wxChar *msg);


    // Implementing OnInit is optional for wxPython apps
    virtual bool OnInit()     { return true; }
    virtual void OnPreInit()  { }

    void _BootstrapApp();
    virtual int MainLoop();

    static bool IsDisplayAvailable();

    // implementation only
    void SetStartupComplete(bool val) { m_startupComplete = val; }

private:
    wxAppAssertMode m_assertMode;
    bool m_startupComplete;
    //bool m_callFilterEvent;
};

IMPLEMENT_ABSTRACT_CLASS(wxPyApp, wxApp);

extern PyObject* wxAssertionError;         // Exception object raised for wxASSERT failures


void wxPyApp::OnAssertFailure(const wxChar *file,
                              int line,
                              const wxChar *func,
                              const wxChar *cond,
                              const wxChar *msg)
{
    // ignore it?
    if (m_assertMode & wxAPP_ASSERT_SUPPRESS)
        return;

    // turn it into a Python exception?
    if (m_assertMode & wxAPP_ASSERT_EXCEPTION) {
        wxString buf;
        buf.Alloc(4096);
        buf.Printf(wxT("C++ assertion \"%s\" failed at %s(%d)"), cond, file, line);
        if ( func && *func )
            buf << wxT(" in ") << func << wxT("()");
        if (msg != NULL)
            buf << wxT(": ") << msg;

        // set the exception
        wxPyThreadBlocker blocker;
        PyObject* s = wx2PyString(buf);
        PyErr_SetObject(wxAssertionError, s);
        Py_DECREF(s);

        // Now when control returns to whatever API wrapper was called from
        // Python it should detect that an exception is set and will return
        // NULL, signalling the exception to Python.
    }

    // Send it to the normal log destination, but only if
    // not _DIALOG because it will call this too
    if ( (m_assertMode & wxAPP_ASSERT_LOG) && !(m_assertMode & wxAPP_ASSERT_DIALOG)) {
        wxString buf;
        buf.Alloc(4096);
        buf.Printf(wxT("%s(%d): assert \"%s\" failed"),
                   file, line, cond);
        if ( func && *func )
            buf << wxT(" in ") << func << wxT("()");
        if (msg != NULL)
            buf << wxT(": ") << msg;
        wxLogDebug(buf);
    }

    // do the normal wx assert dialog?
    if (m_assertMode & wxAPP_ASSERT_DIALOG)
        wxApp::OnAssertFailure(file, line, func, cond, msg);
}


void wxPyApp::_BootstrapApp()
{
    static      bool haveInitialized = false;
    bool        result;

    // Only initialize wxWidgets once
    if (! haveInitialized) {

        // Copy the values in Python's sys.argv list to a C array of char* to
        // be passed to the wxEntryStart function below.
        #if PY_MAJOR_VERSION >= 3
            #define argType   wchar_t
        #else
            #define argType   char
        #endif
        int       argc = 0;
        argType** argv = NULL;
        {
            wxPyThreadBlocker blocker;
            PyObject* sysargv = PySys_GetObject("argv");
            if (sysargv != NULL) {
                argc = PyList_Size(sysargv);
                argv = new argType*[argc+1];
                int x;
                for(x=0; x<argc; x++) {
                    PyObject *pyArg = PyList_GetItem(sysargv, x); // borrowed reference
                    // if there isn't anything in sys.argv[0] then set it to the python executable
                    if (x == 0 && PyObject_Length(pyArg) < 1)
                        pyArg = PySys_GetObject("executable");
                    #if PY_MAJOR_VERSION >= 3
                        int len = PyObject_Length(pyArg);
                        argv[x] = new argType[len+1];
                        wxPyUnicode_AsWideChar(pyArg, argv[x], len+1);
                    #else
                        argv[x] = strdup(PyBytes_AsString(pyArg));
                    #endif
                }
                argv[argc] = NULL;
            }
        }

        // Initialize wxWidgets
#ifdef __WXOSX__
        wxMacAutoreleasePool autoreleasePool;
#endif
        result = wxEntryStart(argc, argv);
        // wxApp takes ownership of the argv array, don't delete it here

        if (! result)  {
            wxPyThreadBlocker blocker;
            PyErr_SetString(PyExc_SystemError,
                              "wxEntryStart failed, unable to initialize wxWidgets!"
#ifdef __WXGTK__
                              "  (Is DISPLAY set properly?)"
#endif
                );
            goto error;
        }
    }
    else {
        this->argc = 0;
    }

    // It's now ok to generate exceptions for assertion errors.
    SetStartupComplete(true);

    // Call the Python wxApp's OnPreInit and OnInit functions if they exist
    OnPreInit();

    // Only use CallOnInit the first time, otherwise it will block on [NSApp run] in wxOSX_Cocoa;
    if (! haveInitialized)
        result = CallOnInit();
    else
        result = OnInit();

//#ifdef __WXOSX_COCOA__
//    OSXSetInitWasCalled(true);  TODO: consider adding this method to wxApp
//#endif

    if (! result) {
        wxPyErr_SetString(PyExc_SystemExit, "OnInit returned false, exiting...");
    }

    haveInitialized = true;

error:
    return;
}


int wxPyApp::MainLoop()
{
    int retval = 0;

    {
#ifdef __WXOSX__
        wxMacAutoreleasePool autoreleasePool;
#endif
        DeletePendingObjects();
    }
    bool initialized = wxTopLevelWindows.GetCount() != 0;
    if (initialized) {
        if ( m_exitOnFrameDelete == Later ) {
            m_exitOnFrameDelete = Yes;
        }

        retval = wxApp::MainLoop();
        OnExit();
    }
    return retval;
}


// Function to test if the Display (or whatever is the platform equivallent)
// can be connected to.
bool wxPyApp::IsDisplayAvailable()
{
#ifdef __WXGTK__
    GdkDisplay* display;
    display = gdk_display_open(NULL);
    if (display == NULL)
        return false;
    gdk_display_close(display);
    return true;
#endif

#ifdef __WXMAC__
    // This is adapted from Python's Mac/Modules/MacOS.c in the
    // MacOS_WMAvailable function.
    bool rv;
    ProcessSerialNumber psn;

    /*
    ** This is a fairly innocuous call to make if we don't have a window
    ** manager, or if we have no permission to talk to it. It will print
    ** a message on stderr, but at least it won't abort the process.
    ** It appears the function caches the result itself, and it's cheap, so
    ** no need for us to cache.
    */
#ifdef kCGNullDirectDisplay
    /* On 10.1 CGMainDisplayID() isn't available, and
    ** kCGNullDirectDisplay isn't defined.
    */
    if (CGMainDisplayID() == 0) {
        rv = false;
    } else
#endif
    {
        // Assume all is well... Until something better is found again.
        rv = true;
    }
    return rv;
#endif

#ifdef __WXMSW__
    // TODO...
    return true;
#endif
}



wxAppConsole* wxGetApp()
{
    return wxApp::GetInstance();
}
