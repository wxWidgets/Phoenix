#---------------------------------------------------------------------------
# Name:        etg/tooltip.py
# Author:      Robin Dunn
#
# Created:     30-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "tooltip"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxToolTip' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxToolTip')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()

    # TODO: This is MSW only
    c.find('SetMaxWidth').setCppCode("""\
    #ifdef __WXMSW__
        wxToolTip::SetMaxWidth(width);
    #endif
    """)

    c.addProperty('Tip GetTip SetTip')
    c.addProperty('Window GetWindow')

    c.addPrivateCopyCtor()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

