#---------------------------------------------------------------------------
# Name:        etg/collheaderctrl.py
# Author:      Robin Dunn
#
# Created:     29-Oct-2019
# Copyright:   (c) 2019-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "collheaderctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxCollapsibleHeaderCtrl',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/collheaderctrl.h>')

    c = module.find('wxCollapsibleHeaderCtrl')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    c.find('wxCollapsibleHeaderCtrl.label').default = '""'
    c.find('Create.label').default = '""'

    module.addGlobalStr('wxCollapsibleHeaderCtrlNameStr', c)
    module.addItem(etgtools.WigCode(
        "wxEventType wxEVT_COLLAPSIBLEHEADER_CHANGED /PyName=wxEVT_COLLAPSIBLEHEADER_CHANGED/;"))
    module.addPyCode("""\
        EVT_COLLAPSIBLEHEADER_CHANGED = PyEventBinder(wxEVT_COLLAPSIBLEHEADER_CHANGED, 1)
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

