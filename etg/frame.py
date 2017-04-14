#---------------------------------------------------------------------------
# Name:        etg/frame.py
# Author:      Robin Dunn
#
# Created:     6-Dec-2010
# Copyright:   (c) 2010-2017 by Total Control Software
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

    c.find('wxFrame.title').default = 'wxEmptyString'
    c.find('Create.title').default = 'wxEmptyString'    
    
    c.find('SetMenuBar.menuBar').transfer = True
    
    # We already have a MappedType for wxArrayInt, so just tweak the
    # interface to use that instead of an array size and a const int pointer.
    tools.fixSetStatusWidths(c.find('SetStatusWidths'))

    c.addProperty('MenuBar GetMenuBar SetMenuBar')
    c.addProperty('StatusBar GetStatusBar SetStatusBar')
    c.addProperty('StatusBarPane GetStatusBarPane SetStatusBarPane')
    c.addProperty('ToolBar GetToolBar SetToolBar')
    
    tools.fixTopLevelWindowClass(c)

    # Add back the virtual flag for these methods.
    # TODO: maybe these should go into a tools.addFrameVirtuals function?
    c.find('OnCreateStatusBar').isVirtual = True
    c.find('OnCreateToolBar').isVirtual = True
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

