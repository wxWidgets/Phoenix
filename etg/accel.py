#---------------------------------------------------------------------------
# Name:        etg/accel.py
# Author:      Kevin Ollivier
#
# Created:     06-Sept-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "accel"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxAcceleratorEntry', 'wxAcceleratorTable', ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxAcceleratorTable')
    # Mac doesn't have this?
    c.find('wxAcceleratorTable').findOverload('resource').ignore()
    c.find('wxAcceleratorTable.n').arraySize = True
    c.find('wxAcceleratorTable.entries').array = True
    c.find('wxAcceleratorTable.entries').type += '*'
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

