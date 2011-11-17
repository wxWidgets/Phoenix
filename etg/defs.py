#---------------------------------------------------------------------------
# Name:        etg/defs.py
# Author:      Robin Dunn
#
# Created:     19-Nov-2010
# Copyright:   (c) 2011 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "defs"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'defs_8h.xml' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING,
                                check4unittest=False)
    etgtools.parseDoxyXML(module, ITEMS)
    module.check4unittest = False
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
        
    # tweaks for defs.h
    module.find('wxInt16').type = 'short'
    module.find('wxInt64').type = 'long long'
    module.find('wxUint64').type = 'unsigned long long'
    module.find('wxIntPtr').type =  'long'           #'ssize_t'
    module.find('wxUIntPtr').type = 'unsigned long'  #'size_t'
    module.find('wxInt8').pyInt = True
    module.find('wxUint8').pyInt = True
    module.find('wxByte').pyInt = True
    
    module.find('wxDELETE').ignore()
    module.find('wxDELETEA').ignore()
    module.find('wxSwap').ignore()
    module.find('wxVaCopy').ignore()
    
    # add some typedefs for wxChar, wxUChar, etc.
    td = module.find('wxUIntPtr')
    module.insertItemAfter(td, etgtools.TypedefDef(type='wchar_t', name='wxUChar'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='wchar_t', name='wxChar'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='unsigned int', name='size_t'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='long', name='time_t'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='int', name='wxPrintQuality'))

    
    # Forward declarations for classes that are referenced but not defined
    # yet. 
    # 
    # TODO: Remove these when the classes are added for real.
    # TODO: Add these classes for real :-)
    module.insertItem(0, etgtools.WigCode("""\
        // forward declarations
        class wxPalette;
        class wxDropTarget;
        class wxCaret;
        class wxImageHandler;
        class wxToolBar;
        class wxExecuteEnv;
        class wxInputStream;
        class wxOutputStream;
    """))
    
    
    # TBD: I've always disliked the WXK_* names. Should I rename all the items
    # in the wxKeyCode enum to be KEY_* names?

    
    # Add some code for getting the version numbers
    module.addCppCode("""
        #include <wx/version.h>
        const int MAJOR_VERSION = wxMAJOR_VERSION;
        const int MINOR_VERSION = wxMINOR_VERSION;           
        const int RELEASE_NUMBER = wxRELEASE_NUMBER;     
        const int SUBRELEASE_NUMBER = wxSUBRELEASE_NUMBER;
        """)
    module.addItem(etgtools.WigCode("""
        const int MAJOR_VERSION;
        const int MINOR_VERSION;
        const int RELEASE_NUMBER;
        const int SUBRELEASE_NUMBER;
        """))

    module.addPyCode("wx.BG_STYLE_CUSTOM = wx.BG_STYLE_PAINT")

    # Some aliases that should be phased out eventually, (sooner rather than
    # later.) They are already gone (or wrapped by an #if) in the C++ code,
    # and so are not found in the documentation...
    module.addPyCode("""\
        wx.DEFAULT    = wx.FONTFAMILY_DEFAULT
        wx.DECORATIVE = wx.FONTFAMILY_DECORATIVE
        wx.ROMAN      = wx.FONTFAMILY_ROMAN
        wx.SCRIPT     = wx.FONTFAMILY_SCRIPT
        wx.SWISS      = wx.FONTFAMILY_SWISS
        wx.MODERN     = wx.FONTFAMILY_MODERN
        wx.TELETYPE   = wx.FONTFAMILY_TELETYPE

        wx.NORMAL = wx.FONTWEIGHT_NORMAL
        wx.LIGHT  = wx.FONTWEIGHT_LIGHT
        wx.BOLD   = wx.FONTWEIGHT_BOLD
        
        wx.NORMAL = wx.FONTSTYLE_NORMAL
        wx.ITALIC = wx.FONTSTYLE_ITALIC
        wx.SLANT  = wx.FONTSTYLE_SLANT
            
        wx.SOLID       = wx.PENSTYLE_SOLID
        wx.DOT         = wx.PENSTYLE_DOT 
        wx.LONG_DASH   = wx.PENSTYLE_LONG_DASH 
        wx.SHORT_DASH  = wx.PENSTYLE_SHORT_DASH 
        wx.DOT_DASH    = wx.PENSTYLE_DOT_DASH 
        wx.USER_DASH   = wx.PENSTYLE_USER_DASH 
        wx.TRANSPARENT = wx.PENSTYLE_TRANSPARENT 

        wx.STIPPLE_MASK_OPAQUE = wx.BRUSHSTYLE_STIPPLE_MASK_OPAQUE 
        wx.STIPPLE_MASK        = wx.BRUSHSTYLE_STIPPLE_MASK 
        wx.STIPPLE             = wx.BRUSHSTYLE_STIPPLE 
        wx.BDIAGONAL_HATCH     = wx.BRUSHSTYLE_BDIAGONAL_HATCH 
        wx.CROSSDIAG_HATCH     = wx.BRUSHSTYLE_CROSSDIAG_HATCH 
        wx.FDIAGONAL_HATCH     = wx.BRUSHSTYLE_FDIAGONAL_HATCH 
        wx.CROSS_HATCH         = wx.BRUSHSTYLE_CROSS_HATCH 
        wx.HORIZONTAL_HATCH    = wx.BRUSHSTYLE_HORIZONTAL_HATCH 
        wx.VERTICAL_HATCH      = wx.BRUSHSTYLE_VERTICAL_HATCH     
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

