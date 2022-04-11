#---------------------------------------------------------------------------
# Name:        etg/dateevt.py
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
NAME      = "dateevt"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxDateEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/dateevt.h>")

    c = module.find('wxDateEvent')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_DATE_CHANGED = wx.PyEventBinder( wxEVT_DATE_CHANGED, 1 )
        EVT_TIME_CHANGED = wx.PyEventBinder( wxEVT_TIME_CHANGED, 1 )
        """)

    c.addPyMethod('PyGetDate', '(self)',
        doc="Return the date as a Python datetime.date object.",
        body="return wx.wxdate2pydate(self.GetDate())",
        deprecated="Use GetDate instead.")

    c.addPyCode("""\
        DateEvent.PySetDate = wx.deprecated(DateEvent.SetDate, 'Use SetDate instead.')
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

