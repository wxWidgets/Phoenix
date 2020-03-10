#---------------------------------------------------------------------------
# Name:        etg/richtextprint.py
# Author:      Robin Dunn
#
# Created:     14-May-2013
# Copyright:   (c) 2013-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_richtext"
NAME      = "richtextprint"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxRichTextHeaderFooterData",
           "wxRichTextPrintout",
           "wxRichTextPrinting",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxRichTextHeaderFooterData')
    assert isinstance(c, etgtools.ClassDef)
    tools.ignoreAllOperators(c)


    c = module.find('wxRichTextPrintout')
    assert isinstance(c, etgtools.ClassDef)
    c.find('GetPageInfo.minPage').out = True
    c.find('GetPageInfo.maxPage').out = True
    c.find('GetPageInfo.selPageFrom').out = True
    c.find('GetPageInfo.selPageTo').out = True


    c = module.find('wxRichTextPrinting')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

