#---------------------------------------------------------------------------
# Name:        etg/bannerwindow.py
# Author:      Robin Dunn
#
# Created:     21-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "bannerwindow"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxBannerWindow",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxBannerWindow')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    module.addHeaderCode('#include <wx/bannerwindow.h>')
    module.addGlobalStr('wxBannerWindowNameStr', c)

    # We can already do with keyword args what this ctor does for C++ people,
    # so ignore it to avoid signature conflicts.
    c.find('wxBannerWindow').findOverload('parent, wxDirection').ignore()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

