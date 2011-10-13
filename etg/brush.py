#---------------------------------------------------------------------------
# Name:        etg/brush.py
# Author:      Robin Dunn
#
# Created:     2-Sept-2011
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
ITEMS  = [ 'wxBrush', 'wxBrushList', ]    
    
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

    c.addCppMethod('int', '__nonzero__', '()', """\
        return self->IsOk();
        """)


    c.addCppCode("""\
        #ifdef __WXMAC__
        #include <wx/osx/private.h>
        #endif
        """)    
    c.addCppMethod('void', 'MacSetTheme', '(int macThemeBrushID)', """\
        #ifdef __WXMAC__
            self->SetColour(wxColour(wxMacCreateCGColorFromHITheme(macThemeBrushID)));
        #else
            wxPyRaiseNotImplemented(); 
        #endif
        """)

    
    c.addGetterSetterProps()
    
    
    # The stock Brush items are documented as simple pointers, but in reality
    # they are macros that evaluate to a function call that returns a brush
    # pointer, and that is only valid *after* the wx.App object has been
    # created. That messes up the code that SIP generates for them, so we need
    # to come up with another solution. So instead we will just create
    # uninitialized brush in a block of Python code, that will then be
    # intialized later when the wx.App is created.
    c.addCppMethod('void', '_copyFrom', '(const wxBrush* other)', 
                   "*self = *other;",
                   briefDoc="For internal use only.")  # ??
    pycode = '# These stock brushes will be initialized when the wx.App object is created.\n'
    for item in module:
        if '_BRUSH' in item.name:
            item.ignore()
            pycode += '%s = Brush()\n' % tools.removeWxPrefix(item.name)
    module.addPyCode(pycode)
            
    
    # it is delay-initialized, see stockgdi.sip
    module.find('wxTheBrushList').ignore()
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

