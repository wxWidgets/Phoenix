#---------------------------------------------------------------------------
# Name:        etg/cursor.py
# Author:      Kevin Ollivier
#
# Created:     06-Sept-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "cursor"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxCursor', ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    c = module.find('wxCursor')
    assert isinstance(c, etgtools.ClassDef)
    
    c.find('wxCursor').findOverload('bits').ignore()
    c.find('wxCursor').findOverload('cursorName').find('type').default='wxBITMAP_TYPE_ANY'    
    # TODO: This ctor ^^ in Classic has a custom implementation for wxGTK that
    # sets the hotspot. Is that still needed?

    c.addCppMethod('int', '__nonzero__', '()', """\
        return self->IsOk();
    """)

    c.addCppMethod('long', 'GetHandle', '()', """\
    #ifdef __WXMSW__
        return self->GetHandle()
    #endif
        return 0;""",
    briefDoc="Get the handle for the Cursor.  Windows only.")
    
    c.addCppMethod('void', 'SetHandle', '(long handle)', """\
    #ifdef __WXMSW__
        self->SetHandle(handle)
    #endif""",
    briefDoc="Set the handle to use for this Cursor.  Windows only.")
    
    # TODO:  Classic has MSW-only getters and setters for width, height, depth, and size.
    
    module.find('wxCROSS_CURSOR').ignore()
    module.find('wxHOURGLASS_CURSOR').ignore()
    module.find('wxSTANDARD_CURSOR').ignore()
    
    module.addPyCode('StockCursor = wx.deprecated(Cursor)')
    module.addPyCode('CursorFromImage = wx.deprecated(Cursor)')
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

