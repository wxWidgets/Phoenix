#---------------------------------------------------------------------------
# Name:        etg/iconbndl.py
# Author:      Robin Dunn
#
# Created:     14-Nov-2011
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "iconbndl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxIconBundle', ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxIconBundle')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()

    # Ignore the overloads that require a WXHINSTANCE
    c.find('wxIconBundle').findOverload('WXHINSTANCE').ignore()
    c.find('AddIcon').findOverload('WXHINSTANCE').ignore()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

