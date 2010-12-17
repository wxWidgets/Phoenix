
#ifdef __WXGTK__
#include <gdk/gdkx.h>
#include <wx/gtk/private/win_gtk.h>
#endif

#ifdef __WXMAC__
#include <wx/osx/private.h>
#endif


class wxPyApp : public wxApp 
{
    DECLARE_ABSTRACT_CLASS(wxPyApp)

public:
    wxPyApp() : wxApp() {
        m_assertMode = wxPYAPP_ASSERT_EXCEPTION;
        m_startupComplete = false;
        //m_callFilterEvent = false;
        ms_appInstance = this;
    }
    ~wxPyApp() {
        ms_appInstance = NULL;
        wxApp::SetInstance(NULL);
    }

    
#ifndef __WXMAC__
    virtual void MacNewFile() {}
    virtual void MacOpenFile(const wxString &) {}
    virtual void MacOpenURL(const wxString &) {}
    virtual void MacPrintFile(const wxString &) {}
    virtual void MacReopenApp() {}
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
    void SetAssertMode(wxAppAssertMode mode) { m_assertMode = mode; }

//     virtual void OnAssertFailure(const wxChar *file,
//                                  int line,
//                                  const wxChar *func,
//                                  const wxChar *cond,
//                                  const wxChar *msg);

    
    // Implementing OnInit is optional for wxPython apps
    virtual bool OnInit()     { return true; }
    virtual void OnPreInit()  { }
    
    void _BootstrapApp();
    virtual int MainLoop(); 

    static bool IsDisplayAvailable();

    // implementation only
    void SetStartupComplete(bool val) { m_startupComplete = val; } 
    static wxPyApp* ms_appInstance;
    
private:
    wxAppAssertMode m_assertMode;
    bool m_startupComplete;
    //bool m_callFilterEvent;
};

IMPLEMENT_ABSTRACT_CLASS(wxPyApp, wxApp);

wxPyApp* wxPyApp::ms_appInstance = NULL;



void wxPyApp::_BootstrapApp()
{
    static      bool haveInitialized = false;
    bool        result;
    wxPyBlock_t blocked;

    // Only initialize wxWidgets once
    if (! haveInitialized) {
        
        // Copy the values in Python's sys.argv list to a C array of char* to
        // be passed to the wxEntryStart function below.
        int    argc = 0;
        char** argv = NULL;
        blocked = wxPyBeginBlockThreads();
        PyObject* sysargv = PySys_GetObject("argv");
        if (sysargv != NULL) {            
            argc = PyList_Size(sysargv);
            argv = new char*[argc+1];
            int x;
            for(x=0; x<argc; x++) {
                PyObject *pyArg = PyList_GetItem(sysargv, x); // borrowed reference
                // if there isn't anything in sys.argv[0] then set it to the python executable
                if (x == 0 && PyObject_Length(pyArg) < 1) 
                    pyArg = PySys_GetObject("executable");
                argv[x] = strdup(PyString_AsString(pyArg));
            }
            argv[argc] = NULL;
        }
        wxPyEndBlockThreads(blocked);

        
        // Initialize wxWidgets
#ifdef __WXOSX__
        wxMacAutoreleasePool autoreleasePool;
#endif
        result = wxEntryStart(argc, argv);
        // wxApp takes ownership of the argv array, don't delete it here

        blocked = wxPyBeginBlockThreads();
        if (! result)  {
            PyErr_SetString(PyExc_SystemError,
                            "wxEntryStart failed, unable to initialize wxWidgets!"
#ifdef __WXGTK__
                            "  (Is DISPLAY set properly?)"
#endif
                );
            goto error;
        }
        wxPyEndBlockThreads(blocked);
        haveInitialized = true;
    }
    else {
        this->argc = 0;
    }
    
    // It's now ok to generate exceptions for assertion errors.
    SetStartupComplete(true);

    // Call the Python wxApp's OnPreInit and OnInit functions if they exist
    OnPreInit();
    result = OnInit();

    blocked = wxPyBeginBlockThreads();
    if (! result) {
        PyErr_SetString(PyExc_SystemExit, "OnInit returned false, exiting...");
    }
error:
    wxPyEndBlockThreads(blocked);    
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
// can be connected to.  This is accessable from wxPython as a staticmethod of
// wx.App called IsDisplayAvailable().
bool wxPyApp::IsDisplayAvailable()
{
#ifdef __WXGTK__
    Display* display;
    display = XOpenDisplay(NULL);
    if (display == NULL)
        return false;
    XCloseDisplay(display);
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
        // Also foreground the application on the first call as a side-effect.
        if (GetCurrentProcess(&psn) < 0 || SetFrontProcess(&psn) < 0) {
            rv = false;
        } else {
            rv = true;
        }
    }
    return rv;
#endif

#ifdef __WXMSW__
    // TODO...
    return true;
#endif
}



wxPyApp* wxGetApp()
{
    return wxPyApp::ms_appInstance;
}
