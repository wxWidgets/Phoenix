#---------------------------------------------------------------------------
# Name:        etg/metafile.py
# Author:      Robin Dunn
#              Dietmar Schwertberger
#
# Created:     24-Nov-2015
# Copyright:   (c) 2015 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import sys
sys.path.insert(0, r"C:\Program Files (x86)\Wing IDE 5.1" )
import wingdbstub


import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_media"
NAME      = "mediactrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxMediaCtrl',
           'wxMediaEvent']


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    module.addHeaderCode('#include "wx/mediactrl.h"')
    #module.addHeaderCode('#include "wx/mediaevent.h"')
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxMediaCtrl')
    c.addPrivateCopyCtor()

    # the C++ class has three overloaded Load(...) methods
    # for now we ignore all than the first one for loading a filename
    for item in c.findAll("Load"):
        if not "fileName" in item.argsString:
            # ignore e.g. the Load with args '(const wxURI &uri)'
            # keep e.g. '(const wxString &fileName)'
            item.ignore()


    # this is from old SWIG, do we still need it?
    #%pythoncode { LoadFromURI = LoadURI }


    c = module.find('wxMediaEvent')
    tools.fixEventClass(c)

    c.addPyCode("""\
                EVT_MEDIA_LOADED = wx.PyEventBinder( wxEVT_MEDIA_LOADED )
                EVT_MEDIA_STOP = wx.PyEventBinder( wxEVT_MEDIA_STOP )
                EVT_MEDIA_FINISHED = wx.PyEventBinder( wxEVT_MEDIA_FINISHED )
                EVT_MEDIA_STATECHANGED = wx.PyEventBinder( wxEVT_MEDIA_STATECHANGED )
                EVT_MEDIA_PLAY = wx.PyEventBinder( wxEVT_MEDIA_PLAY )
                EVT_MEDIA_PAUSE = wx.PyEventBinder( wxEVT_MEDIA_PAUSE )
                """)
    # do we need such as well?
    #    # The same as above but with the ability to specify an identifier
    #    EVT_GRID_CMD_CELL_LEFT_CLICK =     wx.PyEventBinder( wxEVT_GRID_CELL_LEFT_CLICK,    1 )

    
    # the following is in mediactrl.h:
    # #define wxMEDIABACKEND_DIRECTSHOW   wxT("wxAMMediaBackend")
    # not sure whether there would be a better way than just defining these strings here:
    module.addPyCode("""\
                MEDIABACKEND_DIRECTSHOW = "wxAMMediaBackend"
                MEDIABACKEND_MCI        = "wxMCIMediaBackend"
                MEDIABACKEND_QUICKTIME  = "wxQTMediaBackend"
                MEDIABACKEND_GSTREAMER  = "wxGStreamerMediaBackend"
                MEDIABACKEND_REALPLAYER = "wxRealPlayerMediaBackend"
                MEDIABACKEND_WMP10      = "wxWMP10MediaBackend"
                """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

