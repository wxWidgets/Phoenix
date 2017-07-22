#---------------------------------------------------------------------------
# Name:        etg/fswatcher.py
# Author:      Robin Dunn
#
# Created:     29-Jul-2012
# Copyright:   (c) 2012-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "fswatcher"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxFileSystemWatcher",
           "wxFileSystemWatcherEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("""
        #include <wx/fswatcher.h>
        #ifndef wxHAS_INOTIFY
        #define wxFSW_EVENT_UNMOUNT 0x2000
        #endif
        """)

    c = module.find('wxFileSystemWatcher')
    assert isinstance(c, etgtools.ClassDef)


    c = module.find('wxFileSystemWatcherEvent')
    tools.fixEventClass(c)

    c.addPyCode("""\
        EVT_FSWATCHER = wx.PyEventBinder(wxEVT_FSWATCHER)
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

