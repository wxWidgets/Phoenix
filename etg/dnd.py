#---------------------------------------------------------------------------
# Name:        etg/dnd.py
# Author:      Robin Dunn
#
# Created:     29-Apr-2012
# Copyright:   (c) 2012 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "dnd"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ "interface_2wx_2dnd_8h.xml",
           #"wxDropTarget",
           #"wxTextDropTarget",
           #"wxFileDropTarget",
           #"wxDropSource",
           ]    

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/dnd.h>')
        
    #c = module.find('wxDropSource')
    #assert isinstance(c, etgtools.ClassDef)
    
    #for m in c.find('wxDropSource').all():
    #    if 'wxIcon' in m.argsString:
    #        m.ignore()
    
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

