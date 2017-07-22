#---------------------------------------------------------------------------
# Name:        etg/metafile.py
# Author:      Robin Dunn
#              Dietmar Schwertberger
#
# Created:     01-Nov-2015
# Copyright:   (c) 2015-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_msw"
NAME      = "metafile"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxMetafile',
           'wxMetafileDC',
           ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxMetafile')
    c.addPrivateCopyCtor()

    c = module.find('wxMetafileDC')
    c.addPrivateCopyCtor()

    module.find("wxMakeMetafilePlaceable").ignore()

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()
