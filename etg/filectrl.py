#---------------------------------------------------------------------------
# Name:        etg/filectrl.py
# Author:      Robin Dunn
#
# Created:     12-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "filectrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxFileCtrl",
           "wxFileCtrlEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/filectrl.h>')

    c = module.find('wxFileCtrl')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    module.addGlobalStr('wxFileCtrlNameStr', c)

    c.find('GetFilenames').ignore()
    c.addCppMethod('wxArrayString*', 'GetFilenames', '()', doc="""\
        Returns a list of filenames selected in the control.  This function
        should only be used with controls which have the wx.FC_MULTIPLE style,
        use GetFilename for the others.""",
        body="""\
        wxArrayString* arr = new wxArrayString;
        self->GetFilenames(*arr);
        return arr;""",
        factory=True)

    c.find('GetPaths').ignore()
    c.addCppMethod('wxArrayString*', 'GetPaths', '()', doc="""\
        Returns a list of the full paths (directory and filename) of the files
        chosen. This function should only be used with controlss which have
        the wx.FC_MULTIPLE style, use GetPath for the others.
        """,
        body="""\
        wxArrayString* arr = new wxArrayString;
        self->GetPaths(*arr);
        return arr;""",
        factory=True)



    c = module.find('wxFileCtrlEvent')
    tools.fixEventClass(c)
    module.addPyCode("""\
        EVT_FILECTRL_SELECTIONCHANGED = wx.PyEventBinder( wxEVT_FILECTRL_SELECTIONCHANGED, 1)
        EVT_FILECTRL_FILEACTIVATED = wx.PyEventBinder( wxEVT_FILECTRL_FILEACTIVATED, 1)
        EVT_FILECTRL_FOLDERCHANGED = wx.PyEventBinder( wxEVT_FILECTRL_FOLDERCHANGED, 1)
        EVT_FILECTRL_FILTERCHANGED = wx.PyEventBinder( wxEVT_FILECTRL_FILTERCHANGED, 1)
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

