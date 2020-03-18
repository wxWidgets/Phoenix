#---------------------------------------------------------------------------
# Name:        etg/timectrl.py
# Author:      Robin Dunn
#
# Created:     06-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "timectrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxTimePickerCtrl",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/timectrl.h>')

    c = module.find('wxTimePickerCtrl')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    module.addGlobalStr('wxTimePickerCtrlNameStr', c, wide=True)


    # ignore the return value and set the parameters to be outputs
    c.find('GetTime').type = 'void'
    c.find('GetTime.hour').out = True
    c.find('GetTime.min').out = True
    c.find('GetTime.sec').out = True


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

