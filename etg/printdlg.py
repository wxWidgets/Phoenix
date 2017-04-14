#---------------------------------------------------------------------------
# Name:        etg/printdlg.py
# Author:      Robin Dunn
#
# Created:     20-Apr-2012
# Copyright:   (c) 2012-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "printdlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxPrintDialog",
           "wxPageSetupDialog",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # NOTE: They are not really dialog classes, but derive from wx.Object and
    #       just happen to quack like a duck...

    c = module.find('wxPrintDialog')
    assert isinstance(c, etgtools.ClassDef)
    c.find('GetPrintDC').transferBack = True
    c.addPrivateCopyCtor()

    c = module.find('wxPageSetupDialog')
    c.addPrivateCopyCtor()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

