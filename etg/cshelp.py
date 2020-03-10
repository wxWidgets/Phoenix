#---------------------------------------------------------------------------
# Name:        etg/cshelp.py
# Author:      Robin Dunn
#
# Created:     06-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "cshelp"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHelpProvider",
           "wxSimpleHelpProvider",
           "wxHelpControllerHelpProvider",
           "wxContextHelp",
           "wxContextHelpButton",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxContextHelpButton')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)


    c = module.find('wxHelpProvider')
    c.abstract = True
    c.find('Set').transferBack = True
    c.find('Set.helpProvider').transfer = True
    c.find('AddHelp.window').type = 'wxWindowBase *'
    c.find('RemoveHelp.window').type = 'wxWindowBase *'
    c.find('ShowHelp.window').type = 'wxWindowBase *'
    c.find('ShowHelpAtPoint.window').type = 'wxWindowBase *'
    c.mustHaveApp()


    c = module.find('wxSimpleHelpProvider')
    c.addItem(etgtools.WigCode("virtual wxString GetHelp(const wxWindowBase* window);"))
    c.mustHaveApp()

    c = module.find('wxHelpControllerHelpProvider')
    c.addPrivateCopyCtor()
    c.mustHaveApp()


    c = module.find('wxContextHelp')
    c.mustHaveApp()

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

