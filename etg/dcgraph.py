#---------------------------------------------------------------------------
# Name:        etg/dcgraph.py
# Author:      Robin Dunn
#
# Created:     2-Sept-2011
# Copyright:   (c) 2011-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "dcgraph"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxGCDC' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxGCDC')
    c.mustHaveApp()
    # FIXME: Do we handle platform-specific classes, and if so, how?
    c.find('wxGCDC').findOverload('wxEnhMetaFileDC').ignore()
    c.addPrivateCopyCtor()

    c.find('wxGCDC.windowDC').keepReference = True
    c.find('wxGCDC.memoryDC').keepReference = True
    c.find('wxGCDC.printerDC').keepReference = True

    c.find('wxGCDC.context').transfer = True
    c.find('SetGraphicsContext.ctx').transfer = True


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

