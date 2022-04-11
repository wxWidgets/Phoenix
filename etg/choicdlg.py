#---------------------------------------------------------------------------
# Name:        etg/choicdlg.py
# Author:      Robin Dunn
#
# Created:     30-Mar-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "choicdlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxMultiChoiceDialog",
           "wxSingleChoiceDialog",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxMultiChoiceDialog')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixTopLevelWindowClass(c)


    c = module.find('wxSingleChoiceDialog')
    tools.fixTopLevelWindowClass(c)

    # Make a new class so we can ignore the clientData parameter in the ctor
    c.addHeaderCode("""\
    class wxPySingleChoiceDialog : public wxSingleChoiceDialog {
    public:
        wxPySingleChoiceDialog(wxWindow* parent,
                               const wxString& message,
                               const wxString& caption,
                               const wxArrayString& choices,
                               long style = wxCHOICEDLG_STYLE,
                               const wxPoint& pos = wxDefaultPosition)
            : wxSingleChoiceDialog(parent, message, caption, choices, (void**)NULL, style, pos)
            {}
    };
    """)

    for item in c.allItems():
        if item.name == 'wxSingleChoiceDialog':
            item.name = 'wxPySingleChoiceDialog'
    c.renameClass('SingleChoiceDialog')

    # ignore this ctor
    c.find('wxPySingleChoiceDialog').findOverload('int n').ignore()

    # and ignore the clientData param in this one
    ctor = c.find('wxPySingleChoiceDialog').findOverload('wxArrayString')
    ctor.find('clientData').ignore()

    c.find('GetSelectionData').ignore()


    # ignore a bunch of the standalone functions
    for f in module.find('wxGetSingleChoiceIndex').all():
        f.ignore()
    for f in module.find('wxGetSingleChoiceData').all():
        f.ignore()
    for f in module.find('wxGetSelectedChoices').all():  # TODO, it might be nice to keep this one
        f.ignore()

    # keep just the overloads of this function that use wxArrayString, and
    # ignore the ones that have "int n"
    for func in module.find('wxGetSingleChoice').all():
        for p in func:
            if p.type == 'int' and p.name == 'n':
                func.ignore()


    for c in module.find('wxGetSingleChoiceIndex').all():
        c.mustHaveApp()

    for c in module.find('wxGetSingleChoice').all():
        c.mustHaveApp()

    for c in module.find('wxGetSingleChoiceData').all():
        c.mustHaveApp()


    #c = module.find('wxGetSingleChoiceIndex')
    #c.mustHaveApp()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

