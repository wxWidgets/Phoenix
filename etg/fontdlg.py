#---------------------------------------------------------------------------
# Name:        etg/fontdlg.py
# Author:      Robin Dunn
#
# Created:     19-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "fontdlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxFontData",
           "wxFontDialog",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/fontdlg.h>')

    c = module.find('wxFontDialog')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixTopLevelWindowClass(c)

    # there are two of these, ignore one of them
    c.find('GetFontData').ignore()


    c = module.find('wxGetFontFromUser')
    c.mustHaveApp()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

