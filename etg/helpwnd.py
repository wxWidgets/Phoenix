#---------------------------------------------------------------------------
# Name:        etg/helpwnd.py
# Author:      Robin Dunn
#
# Created:     30-Oct-2012
# Copyright:   (c) 2012-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_html"
NAME      = "helpwnd"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHtmlHelpWindow",

           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHtmlHelpWindow')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    c.find('SetController.controller').transfer = True

    c.find('CreateSearch').ignore(False)
    c.find('AddToolbarButtons').ignore(False)
    c.find('CreateContents').ignore(False)
    c.find('CreateIndex').ignore(False)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

