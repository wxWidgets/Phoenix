#---------------------------------------------------------------------------
# Name:        etg/filehistory.py
# Author:      Robin Dunn
#
# Created:     16-Jul-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "filehistory"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxFileHistory",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFileHistory')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()

    # There is already a wxMenuList class so we have to name this one something else.
    module.addItem(
        tools.wxListWrapperTemplate('wxList', 'wxMenu', module,
                                    fakeListClassName='wxFileHistoryMenuList'))
    c.find('GetMenus').type = 'const wxFileHistoryMenuList&'
    c.find('GetMenus').noCopy = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

