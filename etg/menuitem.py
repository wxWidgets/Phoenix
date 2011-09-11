#---------------------------------------------------------------------------
# Name:        etg/menuitem.py
# Author:      Robin Dunn
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "menuitem"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxMenuItem' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    
    c = module.find('wxMenuItem')
    assert isinstance(c, etgtools.ClassDef)
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
    module.addItem(tools.wxListWrapperTemplate('wxMenuItemList', 'wxMenuItem'))
    

    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

