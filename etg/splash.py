#---------------------------------------------------------------------------
# Name:        etg/splash.py
# Author:      Robin Dunn
#
# Created:     21-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "splash"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxSplashScreen",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/splash.h>')

    c = module.find('wxSplashScreen')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixTopLevelWindowClass(c)

    c.find('OnCloseWindow').ignore()
    c.find('GetSplashWindow').ignore()

    c.addCppMethod('wxBitmap*', 'GetBitmap', '()',
        doc="Get the spash screen's bitmap",
        body="""\
            return & self->GetSplashWindow()->GetBitmap();
            """)

    c.addCppMethod('void', 'SetBitmap', '(const wxBitmap& bitmap)',
        doc="Set a new bitmap for the splash screen.",
        body="""\
            self->GetSplashWindow()->SetBitmap(*bitmap);
            """)

    module.addPyCode("""\
        SPLASH_CENTER_ON_PARENT = SPLASH_CENTRE_ON_PARENT
        SPLASH_CENTER_ON_SCREEN = SPLASH_CENTRE_ON_SCREEN
        SPLASH_NO_CENTER = SPLASH_NO_CENTRE
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

