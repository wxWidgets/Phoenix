#---------------------------------------------------------------------------
# Name:        etg/mousemanager.py
# Author:      Robin Dunn
#
# Created:     28-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "mousemanager"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxMouseEventsManager",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxMouseEventsManager')
    assert isinstance(c, etgtools.ClassDef)

    c.find('MouseHitTest').ignore(False)
    c.find('MouseClicked').ignore(False)
    c.find('MouseDragBegin').ignore(False)
    c.find('MouseDragging').ignore(False)
    c.find('MouseDragEnd').ignore(False)
    c.find('MouseDragCancelled').ignore(False)
    c.find('MouseClickBegin').ignore(False)
    c.find('MouseClickCancelled').ignore(False)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

