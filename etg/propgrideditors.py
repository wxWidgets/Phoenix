#---------------------------------------------------------------------------
# Name:        etg/propgrideditors.py
# Author:      Robin Dunn
#
# Created:     23-Feb-2015
# Copyright:   (c) 2015-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "propgrideditors"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxPGWindowList',
           'wxPGEditor',
           'wxPGTextCtrlEditor',
           'wxPGChoiceEditor',
           'wxPGComboBoxEditor',
           'wxPGChoiceAndButtonEditor',
           'wxPGTextCtrlAndButtonEditor',
           'wxPGCheckBoxEditor',
           'wxPGEditorDialogAdapter',
           'wxPGMultiButton',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxPGEditor')
    assert isinstance(c, etgtools.ClassDef)

    # Change the method to return the value instead of passing it
    # through a parameter for modification.
    m = c.find('GetValueFromControl')
    m.find('variant').out = True

    # Change the virtual method handler code for GetValueFromControl to follow
    # the same pattern as the tweaked public API, namely that the value is the
    # return value instead of an out parameter.
    m.cppSignature = 'bool (wxVariant& variant, wxPGProperty* property, wxWindow* ctrl)'
    m.virtualCatcherCode = """\
        PyObject *sipResObj = sipCallMethod(&sipIsErr, sipMethod, "DD",
                                            property, sipType_wxPGProperty, NULL,
                                            ctrl, sipType_wxWindow, NULL);
        if (sipResObj == NULL) {
            if (PyErr_Occurred())
                PyErr_Print();
            sipRes = false;
        }
        else if (sipResObj == Py_None) {
            sipRes = false;
        } else if (sipResObj && !sipIsErr) {
            sipParseResult(&sipIsErr, sipMethod, sipResObj, "(bH5)", &sipRes, sipType_wxPGVariant, &variant);
        }
        """


    c = module.find('wxPGMultiButton')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    c.addPyMethod('AddButton', '(self, label, id=-2)',
        doc='A simple wrapper around the PGMultiButton.Add method, for backwards compatibility.',
        body="self.Add(label, id)")

    c.addPyMethod('AddBitmapButton', '(self, bitmap, id=-2)',
        doc='A simple wrapper around the PGMultiButton.Add method, for backwards compatibility.',
        body="self.Add(bitmap, id)")

    # Switch all wxVariant types to wxPGVariant, so the propgrid-specific
    # version of the MappedType will be used for converting to/from Python
    # objects.
    for item in module.allItems():
        if hasattr(item, 'type') and 'wxVariant' in item.type:
            item.type = item.type.replace('wxVariant', 'wxPGVariant')

    # wxPGWindowList doesn't expect to own these, but wxPropertyGrid does,
    # so flag them as transferred to the C++ side.
    c = module.find('wxPGWindowList')
    c.find('wxPGWindowList.primary').transfer = True
    c.find('wxPGWindowList.secondary').transfer = True
    c.find('SetSecondary.secondary').transfer = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

