#---------------------------------------------------------------------------
# Name:        etg/stdpaths.py
# Author:      Kevin Ollivier
#
# Created:     27-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "stdpaths"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxStandardPaths' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxStandardPaths')
    assert isinstance(c, etgtools.ClassDef)
    c.find('wxStandardPaths').ignore(False)
    c.abstract = True

    # Since the ctor is protected we need to tell SIP how to get a default
    # instance of this class
    c.instanceCode = 'sipCpp = & wxStandardPaths::Get();'

    c.find('IgnoreAppSubDir').ignore()
    c.find('DontIgnoreAppSubDir').ignore()
    c.find('IgnoreAppBuildSubDirs').ignore()

    c.find('MSWGetShellDir').setCppCode("""\
    #ifdef __WXMSW__
        return new wxString(wxStandardPaths::MSWGetShellDir(csidl));
    #else
        return new wxString;
    #endif
    """)

    c.find('SetInstallPrefix').setCppCode("""\
    #ifndef wxHAS_STDPATHS_INSTALL_PREFIX
    #else
        self->SetInstallPrefix(*prefix);
    #endif
    """)
    c.find('GetInstallPrefix').setCppCode("""\
    #ifndef wxHAS_STDPATHS_INSTALL_PREFIX
        return new wxString;
    #else
        return new wxString(self->GetInstallPrefix());
    #endif
    """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

