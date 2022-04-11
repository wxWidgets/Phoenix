#---------------------------------------------------------------------------
# Name:        etg/taskbar.py
# Author:      Robin Dunn
#
# Created:     19-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "taskbar"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxTaskBarIconEvent",
           "wxTaskBarIcon",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wx/taskbar.h>')

    c = module.find('wxTaskBarIconEvent')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_TASKBAR_MOVE = wx.PyEventBinder (         wxEVT_TASKBAR_MOVE )
        EVT_TASKBAR_LEFT_DOWN = wx.PyEventBinder (    wxEVT_TASKBAR_LEFT_DOWN )
        EVT_TASKBAR_LEFT_UP = wx.PyEventBinder (      wxEVT_TASKBAR_LEFT_UP )
        EVT_TASKBAR_RIGHT_DOWN = wx.PyEventBinder (   wxEVT_TASKBAR_RIGHT_DOWN )
        EVT_TASKBAR_RIGHT_UP = wx.PyEventBinder (     wxEVT_TASKBAR_RIGHT_UP )
        EVT_TASKBAR_LEFT_DCLICK = wx.PyEventBinder (  wxEVT_TASKBAR_LEFT_DCLICK )
        EVT_TASKBAR_RIGHT_DCLICK = wx.PyEventBinder ( wxEVT_TASKBAR_RIGHT_DCLICK )
        EVT_TASKBAR_CLICK =  wx.PyEventBinder (       wxEVT_TASKBAR_CLICK )
        EVT_TASKBAR_BALLOON_TIMEOUT = wx.PyEventBinder ( wxEVT_TASKBAR_BALLOON_TIMEOUT )
        EVT_TASKBAR_BALLOON_CLICK = wx.PyEventBinder ( wxEVT_TASKBAR_BALLOON_CLICK )
        """)


    c = module.find('wxTaskBarIcon')
    c.mustHaveApp()
    method = c.find('CreatePopupMenu')
    method.ignore(False)
    method.transfer = True
    method.virtualCatcherCode = """\
        // VirtualCatcherCode for wxTaskBarIcon.CreatePopupMenu
        PyObject *sipResObj = sipCallMethod(0, sipMethod, "");
        if (!sipResObj || sipParseResult(0, sipMethod, sipResObj, "H0", sipType_wxMenu, &sipRes) < 0)
            PyErr_Print();
        if (sipRes) {
            sipTransferTo(sipResObj, Py_None);
        }
        """
    method = c.find('GetPopupMenu')
    method.ignore(False)


    c.find('Destroy').transferThis = True

    c.addCppMethod('bool', 'ShowBalloon', '(const wxString& title, const wxString& text,'
                                            'unsigned msec = 0, int flags = 0)',
        doc="""\
            Show a balloon notification (the icon must have been already
            initialized using SetIcon).  Only implemented for Windows.

            The ``title`` and ``text`` parameters are limited to 63 and 255
            characters respectively, ``msec`` is the timeout, in milliseconds,
            before the balloon disappears (will be clamped down to the allowed
            10-30s range by Windows if it's outside it) and ``flags`` can
            include wxICON_ERROR/INFO/WARNING to show a corresponding icon.

            Returns ``True`` if balloon was shown, ``False`` on error (incorrect
            parameters or function unsupported by OS).
            """,
        body="""\
            #ifdef __WXMSW__
                return self->ShowBalloon(*title, *text, msec, flags);
            #else
                return false;
            #endif
            """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

