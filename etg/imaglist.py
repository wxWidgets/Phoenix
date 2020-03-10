#---------------------------------------------------------------------------
# Name:        etg/imaglist.py
# Author:      Kevin Ollivier
#
# Created:     27-Aug-2011
# Copyright:   (c) 2013 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "imaglist"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  =    [ 'wxImageList',
              ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxImageList')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()
    tools.removeVirtuals(c)
    c.mustHaveApp()

    c.find('GetSize').type = 'void'
    c.find('GetSize.width').out = True
    c.find('GetSize.height').out = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

