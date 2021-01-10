#---------------------------------------------------------------------------
# Name:        etg/checkbox.py
# Author:      Kevin Ollivier
#
# Created:     6-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "checkbox"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxCheckBox' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxCheckBox')
    assert isinstance(c, etgtools.ClassDef)
    c.find('wxCheckBox.label').default = 'wxEmptyString'
    c.find('Create.label').default = 'wxEmptyString'

    module.addGlobalStr('wxCheckBoxNameStr', c)

    # Workaround warning for the property name starting with a digit
    c.find('Get3StateValue').ignore()
    c.addAutoProperties()
    c.find('Get3StateValue').ignore(False)
    c.addProperty('ThreeStateValue Get3StateValue Set3StateValue')

    tools.fixWindowClass(c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

