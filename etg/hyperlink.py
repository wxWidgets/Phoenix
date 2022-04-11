#---------------------------------------------------------------------------
# Name:        etg/hyperlink.py
# Author:      Robin Dunn
#
# Created:     09-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "hyperlink"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHyperlinkEvent",
           "wxHyperlinkCtrl",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/hyperlink.h>")

    c = module.find('wxHyperlinkEvent')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixEventClass(c)
    module.addPyCode("""\
        EVT_HYPERLINK = wx.PyEventBinder( wxEVT_HYPERLINK, 1 )

        # deprecated wxEVT alias
        wxEVT_COMMAND_HYPERLINK  = wxEVT_HYPERLINK
        """)

    c = module.find('wxHyperlinkCtrl')
    tools.fixWindowClass(c)

    c.find('wxHyperlinkCtrl.label').default = 'wxEmptyString'
    c.find('wxHyperlinkCtrl.url').default = 'wxEmptyString'
    c.find('Create.label').default = 'wxEmptyString'
    c.find('Create.url').default = 'wxEmptyString'

    module.addGlobalStr('wxHyperlinkCtrlNameStr', c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

