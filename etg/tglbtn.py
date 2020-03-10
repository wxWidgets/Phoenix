#---------------------------------------------------------------------------
# Name:        etg/togglebtn.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     16-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "tglbtn"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxToggleButton',
           'wxBitmapToggleButton'
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/tglbtn.h>")

    c = module.find('wxToggleButton')
    c.find('wxToggleButton.label').default = 'wxEmptyString'
    c.find('Create.label').default = 'wxEmptyString'
    tools.fixWindowClass(c)

    c = module.find('wxBitmapToggleButton')
    c.find('wxBitmapToggleButton.label').default = 'wxNullBitmap'
    c.find('Create.label').default = 'wxNullBitmap'
    tools.fixWindowClass(c)

    module.addPyCode("""\
        EVT_TOGGLEBUTTON = PyEventBinder(wxEVT_TOGGLEBUTTON, 1)

        # deprecated wxEVT alias
        wxEVT_COMMAND_TOGGLEBUTTON_CLICKED   = wxEVT_TOGGLEBUTTON
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

