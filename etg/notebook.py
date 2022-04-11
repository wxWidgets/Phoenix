#---------------------------------------------------------------------------
# Name:        etg/notebook.py
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
NAME      = "notebook"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  =    [ 'wxNotebook' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/notebook.h>')

    c = module.find('wxNotebook')
    c.find('OnSelChange').ignore()

    tools.fixWindowClass(c)
    tools.fixBookctrlClass(c)

    module.addGlobalStr('wxNotebookNameStr', c)

    module.addPyCode("""\
        EVT_NOTEBOOK_PAGE_CHANGED  = wx.PyEventBinder( wxEVT_NOTEBOOK_PAGE_CHANGED, 1 )
        EVT_NOTEBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_NOTEBOOK_PAGE_CHANGING, 1 )
        """)

    module.addPyCode("""\
        # Aliases for the "best book" control as described in the overview
        BookCtrl =                       Notebook
        wxEVT_BOOKCTRL_PAGE_CHANGED =    wxEVT_NOTEBOOK_PAGE_CHANGED
        wxEVT_BOOKCTRL_PAGE_CHANGING =   wxEVT_NOTEBOOK_PAGE_CHANGING
        EVT_BOOKCTRL_PAGE_CHANGED =      EVT_NOTEBOOK_PAGE_CHANGED
        EVT_BOOKCTRL_PAGE_CHANGING =     EVT_NOTEBOOK_PAGE_CHANGING

        # deprecated wxEVT aliases
        wxEVT_COMMAND_BOOKCTRL_PAGE_CHANGED   = wxEVT_BOOKCTRL_PAGE_CHANGED
        wxEVT_COMMAND_BOOKCTRL_PAGE_CHANGING  = wxEVT_BOOKCTRL_PAGE_CHANGING
        wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGED   = wxEVT_NOTEBOOK_PAGE_CHANGED
        wxEVT_COMMAND_NOTEBOOK_PAGE_CHANGING  = wxEVT_NOTEBOOK_PAGE_CHANGING
        """)

    module.addPyCode("""\
        # Add wx.NotebookPage alias, as seen in the documentation
        NotebookPage = Window
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

