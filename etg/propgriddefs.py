#---------------------------------------------------------------------------
# Name:        etg/propgriddefs.py
# Author:      Robin Dunn
#
# Created:     14-Feb-2017
# Copyright:   (c) 2017-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_propgrid"
NAME      = "propgriddefs"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'propgriddefs_8h.xml',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.find('wxPG_LABEL').ignore()
    module.find('wxPG_LABEL_STRING').ignore()
    module.find('wxPG_NULL_BITMAP').ignore()
    module.find('wxPG_COLOUR_BLACK').ignore()
    module.find('wxPG_COLOUR').ignore()
    module.find('wxPG_DEFAULT_IMAGE_SIZE').ignore()
    module.find('wxPGSortCallback').ignore()

    module.addPyCode(
        code="""\
        PG_LABEL = "@!"
        PG_LABEL_STRING = PG_LABEL
        PG_NULL_BITMAP = wx.NullBitmap
        PG_COLOUR_BLACK = wx.BLACK
        PG_DEFAULT_IMAGE_SIZE = wx.Size(-1, -1)
        """,
        order=15)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

