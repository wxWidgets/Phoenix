#---------------------------------------------------------------------------
# Name:        etg/propgrid.py
# Author:      Robin Dunn
#
# Created:     23-Feb-2015
# Copyright:   (c) 2015 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_propgrid"
NAME      = "propgrid"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'interface_2wx_2propgrid_2propgrid_8h.xml',
           'wxPGValidationInfo',
           'wxPropertyGrid',
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    module.find('wxPGSortCallback').ignore()
    
    c = module.find('wxPGValidationInfo')
    assert isinstance(c, etgtools.ClassDef)
    
    
    c = module.find('wxPropertyGrid')
    assert isinstance(c, etgtools.ClassDef)
    c.bases.remove('wxScrollHelper')
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

