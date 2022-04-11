#---------------------------------------------------------------------------
# Name:        etg/access.py
# Author:      Robin Dunn
#
# Created:     08-Oct-2018
# Copyright:   (c) 2018-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "access"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxAccessible',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/access.h>')

    tools.generateStubs('wxUSE_ACCESSIBILITY', module,
                        typeValMap={'wxAccStatus':'wxACC_NOT_IMPLEMENTED'})

    c = module.find('wxAccessible')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()

    c.find('GetChild.child').out = True
    c.find('GetChildCount.childCount').out = True
    c.find('GetDefaultAction.actionName').out = True
    c.find('GetDescription.description').out = True
    c.find('GetFocus.child').out = True
    c.find('GetHelpText.helpText').out = True
    c.find('GetKeyboardShortcut.shortcut').out = True
    c.find('GetName.name').out = True
    c.find('GetParent.parent').out = True
    c.find('GetRole.role').out = True
    c.find('GetSelections.selections').out = True
    c.find('GetState.state').out = True
    c.find('GetValue.strValue').out = True

    #TODO: double-check this one
    c.find('GetLocation.rect').out = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

