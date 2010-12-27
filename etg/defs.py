#---------------------------------------------------------------------------
# Name:        etg/defs.py
# Author:      Robin Dunn
#
# Created:     19-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
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
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
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
    
    
    # Forward declarations for classes that are referenced but not defined
    # yet. 
    # 
    # TODO: Remove these when the classes are added for real.
    # TODO: Add these classes for real :-)
    module.insertItem(0, etgtools.WigCode("""\
        // forward declarations
        class wxDC;
        class wxMenu;
        class wxCursor;
        class wxBitmap;
        class wxWindowList;  
        class wxSizer;
        class wxPalette;
        class wxAcceleratorTable;
        class wxDropTarget;
        class wxCaret;
        class wxIcon;
        class wxIconBundle;
        class wxStatusBar;
        class wxToolBar;
        class wxMenuBar;
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

    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

