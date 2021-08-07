#---------------------------------------------------------------------------
# Name:        etg/headerctrl.py
# Author:      Robin Dunn
#
# Created:     29-Jun-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "headerctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHeaderCtrl",
           "wxHeaderCtrlSimple",
           "wxHeaderCtrlEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHeaderCtrl')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)

    module.addGlobalStr('wxHeaderCtrlNameStr', c)
    module.addHeaderCode('#include <wx/headerctrl.h>')

    # Uningnore the protected virtuals that are intended to be overridden in
    # derived classes.
    for name in ['GetColumn', 'UpdateColumnVisibility', 'UpdateColumnsOrder',
                 'UpdateColumnWidthToFit', 'OnColumnCountChanging']:
        c.find(name).ignore(False)
        c.find(name).isVirtual = True
    c.find('GetColumn').isPureVirtual = True
    c.find('GetColumn')._virtualCatcherCode = """\
        PyObject *resObj = sipCallMethod(0,sipMethod,"u",idx);
        sipIsErr = (!resObj || sipParseResult(0,sipMethod,resObj,"H1",sipType_wxHeaderColumn,&sipRes) < 0);
        if (sipIsErr)
            PyErr_Print();
        Py_XDECREF(resObj);
        if (sipIsErr)
            return *(new wxHeaderColumnSimple(""));
        """

    #-------------------------------------------------------
    c = module.find('wxHeaderCtrlSimple')
    tools.fixWindowClass(c)

    # Uningnore the protected virtuals that are intended to be overridden in
    # derived classes.
    c.find('GetBestFittingWidth').ignore(False)
    c.find('GetBestFittingWidth').isVirtual = True

    # indicate the the base class virtuals have implementations here
    c.addItem(etgtools.WigCode("""\
        virtual const wxHeaderColumn& GetColumn(unsigned int idx) const;
        virtual void UpdateColumnVisibility(unsigned int idx, bool show);
        virtual void UpdateColumnsOrder(const wxArrayInt& order);
        virtual bool UpdateColumnWidthToFit(unsigned int idx, int widthTitle);
        virtual void OnColumnCountChanging(unsigned int count);
        """, protection='protected'))


    #-------------------------------------------------------
    c = module.find('wxHeaderCtrlEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_HEADER_CLICK =              wx.PyEventBinder( wxEVT_HEADER_CLICK )
        EVT_HEADER_RIGHT_CLICK =        wx.PyEventBinder( wxEVT_HEADER_RIGHT_CLICK )
        EVT_HEADER_MIDDLE_CLICK =       wx.PyEventBinder( wxEVT_HEADER_MIDDLE_CLICK )
        EVT_HEADER_DCLICK =             wx.PyEventBinder( wxEVT_HEADER_DCLICK )
        EVT_HEADER_RIGHT_DCLICK =       wx.PyEventBinder( wxEVT_HEADER_RIGHT_DCLICK )
        EVT_HEADER_MIDDLE_DCLICK =      wx.PyEventBinder( wxEVT_HEADER_MIDDLE_DCLICK )
        EVT_HEADER_SEPARATOR_DCLICK =   wx.PyEventBinder( wxEVT_HEADER_SEPARATOR_DCLICK )
        EVT_HEADER_BEGIN_RESIZE =       wx.PyEventBinder( wxEVT_HEADER_BEGIN_RESIZE )
        EVT_HEADER_RESIZING =           wx.PyEventBinder( wxEVT_HEADER_RESIZING )
        EVT_HEADER_END_RESIZE =         wx.PyEventBinder( wxEVT_HEADER_END_RESIZE )
        EVT_HEADER_BEGIN_REORDER =      wx.PyEventBinder( wxEVT_HEADER_BEGIN_REORDER )
        EVT_HEADER_END_REORDER =        wx.PyEventBinder( wxEVT_HEADER_END_REORDER )
        EVT_HEADER_DRAGGING_CANCELLED = wx.PyEventBinder( wxEVT_HEADER_DRAGGING_CANCELLED )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_HEADER_CLICK               = wxEVT_HEADER_CLICK
        wxEVT_COMMAND_HEADER_RIGHT_CLICK         = wxEVT_HEADER_RIGHT_CLICK
        wxEVT_COMMAND_HEADER_MIDDLE_CLICK        = wxEVT_HEADER_MIDDLE_CLICK
        wxEVT_COMMAND_HEADER_DCLICK              = wxEVT_HEADER_DCLICK
        wxEVT_COMMAND_HEADER_RIGHT_DCLICK        = wxEVT_HEADER_RIGHT_DCLICK
        wxEVT_COMMAND_HEADER_MIDDLE_DCLICK       = wxEVT_HEADER_MIDDLE_DCLICK
        wxEVT_COMMAND_HEADER_SEPARATOR_DCLICK    = wxEVT_HEADER_SEPARATOR_DCLICK
        wxEVT_COMMAND_HEADER_BEGIN_RESIZE        = wxEVT_HEADER_BEGIN_RESIZE
        wxEVT_COMMAND_HEADER_RESIZING            = wxEVT_HEADER_RESIZING
        wxEVT_COMMAND_HEADER_END_RESIZE          = wxEVT_HEADER_END_RESIZE
        wxEVT_COMMAND_HEADER_BEGIN_REORDER       = wxEVT_HEADER_BEGIN_REORDER
        wxEVT_COMMAND_HEADER_END_REORDER         = wxEVT_HEADER_END_REORDER
        wxEVT_COMMAND_HEADER_DRAGGING_CANCELLED  = wxEVT_HEADER_DRAGGING_CANCELLED
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()
