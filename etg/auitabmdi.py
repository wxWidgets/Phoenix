#---------------------------------------------------------------------------
# Name:        etg/auitabmdi.py
# Author:      Robin Dunn
#
# Created:     27-Oct-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_aui"
NAME      = "auitabmdi"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxAuiMDIParentFrame',
           'wxAuiMDIChildFrame',
           'wxAuiMDIClientWindow',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxAuiMDIParentFrame')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixTopLevelWindowClass(c)
    c.find('SetMenuBar.menuBar').transfer = True
    c.find('SetArtProvider.provider').transfer = True


    c = module.find('wxAuiMDIChildFrame')
    c.bases = ['wxTDIChildFrame']
    tools.fixTopLevelWindowClass(c)
    tools.fixSetStatusWidths(c.find('SetStatusWidths'))
    c.find('SetMenuBar.menuBar').transfer = True
    c.find('Show').isVirtual = True

    c = module.find('wxAuiMDIClientWindow')
    tools.fixWindowClass(c)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

