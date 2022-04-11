#---------------------------------------------------------------------------
# Name:        etg/cmndata.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     15-Sept-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "cmndata"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxPageSetupDialogData',
           'wxPrintData',
           'wxPrintDialogData',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)

    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPageSetupDialogData')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)

    c.find('GetPrintData').overloads = []

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addProperty('MarginBottomRight', 'GetMarginBottomRight', 'SetMarginBottomRight')
    c.addProperty('MarginTopLeft', 'GetMarginTopLeft', 'SetMarginTopLeft')
    c.addProperty('MinMarginBottomRight', 'GetMinMarginBottomRight', 'SetMinMarginBottomRight')
    c.addProperty('MinMarginTopLeft', 'GetMinMarginTopLeft', 'SetMinMarginTopLeft')
    c.addProperty('PaperId', 'GetPaperId', 'SetPaperId')
    c.addProperty('PaperSize', 'GetPaperSize', 'SetPaperSize')
    c.addProperty('PrintData', 'GetPrintData', 'SetPrintData')



    c = module.find('wxPrintData')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)

    c.addCppMethod('wxSize*', 'GetPaperSize', '()', 'return new wxSize(self->GetPaperSize());')
    c.addCppMethod('void', 'SetPaperSize', '(const wxSize* sz)', 'self->SetPaperSize(*sz);')

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    # TODO: These two methods should use something other than a PyString for
    # holding the data...
    c.addCppMethod('PyObject*', 'GetPrivData', '()', """\
        PyObject* data;
        wxPyThreadBlocker blocker;
        data = PyBytes_FromStringAndSize(self->GetPrivData(),
                                         self->GetPrivDataLen());
        return data;
        """)

    c.addCppMethod('void', 'SetPrivData', '(PyObject* data)', """\
        wxPyThreadBlocker blocker;
        if (! PyBytes_Check(data)) {
            wxPyErr_SetString(PyExc_TypeError, "Expected string object");
            return;
        }

        self->SetPrivData(PyBytes_AS_STRING(data), PyBytes_GET_SIZE(data));
        """)

    c.addAutoProperties()



    c = module.find('wxPrintDialogData')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)
    c.find('SetSetupDialog').ignore()

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addAutoProperties()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()
