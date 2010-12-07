#---------------------------------------------------------------------------
# Name:        etg/region.py
# Author:      Robin Dunn
#
# Created:     30-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "region"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxRegionIterator',
           'wxRegion'
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    
    c = module.find('wxRegion')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)
    c.find('GetBox').findOverload('wxCoord').ignore()
    c.addProperty('Box GetBox')
    
    c = module.find('wxRegionIterator')
    c.find('operator++').ignore()
    
    c.addCppMethod('void', 'Next', '()', 'self->operator++();')
    c.addCppMethod('int', '__nonzero__', '()', 'return (int)self->operator bool();')
    
    c.addProperty('H GetH')
    c.addProperty('Height GetHeight')
    c.addProperty('Rect GetRect')
    c.addProperty('W GetW')
    c.addProperty('Width GetWidth')
    c.addProperty('X GetX')
    c.addProperty('Y GetY')
    

    # This is defined in the docs, but not in any of the real headers!
    module.find('wxNullRegion').ignore()
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

