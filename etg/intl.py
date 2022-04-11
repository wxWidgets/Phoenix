#---------------------------------------------------------------------------
# Name:        etg/intl.py
# Author:      Robin Dunn
#
# Created:     27-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "intl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxLanguageInfo',
           'wxLocale',

           'language_8h.xml',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxLocale')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateAssignOp()
    c.addPrivateCopyCtor()

    c.addCppMethod('int', '__nonzero__', '()', 'return self->IsOk();')
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")


    c = module.find('wxLanguageInfo')
    c.find('WinLang').ignore()
    c.find('WinSublang').ignore()
    c.find('GetLCID').ignore()

    module.addItem(etgtools.WigCode("""\
        char* wxSetlocale(int category, const char *locale);
        char* wxSetlocale(int category, const wxString& locale);
        """))


    module.addPyCode("""\
    #----------------------------------------------------------------------------
    # Add the directory where the wxWidgets catalogs were installed
    # to the default catalog path, if they were put in the package dir.
    import os
    _localedir = os.path.join(os.path.dirname(__file__), "locale")
    if os.path.exists(_localedir):
        if isinstance(_localedir, (bytes, bytearray)):
            _localedir = _localedir.decode(_sys.getfilesystemencoding())
        Locale.AddCatalogLookupPathPrefix(_localedir)
    del os
    #----------------------------------------------------------------------------
    """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

