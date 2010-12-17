#---------------------------------------------------------------------------
# Name:        etg/frame.py
# Author:      Robin Dunn
#
# Created:     6-Dec-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "frame"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxFrame' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
        
    c = module.find('wxFrame')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    
    c.find('wxFrame.title').default = 'wxEmptyString'
    c.find('Create.title').default = 'wxEmptyString'    
    
    c.find('SetStatusWidths.n').arraySize = True
    c.find('SetStatusWidths.widths_field').array = True
    
    c.addProperty('MenuBar GetMenuBar SetMenuBar')
    c.addProperty('StatusBar GetStatusBar SetStatusBar')
    c.addProperty('StatusBarPane GetStatusBarPane SetStatusBarPane')
    c.addProperty('ToolBar GetToolBar SetToolBar')
    
        
    tools.removeVirtuals(c)
    tools.addWindowVirtuals(c)

    # TODO: should these go into a tools.addFrameVirtuals function?
    c.find('OnCreateStatusBar').isVirtual = True
    c.find('OnCreateToolBar').isVirtual = True
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

