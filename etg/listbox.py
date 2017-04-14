#---------------------------------------------------------------------------
# Name:        etg/listbox.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "listbox"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxListBox' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxListBox')
    c.find('wxListBox').findOverload('wxString choices').ignore()
    c.find('wxListBox').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'

    c.find('Create').findOverload('wxString choices').ignore()
    c.find('Create').findOverload('wxArrayString').find('choices').default = 'wxArrayString()'

    # Just use the Set() method inherited from wxControlWithItems, it has the
    # overload defined that works best for us
    for set in c.findAll('Set'):
        set.ignore()

    c.find('GetSelections').type = 'wxArrayInt*'
    c.find('GetSelections').factory = True  # a new instance is being created
    c.find('GetSelections.selections').ignore()
    c.find('GetSelections').setCppCode("""\
        wxArrayInt* array = new wxArrayInt;
        self->GetSelections(*array);
        return array;
        """)

    c.find('InsertItems').findOverload('wxString *items').ignore()

    tools.fixWindowClass(c)

    module.addGlobalStr('wxListBoxNameStr', c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

