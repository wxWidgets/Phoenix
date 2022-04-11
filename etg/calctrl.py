#---------------------------------------------------------------------------
# Name:        etg/calctrl.py
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
NAME      = "calctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxCalendarEvent",
           "wxCalendarDateAttr",
           "wxCalendarCtrl",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    c = module.find('wxCalendarEvent')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_CALENDAR =                 wx.PyEventBinder( wxEVT_CALENDAR_DOUBLECLICKED, 1)
        EVT_CALENDAR_SEL_CHANGED =     wx.PyEventBinder( wxEVT_CALENDAR_SEL_CHANGED, 1)
        EVT_CALENDAR_WEEKDAY_CLICKED = wx.PyEventBinder( wxEVT_CALENDAR_WEEKDAY_CLICKED, 1)
        EVT_CALENDAR_PAGE_CHANGED =    wx.PyEventBinder( wxEVT_CALENDAR_PAGE_CHANGED, 1)
        EVT_CALENDAR_WEEK_CLICKED =    wx.PyEventBinder( wxEVT_CALENDAR_WEEK_CLICKED, 1)
        """)

    module.addPyCode("""\
        # These are deprecated, will be removed later...
        EVT_CALENDAR_DAY =             wx.PyEventBinder( wxEVT_CALENDAR_DAY_CHANGED, 1)
        EVT_CALENDAR_MONTH =           wx.PyEventBinder( wxEVT_CALENDAR_MONTH_CHANGED, 1)
        EVT_CALENDAR_YEAR =            wx.PyEventBinder( wxEVT_CALENDAR_YEAR_CHANGED, 1)
        """)
    for name in ['wxEVT_CALENDAR_DAY_CHANGED',
                 'wxEVT_CALENDAR_MONTH_CHANGED',
                 'wxEVT_CALENDAR_YEAR_CHANGED']:
        item = etgtools.GlobalVarDef(name=name, pyName=name, type='wxEventType')
        module.insertItemAfter(module.find('wxEVT_CALENDAR_WEEK_CLICKED'), item)


    cc = module.find('wxCalendarCtrl')
    gcc = tools.copyClassDef(cc, 'wxGenericCalendarCtrl')
    module.insertItemAfter(cc, gcc)

    for c in [cc, gcc]:
        tools.fixWindowClass(c)
        c.find('GetDateRange.lowerdate').out = True
        c.find('GetDateRange.upperdate').out = True
        c.find('HitTest.date').out = True
        c.find('HitTest.wd').out = True
        c.find('SetAttr.attr').transfer = True

        c.addPyMethod('PyGetDate', '(self)',
            doc="Return the date as a Python datetime.date object.",
            body="return wx.wxdate2pydate(self.GetDate())",
            deprecated="Use GetDate instead.")

        # We have convertFromPyObject mapping in place for parameters, so we
        # don't need a full wrapper method for these.
        c.addPyCode("""\
            {name}.PySetDate = wx.deprecated({name}.SetDate, 'Use SetDate instead.')
            {name}.PySetDateRange = wx.deprecated({name}.SetDateRange, 'Use SetDateRange instead.')
            """.format(name=c.name[2:]))

    cc.find('EnableYearChange').ignore()
    gcc.addHeaderCode("#include <wx/generic/calctrlg.h>")

    module.addGlobalStr('wxCalendarNameStr', cc)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

