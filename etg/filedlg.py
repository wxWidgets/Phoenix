#---------------------------------------------------------------------------
# Name:        etg/filedlg.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2018 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "filedlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxFileDialog' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFileDialog')
    isinstance(c, etgtools.ClassDef)
    module.addGlobalStr('wxFileDialogNameStr', c)
    module.find('wxFileSelectorDefaultWildcardStr').ignore()

    c.find('ExtraControlCreatorFunction').ignore()

    c.find('SetExtraControlCreator').ignore()
    c.addHeaderCode("""\
        wxWindow* _callPythonExtraControlCreator(wxWindow* w)
        {
            wxPyThreadBlocker blocker;
            wxWindow* cw = NULL;
            PyObject* pyw = sipGetPyObject(w, sipType_wxWindow);
            PyObject* ccf = PyObject_GetAttrString(pyw, "_wxExtraControlCreatorFunction");
            if (ccf == NULL)
                PyErr_SetString(PyExc_RuntimeError,
                                            "extra control creator function disappeared");
            else {
                PyObject* pycw = PyObject_CallFunction(ccf, "O", pyw);
                if (pycw != NULL && pycw != Py_None) {
                    if (!sipCanConvertToType(pycw, sipType_wxWindow, SIP_NOT_NONE))
                        PyErr_Format(PyExc_ValueError,
                                            "control creator did not return wxWindow: %R", pycw);
                    else {
                        int iserr = 0;
                        cw = (wxWindow*) sipConvertToType(pycw, sipType_wxWindow, NULL,
                                                            SIP_NOT_NONE, NULL, &iserr);
                        if (iserr) {
                            PyErr_Format(PyExc_ValueError,
                                            "conversion failure for control creator "
                                            "return value: %R", pycw);
                            cw = NULL;
                        }
                    }
                }
            }
            return cw;
        }
        """)
    c.addCppMethod('bool', 'SetExtraControlCreator', '(PyObject* ccf)',
        doc="""\
        Set extra control creator function to be called during dialog creation""",
        body="""\
        bool status = true;
        {
        wxPyThreadBlocker blocker;
        PyObject* pySelf = sipGetPyObject(self, sipType_wxWindow);
        if (pySelf == NULL) {
            PyErr_SetString(PyExc_ValueError, "expecting wxWindow object");
            status = false;
        }
        else if (!PyCallable_Check(ccf)) {
            PyErr_SetString(PyExc_ValueError, "expecting function or callable object");
            status = false;
        }
        else if (PyObject_SetAttrString(pySelf, "_wxExtraControlCreatorFunction", ccf) < 0)
            status = false;
        self->SetExtraControlCreator(_callPythonExtraControlCreator);
        }
        return status;
        """)

    c.find('GetFilenames').ignore()
    c.addCppMethod('wxArrayString*', 'GetFilenames', '()', doc="""\
        Returns a list of filenames chosen in the dialog.  This function
        should only be used with the dialogs which have wx.MULTIPLE style,
        use GetFilename for the others.""",
        body="""\
        wxArrayString* arr = new wxArrayString;
        self->GetFilenames(*arr);
        return arr;""",
        factory=True)

    c.find('GetPaths').ignore()
    c.addCppMethod('wxArrayString*', 'GetPaths', '()', doc="""\
        Returns a list of the full paths of the files chosen. This function
        should only be used with the dialogs which have wx.MULTIPLE style, use
        GetPath for the others.
        """,
        body="""\
        wxArrayString* arr = new wxArrayString;
        self->GetPaths(*arr);
        return arr;""",
        factory=True)


    tools.fixTopLevelWindowClass(c)


    for funcname in ['wxFileSelector',
                     'wxFileSelectorEx',
                     'wxLoadFileSelector',
                     'wxSaveFileSelector',
                     ]:
        c = module.find(funcname)
        c.mustHaveApp()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

