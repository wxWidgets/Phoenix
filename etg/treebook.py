#---------------------------------------------------------------------------
# Name:        etg/treebook.py
# Author:      Robin Dunn
#
# Created:     18-Jun-2012
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "treebook"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ "wxTreebook",
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    module.addHeaderCode('#include <wx/treebook.h>')
    
    c = module.find('wxTreebook')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    tools.fixBookctrlClass(c, True)
    
    module.addPyCode("""\
        EVT_TREEBOOK_PAGE_CHANGED = wx.PyEventBinder( wxEVT_COMMAND_TREEBOOK_PAGE_CHANGED, 1 )
        EVT_TREEBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_COMMAND_TREEBOOK_PAGE_CHANGING, 1)
        EVT_TREEBOOK_NODE_COLLAPSED = wx.PyEventBinder( wxEVT_COMMAND_TREEBOOK_NODE_COLLAPSED, 1 )
        EVT_TREEBOOK_NODE_EXPANDED = wx.PyEventBinder( wxEVT_COMMAND_TREEBOOK_NODE_EXPANDED, 1 )
        """)    
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

