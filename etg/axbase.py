#---------------------------------------------------------------------------
# Name:        etg/axbase.py
# Author:      Robin Dunn
#
# Created:     13-May-2016
# Copyright:   (c) 2016-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import (ClassDef, MethodDef, ParamDef, TypedefDef)

PACKAGE   = "wx"
MODULE    = "_msw"
NAME      = "axbase"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # The wxPyAxBaseWindow class does not come from the parsed Doxygen xml,
    # instead it is manufactured entirely in this ETG script.  We're doing it
    # here instead of in a raw .sip file so we can run the generators on it
    # and get things like documentation and .pyi files generated like any
    # normal class.

    # First, output some C++ code
    module.addHeaderCode("""\
        class wxPyAxBaseWindow : public wxWindow
        {
            DECLARE_DYNAMIC_CLASS(wxPyAxBaseWindow)
        public:
            wxPyAxBaseWindow(wxWindow* parent, const wxWindowID id=-1,
                            const wxPoint& pos = wxDefaultPosition,
                            const wxSize& size = wxDefaultSize,
                            long style = 0,
                            const wxString& name = wxPanelNameStr)
            : wxWindow(parent, id, pos, size, style, name) {}
            wxPyAxBaseWindow() : wxWindow() {}
            virtual bool MSWTranslateMessage(WXMSG* msg)
            {
                return wxWindow::MSWTranslateMessage(msg);
            }
        };
        """)
    module.addCppCode("""\
        IMPLEMENT_DYNAMIC_CLASS(wxPyAxBaseWindow, wxWindow);
        """)

    # Now create the extractor objects that will be run through the generators
    module.addItem(TypedefDef(type='void', name='WXMSG'))

    cls = ClassDef(name='wxPyAxBaseWindow', bases=['wxWindow'],
        briefDoc="""\
            A Window class for use with ActiveX controls.

            This Window class exposes some low-level Microsoft Windows
            specific methods which can be overridden in Python.  Intended for
            use as an ActiveX container, but could also be useful
            elsewhere.""",
        items=[
            MethodDef(
                name='wxPyAxBaseWindow', isCtor=True, items=[
                    ParamDef(type='wxWindow*', name='parent'),
                    ParamDef(type='const wxWindowID', name='id', default='-1'),
                    ParamDef(type='const wxPoint&', name='pos', default='wxDefaultPosition'),
                    ParamDef(type='const wxSize&', name='size', default='wxDefaultSize'),
                    ParamDef(type='long', name='style', default='0'),
                    ParamDef(type='const wxString&', name='name', default='wxPanelNameStr'),
                ],
                overloads=[
                    MethodDef(
                        name='wxPyAxBaseWindow', isCtor=True),
                    ]),

            MethodDef(type='bool', name='MSWTranslateMessage', isVirtual=True, items=[
                ParamDef(type='WXMSG*', name='msg')
                ])
            ])

    module.addItem(cls)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

