#---------------------------------------------------------------------------
# Name:        etg/tipwin.py
# Author:      Robin Dunn
#
# Created:     15-Dec-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "tipwin"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxTipWindow",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxTipWindow')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    # We're not going to allow the use of the windowPtr arg in the ctor
    c.find('wxTipWindow.windowPtr').ignore()

    # TODO: find a way to include the rectBounds parameter while still ignoring windowPtr
    c.find('wxTipWindow.rectBounds').ignore()

    # ignore this method too
    c.find('SetTipWindowPtr').ignore()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

