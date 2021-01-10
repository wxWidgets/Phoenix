#---------------------------------------------------------------------------
# Name:        etg/choicebk.py
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
NAME      = "choicebk"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxChoicebook",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/choicebk.h>')

    c = module.find('wxChoicebook')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    tools.fixBookctrlClass(c)

    c.addCppMethod('wxChoice*', 'GetChoiceCtrl', '()',
        doc="Returns the choice control used for selecting pages.",
        body="return(self->GetChoiceCtrl());")


    module.addPyCode("""\
        EVT_CHOICEBOOK_PAGE_CHANGED  = wx.PyEventBinder( wxEVT_CHOICEBOOK_PAGE_CHANGED, 1 )
        EVT_CHOICEBOOK_PAGE_CHANGING = wx.PyEventBinder( wxEVT_CHOICEBOOK_PAGE_CHANGING, 1 )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGED   = wxEVT_CHOICEBOOK_PAGE_CHANGED
        wxEVT_COMMAND_CHOICEBOOK_PAGE_CHANGING  = wxEVT_CHOICEBOOK_PAGE_CHANGING
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

