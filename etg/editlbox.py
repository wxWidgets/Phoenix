#---------------------------------------------------------------------------
# Name:        etg/editlbox.py
# Author:      Robin Dunn
#
# Created:     21-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "editlbox"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxEditableListBox",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxEditableListBox')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    c.find('wxEditableListBox.label').default = 'wxEmptyString'
    c.find('Create.label').default = 'wxEmptyString'

    module.addHeaderCode('#include <wx/editlbox.h>')
    module.addGlobalStr('wxEditableListBoxNameStr', c)

    c.find('GetStrings').ignore()
    c.addCppMethod('wxArrayString*', 'GetStrings', '()',
        doc="Returns a list of the current contents of the control.",
        body="""\
            wxArrayString* arr = new wxArrayString;
            self->GetStrings(*arr);
            return arr;""",
        factory=True)


    # These are not in the documented C++ API. Should they be?
    c.addCppMethod('wxListCtrl*', 'GetListCtrl', '()',
        doc="Returns a reference to the listctrl used in the EditableListBox.",
        body="return self->GetListCtrl();")

    c.addCppMethod('wxBitmapButton*', 'GetDelButton', '()',
        doc="Returns a reference to the delete button used in the EditableListBox.",
        body="return self->GetDelButton();")

    c.addCppMethod('wxBitmapButton*', 'GetNewButton', '()',
        doc="Returns a reference to the new button used in the EditableListBox.",
        body="return self->GetNewButton();")

    c.addCppMethod('wxBitmapButton*', 'GetUpButton', '()',
        doc="Returns a reference to the up button used in the EditableListBox.",
        body="return self->GetUpButton();")

    c.addCppMethod('wxBitmapButton*', 'GetDownButton', '()',
        doc="Returns a reference to the down button used in the EditableListBox.",
        body="return self->GetDownButton();")

    c.addCppMethod('wxBitmapButton*', 'GetEditButton', '()',
        doc="Returns a reference to the edit button used in the EditableListBox.",
        body="return self->GetEditButton();")

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

