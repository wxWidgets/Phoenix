#---------------------------------------------------------------------------
# Name:        etg/power.py
# Author:      Robin Dunn
#
# Created:     18-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "power"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxPowerEvent",
           'wxPowerResource',
           'wxPowerResourceBlocker',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/power.h>')

    module.addHeaderCode("""\
        #ifndef wxHAS_POWER_EVENTS
        // Dummy class and other definitions for platforms that don't have power events

        class wxPowerEvent : public wxEvent
        {
        public:
            wxPowerEvent() {}
            wxPowerEvent(wxEventType evtType) : wxEvent(wxID_NONE, evtType) {}
            void Veto() {}
            bool IsVetoed() const { return false; }
            virtual wxEvent *Clone() const { return new wxPowerEvent(*this); }
        };

        enum {
            wxEVT_POWER_SUSPENDING,
            wxEVT_POWER_SUSPENDED,
            wxEVT_POWER_SUSPEND_CANCEL,
            wxEVT_POWER_RESUME,
        };
        #endif
        """)


    c = module.find('wxPowerEvent')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_POWER_SUSPENDING       = wx.PyEventBinder( wxEVT_POWER_SUSPENDING , 1 )
        EVT_POWER_SUSPENDED        = wx.PyEventBinder( wxEVT_POWER_SUSPENDED , 1 )
        EVT_POWER_SUSPEND_CANCEL   = wx.PyEventBinder( wxEVT_POWER_SUSPEND_CANCEL , 1 )
        EVT_POWER_RESUME           = wx.PyEventBinder( wxEVT_POWER_RESUME , 1 )
        """)


    c = module.find('wxPowerResourceBlocker')
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()
    # add context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'pass')

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

