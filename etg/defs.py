#---------------------------------------------------------------------------
# Name:        etg/defs.py
# Author:      Robin Dunn
#
# Created:     19-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import sys

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "defs"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'defs_8h.xml',
           'textfile_8h.xml',  # Just for the wxTextFileType enum
           ]

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

    module.addHeaderCode("#include <wx/textfile.h>")

    # tweaks for defs.h to help SIP understand the types better
    module.find('wxInt16').type = 'short'
    module.find('wxInt64').type = 'long long'
    module.find('wxUint64').type = 'unsigned long long'

    # See src/wacky_ints.sip
    module.find('wxIntPtr').ignore()
    module.find('wxUIntPtr').ignore()

    # Correct the types for these as their values are outside the range of int
    module.find('wxUINT32_MAX').type = 'unsigned long'
    module.find('wxINT64_MIN').type = 'long long'
    module.find('wxINT64_MAX').type = 'long long'
    module.find('wxUINT64_MAX').type = 'unsigned long long'

    # Generate the code for these differently because they need to be
    # forcibly mashed into an int in the C code
    module.find('wxCANCEL_DEFAULT').forcedInt = True
    module.find('wxVSCROLL').forcedInt = True
    module.find('wxWINDOW_STYLE_MASK').forcedInt = True

    module.find('wxInt8').pyInt = True
    module.find('wxUint8').pyInt = True
    module.find('wxByte').pyInt = True

    module.find('wxDELETE').ignore()
    module.find('wxDELETEA').ignore()
    module.find('wxSwap').ignore()
    module.find('wxVaCopy').ignore()

    # Add some typedefs for basic wx types and others so the backend
    # generator knows what they are
    td = module.find('wxUIntPtr')
    module.insertItemAfter(td, etgtools.TypedefDef(type='wchar_t', name='wxUChar'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='wchar_t', name='wxChar'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='wxInt64', name='time_t'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='long long', name='wxFileOffset'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='Py_ssize_t', name='ssize_t'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='unsigned char', name='byte', pyInt=True))
    module.insertItemAfter(td, etgtools.TypedefDef(type='unsigned long', name='ulong'))



    # Forward declarations for classes that are referenced but not defined
    # yet.
    #
    # TODO: Remove these when the classes are added for real.
    # TODO: Add these classes for real :-)
    module.insertItem(0, etgtools.WigCode("""\
        // forward declarations
        class wxExecuteEnv;
        """))


    # Add some code for getting the version numbers
    module.addCppCode("""
        #include <wx/version.h>
        const int MAJOR_VERSION = wxMAJOR_VERSION;
        const int MINOR_VERSION = wxMINOR_VERSION;
        const int RELEASE_NUMBER = wxRELEASE_NUMBER;
        """)
    module.addItem(etgtools.WigCode("""
        const int MAJOR_VERSION;
        const int MINOR_VERSION;
        const int RELEASE_NUMBER;
        """))

    # TODO: these should be removed someday
    module.addPyCode("BG_STYLE_CUSTOM = BG_STYLE_PAINT")
    module.addPyCode("ADJUST_MINSIZE = 0")
    module.addPyCode("WS_EX_VALIDATE_RECURSIVELY = 0")

    # This is only supported with C++14, so ignore it for now
    module.find('wxDEPRECATED_ATTR').ignore()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

