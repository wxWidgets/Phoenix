#---------------------------------------------------------------------------
# Name:        etg/htmlpars.py
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
NAME      = "htmlpars"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHtmlTagHandler",
           "wxHtmlParser",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHtmlTagHandler')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.find('ParseInner').ignore(False)
    c.find('ParseInnerSource').ignore(False)


    c = module.find('wxHtmlParser')
    c.addPrivateCopyCtor()
    c.abstract = True
    c.find('AddTag').ignore(False)
    c.find('AddWord').ignore()
    c.find('DoParsing').findOverload('const_iterator').ignore()



    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

