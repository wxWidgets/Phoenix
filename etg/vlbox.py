#---------------------------------------------------------------------------
# Name:        etg/vlbox.py
# Author:      Robin Dunn
#
# Created:     14-Aug-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "vlbox"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxVListBox",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxVListBox')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    module.addHeaderCode('#include <wx/vlbox.h>')
    module.addGlobalStr('wxVListBoxNameStr', c)

    c.find('GetFirstSelected.cookie').out = True
    c.find('GetNextSelected.cookie').inOut = True

    for name in ['OnDrawItem', 'OnDrawBackground', 'OnDrawSeparator', 'OnMeasureItem']:
        c.find(name).ignore(False)
        c.find(name).isVirtual = True

    c.find('OnDrawItem').isPureVirtual = True
    c.find('OnMeasureItem').isPureVirtual = True

    c.find('SelectRange.from').name = 'from_'
    c.find('SelectRange.to').name = 'to_'


    # Let the wrapper generator know that there is an implementation for this
    # pure virtual inherited from the base class.
    c.addItem(etgtools.WigCode("virtual wxCoord OnGetRowHeight(size_t n) const;",
                               protection='protected'))

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

