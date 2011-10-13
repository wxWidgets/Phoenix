#---------------------------------------------------------------------------
# Name:        etg/collpane.py
# Author:      Kevin Ollivier
#
# Created:     27-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "collpane"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  =    [
                'wxCollapsiblePane',
                'wxCollapsiblePaneEvent',
            ]
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    module.addHeaderCode("#include <wx/collpane.h>")
    module.addPyCode(
        "EVT_COLLAPSIBLEPANE_CHANGED = wx.PyEventBinder( wxEVT_COMMAND_COLLPANE_CHANGED )")
    
    c = module.find('wxCollapsiblePane')
    c.find('wxCollapsiblePane.label').default = 'wxEmptyString'
    c.find('Create.label').default = 'wxEmptyString'
    
    tools.fixWindowClass(c)
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addAutoProperties(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

