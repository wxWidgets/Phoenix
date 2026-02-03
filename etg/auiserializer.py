#---------------------------------------------------------------------------
# Name:        etg/auiserializer.py
# Author:      Scott Talbert
#
# Created:     25-Jan-2026
# Copyright:   (c) 2026 by Scott Talbert
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_aui"
NAME      = "auiserializer"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [
    'wxAuiDeserializer',
    'wxAuiPaneLayoutInfo',
    'wxAuiSerializer',
]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxAuiDeserializer')
    c.find('LoadPanes').ignore()
    c.abstract = True

    c = module.find('wxAuiSerializer')
    c.abstract = True


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

