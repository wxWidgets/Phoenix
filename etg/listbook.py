#---------------------------------------------------------------------------
# Name:        etg/listbook.py
# Author:      Robin Dunn
#
# Created:     18-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "listbook"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxListbook",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/listbook.h>')

    c = module.find('wxListbook')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    tools.fixBookctrlClass(c)

    c.addCppMethod('wxListView*', 'GetListView', '()',
        doc="Returns the list control used for selecting pages.",
        body="return(self->GetListView());")

    module.addPyCode("""\
        EVT_LISTBOOK_PAGE_CHANGED  = wx.PyEventBinder( wxEVT_LISTBOOK_PAGE_CHANGED, 1 )
        EVT_LISTBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_LISTBOOK_PAGE_CHANGING, 1 )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_LISTBOOK_PAGE_CHANGED   = wxEVT_LISTBOOK_PAGE_CHANGED
        wxEVT_COMMAND_LISTBOOK_PAGE_CHANGING  = wxEVT_LISTBOOK_PAGE_CHANGING
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

