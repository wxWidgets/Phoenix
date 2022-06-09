#---------------------------------------------------------------------------
# Name:        etg/filedlgcustomize.py
# Author:      Scott Talbert
#
# Created:     07-Jun-2022
# Copyright:   (c) 2022 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "filedlgcustomize"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxFileDialogButton',
           'wxFileDialogChoice',
           'wxFileDialogCheckBox',
           'wxFileDialogCustomControl',
           'wxFileDialogCustomize',
           'wxFileDialogCustomizeHook',
           'wxFileDialogRadioButton',
           'wxFileDialogStaticText',
           'wxFileDialogTextCtrl',
          ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFileDialogButton')
    assert isinstance(c, etgtools.ClassDef)
    c.noDefCtor = True

    c = module.find('wxFileDialogChoice')
    assert isinstance(c, etgtools.ClassDef)
    c.noDefCtor = True

    c = module.find('wxFileDialogCheckBox')
    assert isinstance(c, etgtools.ClassDef)
    c.noDefCtor = True

    c = module.find('wxFileDialogCustomControl')
    assert isinstance(c, etgtools.ClassDef)
    c.noDefCtor = True

    c = module.find('wxFileDialogCustomize')
    assert isinstance(c, etgtools.ClassDef)
    c.noDefCtor = True

    # Change the AddChoice method to use a wxArrayString instead of a C array
    # and size.
    m = c.find('AddChoice')
    m.find('n').ignore()
    m.find('strings').type = 'const wxArrayString&'
    m.argsString = '(size_t n, const wxArrayString& strings)'
    m.setCppCode("""\
        const wxString* ptr = &strings->front();
        return self->AddChoice(strings->size(), ptr);
        """)

    c = module.find('wxFileDialogCustomizeHook')
    assert isinstance(c, etgtools.ClassDef)

    c = module.find('wxFileDialogRadioButton')
    assert isinstance(c, etgtools.ClassDef)
    c.noDefCtor = True

    c = module.find('wxFileDialogStaticText')
    assert isinstance(c, etgtools.ClassDef)
    c.noDefCtor = True

    c = module.find('wxFileDialogTextCtrl')
    assert isinstance(c, etgtools.ClassDef)
    c.noDefCtor = True


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

