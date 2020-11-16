#---------------------------------------------------------------------------
# Name:        etg/datectrl.py
# Author:      Robin Dunn
#
# Created:     09-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools


PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "datectrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxDatePickerCtrl",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/datectrl.h>")

    dpc = module.find('wxDatePickerCtrl')
    assert isinstance(dpc, etgtools.ClassDef)

    # Make a copy and call it wxDatePickerCtrlGeneric so we can generate
    # wrappers for both classes
    gdpc = tools.copyClassDef(dpc, 'wxDatePickerCtrlGeneric')
    assert isinstance(gdpc, etgtools.ClassDef)
    module.insertItemAfter(dpc, gdpc)
    # and give it an alias matching the class name in Classic
    module.addPyCode("GenericDatePickerCtrl = DatePickerCtrlGeneric")

    # now back to our regular tweaking
    for c in [dpc, gdpc]:
        tools.fixWindowClass(c)
        c.find('GetRange.dt1').out = True
        c.find('GetRange.dt2').out = True

    gdpc.addHeaderCode("#include <wx/generic/datectrl.h>")

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

