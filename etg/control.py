#---------------------------------------------------------------------------
# Name:        etg/statbmp.py
# Author:      Kevin Ollivier
#
# Created:     26-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "control"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxControl', 'wxControlWithItems', 'wxItemContainer', 'wxItemContainerImmutable', ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxControlWithItems')
    c.abstract = True
    
    c = module.find('wxItemContainer')
    c.abstract = True
    c.find('Append').overloads = []
    c.find('Insert').overloads = []
    c.find('Set').overloads = []
    
    c.find('DetachClientObject').ignore()
    c.find('GetClientObject').ignore()
    c.find('SetClientObject').ignore()
    
    c = module.find('wxItemContainerImmutable')
    c.abstract = True
    
    module.addPyCode("PyControl = Control")
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

