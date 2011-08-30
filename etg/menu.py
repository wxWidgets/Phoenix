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
ITEMS  = [ 'wxMenu', 'wxMenuBar', 'wxMenuItem' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxMenu')
    c.find('GetMenuItems').ignore()
    assert isinstance(c, etgtools.ClassDef)

    c = module.find('wxMenuBar')
    c.find('wxMenuBar').findOverload('(size_t n, wxMenu *menus[], const wxString titles[], long style=0)').ignore()
    c.find('FindItem').ignore()
    assert isinstance(c, etgtools.ClassDef)

    c = module.find('wxMenuItem')
    c.addPrivateCopyCtor()
    c.find('GetBackgroundColour').ignore()
    c.find('SetBackgroundColour').ignore()
    c.find('GetBitmap').ignore()
    c.find('SetBitmap').ignore()
    c.find('SetBitmaps').ignore()
    c.find('GetFont').ignore()
    c.find('SetFont').ignore()
    c.find('GetMarginWidth').ignore()
    c.find('SetMarginWidth').ignore()
    c.find('GetTextColour').ignore()
    c.find('SetTextColour').ignore()
    assert isinstance(c, etgtools.ClassDef)
    
    module.addItem(tools.wxListWrapperTemplate('wxMenuItemList', 'wxMenuItem'))
    module.addItem(tools.wxListWrapperTemplate('wxMenuList', 'wxMenu'))
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

