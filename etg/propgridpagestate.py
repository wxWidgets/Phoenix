#---------------------------------------------------------------------------
# Name:        etg/propgridpagestate.py
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
NAME      = "propgridpagestate"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxPropertyGridHitTestResult',
           'wxPropertyGridIterator',
           'wxPGVIterator',
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxPropertyGridHitTestResult')
    assert isinstance(c, etgtools.ClassDef)
    
    
    c = module.find('wxPropertyGridIterator')
    # The base class is not documented, and it looks like it may not be
    # needed, so just pretend this class has no base class. At least for
    # now...
    c.bases = []
    
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

