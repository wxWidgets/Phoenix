#---------------------------------------------------------------------------
# Name:        etg/utils.py
# Author:      Robin Dunn
#
# Created:     19-Dec-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "utils"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'utils_8h.xml',
           'wxWindowDisabler',
           'wxBusyCursor',
           'wxVersionInfo',
           'wxExecuteEnv',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/utils.h>')
    module.addHeaderCode('#include <wx/power.h>')


    c = module.find('wxWindowDisabler')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    c.addPrivateCopyCtor()
    # add context manager methods
    tools.addContextManagerMethods(c, exitBody='pass')


    module.find('wxQsort').ignore()
    module.find('wxGetEmailAddress').findOverload('buf').ignore()
    module.find('wxGetHostName').findOverload('buf').ignore()
    module.find('wxGetUserId').findOverload('buf').ignore()
    module.find('wxGetUserName').findOverload('buf').ignore()
    module.find('wxSortCallback').ignore()

    module.find('wxLoadUserResource').findOverload('pLen').ignore()
    module.find('wxLoadUserResource').findOverload('outData').ignore()

    module.find('wxGetFreeMemory').ignore()
    module.find('wxGetLinuxDistributionInfo').ignore()
    module.find('wxGetDisplayName').ignore()
    module.find('wxSetDisplayName').ignore()

    # TODO: Can this be added back? It was removed because of compiler errors.
    module.find('wxGetDiskSpace').ignore()

    # ignore all the environment related functions
    for item in module.allItems():
        if 'Env' in item.name and item.name != 'wxExecuteEnv':
            item.ignore()
    module.find('wxGetenv').ignore()

    c = module.find('wxExecuteEnv')
    c.find('env').ignore()
    c.addCppMethod('PyObject*', 'GetEnv', '()', isConst=True,
        doc="Returns the environment variables for the new process as a dict.",
        body="""\
            wxPyThreadBlocker blocker;
            PyObject* dict = PyDict_New();
            if (!dict)
                return NULL;
            for (const auto& item : self->env) {
                PyObject* key = wx2PyString(item.first);
                PyObject* value = wx2PyString(item.second);
                int rv = key && value ? PyDict_SetItem(dict, key, value) : -1;
                Py_XDECREF(key);
                Py_XDECREF(value);
                if (rv < 0) {
                    Py_DECREF(dict);
                    return NULL;
                }
            }
            return dict;
            """)
    c.addCppMethod('void', 'SetEnv', '(PyObject* env)',
        doc="""\
            Sets the environment variables for the new process from a mapping
            of str to str, such as a dict. If it is empty the new process
            inherits the environment of this one, otherwise it gets only these
            variables.""",
        body="""\
            wxPyThreadBlocker blocker;
            PyObject* items = PyMapping_Items(env);
            if (!items) {
                PyErr_SetString(PyExc_TypeError,
                                "env must be a mapping of str to str");
                return;
            }
            wxEnvVariableHashMap newEnv;
            for (Py_ssize_t i = 0; i < PyList_GET_SIZE(items); ++i) {
                PyObject* key = PyTuple_GET_ITEM(PyList_GET_ITEM(items, i), 0);
                PyObject* value = PyTuple_GET_ITEM(PyList_GET_ITEM(items, i), 1);
                if (!PyUnicode_Check(key) || !PyUnicode_Check(value)) {
                    PyErr_SetString(PyExc_TypeError,
                                    "environment names and values must be str");
                    Py_DECREF(items);
                    return;
                }
                newEnv[Py2wxString(key)] = Py2wxString(value);
            }
            Py_DECREF(items);
            self->env = newEnv;
            """)
    c.addProperty('env GetEnv SetEnv')

    # Keep just the first wxExecute overload
    f = module.find('wxExecute')
    f.overloads = []
    f.mustHaveApp()

    module.find('wxGetOsVersion.major').out = True
    module.find('wxGetOsVersion.minor').out = True

    c = module.find('wxBusyCursor')
    c.mustHaveApp()
    # add context manager methods
    tools.addContextManagerMethods(c, exitBody='pass')

    f = module.find('wxNewId')
    f.clearDeprecated()
    f.deprecated = """\
IDs generated by this function can possibly conflict with IDs used elsewhere in
the application code. It is recommended to instead use the ``wx.ID_ANY`` ID to
assign generated IDs for the controls, menu items and etc. that you create in the
application. These IDs are guaranteed to not conflict with the other IDs that
are in use in the application. For those cases where you need to create an ID
that can be used more than once then please see :func:`wx.NewIdRef`.""".replace('\n', ' ')

    for funcname in ['wxBell',
                     'wxBeginBusyCursor',
                     'wxEndBusyCursor',
                     'wxShutdown',
                     'wxInfoMessageBox',
                     'wxIsBusy',
                     'wxGetMousePosition',
                     'wxGetKeyState',
                     'wxGetMouseState',
                     ]:
        f = module.find(funcname)
        f.mustHaveApp()

    module.find('wxMSWIsOnSecureScreen').setCppCode("""\
        #ifdef __WINDOWS__
            return wxMSWIsOnSecureScreen();
        #else
            wxPyRaiseNotImplemented();
            return false;
        #endif
        """)



    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

