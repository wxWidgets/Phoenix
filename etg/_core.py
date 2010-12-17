#---------------------------------------------------------------------------
# Name:        etg/_core.py
# Author:      Robin Dunn
#
# Created:     8-Nove-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wxPhoenix"   # This is just temporary, rename to 'wx' later.
MODULE    = "_core"
NAME      = "_core"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ ]    
    

# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These items are in their own etg scripts
# for easier maintainability, but their class and function definitions are
# intended to be part of this module, not their own module. This also makes it
# easier to promote one of these to module status later if desired, simply
# remove it from this list of Includes, and change the MODULE value in the
# promoted script to be the same as its NAME.

INCLUDES = [  'defs',
              'wxpy_utils',
              'string',
              'clntdata',
              'windowid',
              'platinfo',
              'display',
              'vidmode',
              'intl',
              
              'gdiobj',
              'font',
              'region',
              
              'gdicmn',
              'geometry',

              'object',
              'colour',
              'tracker',
              'kbdstate',
              'mousestate',
              'tooltip',
              'layout',
              'event',
              
              'evtloop',
              'apptrait',
              'app',
              
              'validate',
              'window',
              'toplevel',
              'frame',
              ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from setup.py for a list of sources and a list
# of additional dependencies when building this extension module
ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
DEPENDS = tools.getNonEtgFiles(INCLUDES)
OTHERDEPS = [ 'src/core_ex.py' ]


#---------------------------------------------------------------------------
 
def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    module.addHeaderCode("""\
    #if defined(__APPLE__)
        // When it's possible that we're building universal binaries with both
        // 32-bit and 64-bit architectures then these need to be undefed because
        // otherwise the values set by configure could conflict with those set
        // based on runtime flags in Python's headers.  We also do something
        // similar in wx/platform.h so it's okay to undef them now because they
        // will be defined again soon.
        #undef SIZEOF_VOID_P
        #undef SIZEOF_LONG
        #undef SIZEOF_SIZE_T

        // Turn off the warning about converting string literals to char*
        // TODO: fix these the right way...
        #pragma GCC diagnostic ignored "-Wwrite-strings"
    #endif
    #ifdef _MSC_VER
        #pragma warning(disable:4800)
        #pragma warning(disable:4190)
    #endif
    
    #include <wx/wx.h>
    """)
    
    module.includePyCode('src/core_ex.py', order=10)
    
    module.addInclude(INCLUDES)
    
    # This code is inserted into the module initialization function
    module.addPostInitializerCode("""
    wxPyCoreModuleInject(sipModuleDict);
    """)
    # Here is the function it calls
    module.addCppCode(wxPyCoreModuleInject)
                      
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    

    
#---------------------------------------------------------------------------

wxPyPreInit = """
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

"""

wxPyCoreModuleInject = """
void wxPyCoreModuleInject(PyObject* moduleDict)
{
//    // Create an exception object to use for wxASSERTions
//    wxPyAssertionError = PyErr_NewException("wx._core.PyAssertionError",
//                                            PyExc_AssertionError, NULL);
//    PyDict_SetItemString(moduleDict, "PyAssertionError", wxPyAssertionError);
//
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

    PyDict_SetItemString(moduleDict, "Port", PyString_FromString(wxPort));

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
#undef _AddInfoString

    PyObject* PortInfoTuple = PyList_AsTuple(PortInfo);
    Py_DECREF(PortInfo);
    PyDict_SetItemString(moduleDict, "PortInfo", PortInfoTuple);
}
"""

if __name__ == '__main__':
    run()
