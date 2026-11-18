
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

// Is comctl32.dll already redirected to version 6 by the active context or
// the process's own manifest, as for python.exe?
static bool wxPyHaveCommonControls6()
{
    // ACTIVATION_CONTEXT_SECTION_KEYED_DATA_FLAG_FOUND_IN_SYSTEM_DEFAULT, not
    // in the SDK headers. The system default context redirects comctl32.dll
    // to version 5.82, so a match found only there doesn't count.
    const ULONG foundInSystemDefault = 0x00000002;

    ACTCTX_SECTION_KEYED_DATA data;
    wxZeroMemory(data);
    data.cbSize = sizeof(data);
    if (!FindActCtxSectionString(FIND_ACTCTX_SECTION_KEY_RETURN_FLAGS, NULL,
                                 ACTIVATION_CONTEXT_SECTION_DLL_REDIRECTION,
                                 wxT("comctl32.dll"), &data))
        return false;
    return !(data.ulFlags & foundInSystemDefault);
}

static ULONG_PTR wxPySetActivationContext()
{

    OSVERSIONINFO info;
    wxZeroMemory(info);
    info.dwOSVersionInfoSize = sizeof(OSVERSIONINFO);
    GetVersionEx(&info);
    if (info.dwMajorVersion < 5)
        return 0;

    // Our context is never deactivated, so it would stay on top of a host
    // application's own one and make the host's DeactivateActCtx fail
    if (wxPyHaveCommonControls6())
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

#include <wx/calctrl.h>
#include <wx/collpane.h>
#include <wx/filectrl.h>
#include <wx/tracker.h>

#include <unordered_map>

// Find the SIP type for the most derived wrapped class of an object, from its
// wxRTTI info. Some ports #define a public class to a port-specific one
// (wxCalendarCtrl is wxGtkCalendarCtrl in wxGTK), whose name SIP doesn't
// know, so those are looked up by the public name.
static const sipTypeDef* wxPyFindSubClassType(const wxClassInfo* info)
{
    static const struct {
        const char* rttiName;
        const char* sipName;
    } aliases[] = {
        { wxSTRINGIZE(wxCalendarCtrl), "wxCalendarCtrl" },
        { wxSTRINGIZE(wxCollapsiblePane), "wxCollapsiblePane" },
        { wxSTRINGIZE(wxFileCtrl), "wxFileCtrl" },
    };

    for ( ; info; info = info->GetBaseClass1() ) {
        wxString name = info->GetClassName();
        for (const auto& alias : aliases) {
            if (name == alias.rttiName) {
                name = alias.sipName;
                break;
            }
        }
        const sipTypeDef* type = sipFindType(name.c_str());
        if (type)
            return type;
    }
    return NULL;
}

// SIP is told when an object created from Python is deleted, but not when
// one created by C++ code (by XRC, for example) is. Its wrapper would then
// stay in SIP's object map, and be handed out again, with the old type, for
// a new object at the same address. Event handlers are trackable, so tell
// SIP when they go away.
class wxPyWrapperTracker;
static std::unordered_map<sipSimpleWrapper*, wxPyWrapperTracker*> wxPyWrapperTrackers;

class wxPyWrapperTracker : public wxTrackerNode
{
public:
    wxPyWrapperTracker(wxEvtHandler* handler, sipSimpleWrapper* wrapper)
        : m_handler(handler), m_wrapper(wrapper) { }

    void OnObjectDestroy() override
    {
        // The handler may outlive Python
        if (Py_IsInitialized() || PyGILState_GetThisThreadState() != NULL) {
            wxPyThreadBlocker blocker;
            wxPyWrapperTrackers.erase(m_wrapper);
            sipInstanceDestroyedEx(&m_wrapper);
        }
        delete this;
    }

    wxEvtHandler* m_handler;
    sipSimpleWrapper* m_wrapper;
};

static void wxPyTrackWrappedEvtHandler(void* cpp)
{
    sipSimpleWrapper* wrapper = (sipSimpleWrapper*)sipGetPyObject(cpp, sipType_wxEvtHandler);
    if (!wrapper || wxPyWrapperTrackers.count(wrapper))
        return;
    wxEvtHandler* handler = (wxEvtHandler*)sipGetCppPtr(wrapper, sipType_wxEvtHandler);
    if (!handler)
        return;
    wxPyWrapperTracker* tracker = new wxPyWrapperTracker(handler, wrapper);
    handler->AddNode(tracker);
    wxPyWrapperTrackers[wrapper] = tracker;
}

static void wxPyUntrackWrapper(sipSimpleWrapper* wrapper)
{
    auto it = wxPyWrapperTrackers.find(wrapper);
    if (it == wxPyWrapperTrackers.end())
        return;
    wxPyWrapperTracker* tracker = it->second;
    wxPyWrapperTrackers.erase(it);
    tracker->m_handler->RemoveNode(tracker);
    delete tracker;
}

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

    sipRegisterEventHandler(sipEventWrappedInstance, sipType_wxEvtHandler,
                            (void*)wxPyTrackWrappedEvtHandler);
    sipRegisterEventHandler(sipEventCollectingWrapper, sipType_wxEvtHandler,
                            (void*)wxPyUntrackWrapper);
}
