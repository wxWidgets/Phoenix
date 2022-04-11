#---------------------------------------------------------------------------
# Name:        etg/fontutil.py
# Author:      Robin Dunn
#
# Created:     8-Oct-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "fontutil"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [  'wxNativeFontInfo',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxNativeFontInfo')
    assert isinstance(c, etgtools.ClassDef)
    c.addCppMethod('wxString*', '__str__', '()', """\
        return new wxString(self->ToString());
        """)

    # linker errors on all but MSW...
    c.find('GetPixelSize').ignore()
    c.find('SetPixelSize').ignore()

    c.addAutoProperties()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

