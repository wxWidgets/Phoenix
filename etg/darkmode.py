#---------------------------------------------------------------------------
# Name:        etg/darkmode.py
# Author:      Scott Talbert
#
# Created:     25-Jan-2026
# Copyright:   (c) 2026 by Scott Talbert
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "darkmode"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [
    'wxDarkModeSettings',
]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxDarkModeSettings')
    assert isinstance(c, etgtools.ClassDef)
    ###c.find('GetMenuColour').ignore()
    c.addPrivateCopyCtor()

    # wxDarkModeSettings only exists on MSW
    import sys
    if not sys.platform.startswith('win'):
        c.ignore()
        module.find('wxMenuColour').ignore()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

