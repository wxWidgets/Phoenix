#---------------------------------------------------------------------------
# Name:        etg/splitter.py
# Author:      Kevin Ollivier
#              Robin Dunn
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
NAME      = "splitter"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  =    [ 'wxSplitterWindow',
              'wxSplitterEvent',
            ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    module.addHeaderCode("#include <wx/splitter.h>")

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxSplitterWindow')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    # We can do these with events so we may as well save the overhead of
    # virtual methods
    c.find('OnDoubleClickSash').ignore()
    c.find('OnSashPositionChange').ignore()
    c.find('OnUnsplit').ignore()

    c.addAutoProperties()
    c.addProperty('SashInvisible', 'IsSashInvisible', 'SetSashInvisible')


    c = module.find('wxSplitterEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_SPLITTER_SASH_POS_CHANGED = wx.PyEventBinder( wxEVT_SPLITTER_SASH_POS_CHANGED, 1 )
        EVT_SPLITTER_SASH_POS_CHANGING = wx.PyEventBinder( wxEVT_SPLITTER_SASH_POS_CHANGING, 1 )
        EVT_SPLITTER_DOUBLECLICKED = wx.PyEventBinder( wxEVT_SPLITTER_DOUBLECLICKED, 1 )
        EVT_SPLITTER_UNSPLIT = wx.PyEventBinder( wxEVT_SPLITTER_UNSPLIT, 1 )
        EVT_SPLITTER_DCLICK = EVT_SPLITTER_DOUBLECLICKED

        # deprecated wxEVT aliases
        wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGED   = wxEVT_SPLITTER_SASH_POS_CHANGED
        wxEVT_COMMAND_SPLITTER_SASH_POS_CHANGING  = wxEVT_SPLITTER_SASH_POS_CHANGING
        wxEVT_COMMAND_SPLITTER_DOUBLECLICKED      = wxEVT_SPLITTER_DOUBLECLICKED
        wxEVT_COMMAND_SPLITTER_UNSPLIT            = wxEVT_SPLITTER_UNSPLIT
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

