#---------------------------------------------------------------------------
# Name:        etg/htmltag.py
# Author:      Robin Dunn
#
# Created:     29-Oct-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_html"
NAME      = "htmltag"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHtmlTag",

           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING, check4unittest=False)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHtmlTag')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()

    c.find('GetParamAsColour.clr').out = True
    c.find('GetParamAsInt.value').out = True
    c.find('ParseAsColour.clr').out = True

    for m in c.findAll('ScanParam'):
        m.ignore()

    c.find('GetBeginPos').ignore()
    c.find('GetEndPos1').ignore()
    c.find('GetEndPos2').ignore()

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

