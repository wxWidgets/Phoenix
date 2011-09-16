#---------------------------------------------------------------------------
# Name:        etg/headercol.py
# Author:      Kevin Ollivier
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "headercol"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxSettableHeaderColumn', 'wxHeaderColumn', 'wxHeaderColumnSimple', ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    module.addHeaderCode('#include <wx/headercol.h>')
    module.addHeaderCode('#include <wx/dataview.h>')
    
    c = module.find('wxHeaderColumn')
    c.abstract = True

    c = module.find('wxSettableHeaderColumn')
    c.abstract = True
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

