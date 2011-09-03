#---------------------------------------------------------------------------
# Name:        etg/brush.py
# Author:      Robin Dunn
#
# Created:     
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "brush"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxBrush' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    
    c = module.find('wxBrush')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)
    
    # TODO: Fix these. I'm not sure why exactly, but in the CPP code
    # they end up with the wrong signature.
    module.find('wxBLUE_BRUSH').ignore()
    module.find('wxGREEN_BRUSH').ignore()
    module.find('wxYELLOW_BRUSH').ignore()
    module.find('wxWHITE_BRUSH').ignore()
    module.find('wxBLACK_BRUSH').ignore()
    module.find('wxGREY_BRUSH').ignore()
    module.find('wxMEDIUM_GREY_BRUSH').ignore()
    module.find('wxLIGHT_GREY_BRUSH').ignore()
    module.find('wxTRANSPARENT_BRUSH').ignore()
    module.find('wxCYAN_BRUSH').ignore()
    module.find('wxRED_BRUSH').ignore()

    module.find('wxTheBrushList').ignore()
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

