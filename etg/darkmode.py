#---------------------------------------------------------------------------
# Name:        etg/darkmode.py
# Author:      Scott Talbert
#
# Created:     25-Jan-2026
# Copyright:   (c) 2026 by Scott Talbert
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "darkmode"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [
    'wxDarkModeSettings',
]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxDarkModeSettings')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()

    # wxDarkModeSettings and wxMenuColour are MSW-only types. Clear the
    # auto-detected class include (which would emit an unconditional
    # #include <wx/msw/darkmode.h> and fail to compile on non-MSW), and
    # instead add a guarded include plus non-MSW stubs so the wrapper
    # generates identical code for all platforms. On non-MSW, attempting to
    # use these types raises NotImplementedError via MSWEnableDarkMode.
    c.includes = []
    module.addHeaderCode("""\
        #ifdef __WXMSW__
        #include <wx/msw/darkmode.h>
        #else
        // Compile-time stubs for non-MSW platforms.
        enum class wxMenuColour {
            StandardFg,
            StandardBg,
            DisabledFg,
            HotBg
        };
        class wxDarkModeSettings {
        public:
            wxDarkModeSettings() {}
            virtual ~wxDarkModeSettings() {}
            virtual wxColour GetColour(wxSystemColour index) { return wxNullColour; }
            virtual wxColour GetMenuColour(wxMenuColour which) { return wxNullColour; }
            virtual wxPen GetBorderPen() { return wxNullPen; }
        };
        #endif // __WXMSW__
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

