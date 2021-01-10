#---------------------------------------------------------------------------
# Name:        etg/fdrepdlg.py
# Author:      Robin Dunn
#
# Created:     30-Mar-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "fdrepdlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxFindDialogEvent",
           "wxFindReplaceData",
           "wxFindReplaceDialog",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFindDialogEvent')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_FIND = wx.PyEventBinder( wxEVT_FIND, 1 )
        EVT_FIND_NEXT = wx.PyEventBinder( wxEVT_FIND_NEXT, 1 )
        EVT_FIND_REPLACE = wx.PyEventBinder( wxEVT_FIND_REPLACE, 1 )
        EVT_FIND_REPLACE_ALL = wx.PyEventBinder( wxEVT_FIND_REPLACE_ALL, 1 )
        EVT_FIND_CLOSE = wx.PyEventBinder( wxEVT_FIND_CLOSE, 1 )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_FIND              = wxEVT_FIND
        wxEVT_COMMAND_FIND_NEXT         = wxEVT_FIND_NEXT
        wxEVT_COMMAND_FIND_REPLACE      = wxEVT_FIND_REPLACE
        wxEVT_COMMAND_FIND_REPLACE_ALL  = wxEVT_FIND_REPLACE_ALL
        wxEVT_COMMAND_FIND_CLOSE        = wxEVT_FIND_CLOSE
        """)

    c = module.find('wxFindReplaceDialog')
    tools.fixTopLevelWindowClass(c)
    c.find('wxFindReplaceDialog.data').keepReference = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

