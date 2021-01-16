#---------------------------------------------------------------------------
# Name:        etg/dirctrl.py
# Author:      Robin Dunn
#
# Created:     29-Mar-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "dirctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxGenericDirCtrl",
           "wxDirFilterListCtrl",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/dirctrl.h>")

    c = module.find('wxGenericDirCtrl')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixTopLevelWindowClass(c)

    c.find('GetPaths').ignore()
    c.addCppMethod('wxArrayString*', 'GetPaths', '()', pyArgsString="() -> list",
        doc='Returns a list of the currently selected paths.',
        body="""\
            wxArrayString* paths = new wxArrayString;
            self->GetPaths(*paths);
            return paths;
            """
    )

    module.addPyCode("""\
        EVT_DIRCTRL_SELECTIONCHANGED = wx.PyEventBinder( wxEVT_DIRCTRL_SELECTIONCHANGED, 1 )
        EVT_DIRCTRL_FILEACTIVATED = wx.PyEventBinder( wxEVT_DIRCTRL_FILEACTIVATED, 1 )
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

