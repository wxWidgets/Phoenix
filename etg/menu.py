#---------------------------------------------------------------------------
# Name:        etg/menu.py
# Author:      Kevin Ollivier
#
# Created:     25-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "menu"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxMenu', 'wxMenuBar' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxMenu')
    assert isinstance(c, etgtools.ClassDef)
    c.find('GetMenuItems').overloads[0].ignore()
    tools.removeVirtuals(c)

    c = module.find('wxMenuBar')
    assert isinstance(c, etgtools.ClassDef)
    c.find('wxMenuBar').findOverload('(size_t n, wxMenu *menus[], const wxString titles[], long style=0)').ignore()
    c.find('FindItem.menu').out = True
    tools.removeVirtuals(c)

    module.addItem(tools.wxListWrapperTemplate('wxMenuList', 'wxMenu'))

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

