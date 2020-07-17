#----------------------------------------------------------------------------
# Name:        wx.lib.mixins.inspection
# Purpose:     A mix-in class that can add PyCrust-based inspection of the
#              app's widgets and sizers.
#
# Author:      Robin Dunn
#
# Created:     21-Nov-2006
# Copyright:   (c) 2006-2020 by Total Control Software
# Licence:     wxWindows license
#
# Tags: phoenix-port, documented, unittest
#----------------------------------------------------------------------------
#
# NOTE: This class was originally based on ideas sent to the
# wxPython-users mail list by Dan Eloff.
"""
This module provides the :class:`~lib.mixins.inspection.InspectableApp` and
:class:`~lib.mixins.inspection.InspectionMixin` which make it easy to use the Widget
Inspection Tool (WIT).


Description
===========

The Widget Inspection Tool (WIT) is very useful debugging tool provided with
wxPython, especially useful to debug layout issues when using :class:`wx.Sizer`.

The :class:`InspectableApp` is a "pre-mixed" :class:`App` and the
:class:`InspectionMixin` allows you to mix it with your custom :class:`App`
class.


Usage
=====

The following samples assume the default key sequence (*ctrl-alt-i*) to start
the WIT, additional information can be found on the following wiki page.

http://wiki.wxpython.org/Widget_Inspection_Tool

InspectableApp usage::

    import wx
    import wx.lib.sized_controls as sc
    import wx.lib.mixins.inspection as wit

    app = wit.InspectableApp()

    frame = sc.SizedFrame(None, -1, "WIT InspectableApp")

    pane = frame.GetContentsPane()
    pane.SetSizerType("horizontal")

    b1 = wx.Button(pane, wx.ID_ANY)
    t1 = wx.TextCtrl(pane, -1)
    t1.SetSizerProps(expand=True)

    frame.Show()

    app.MainLoop()


InspectionMixin usage::

    import wx
    import wx.lib.sized_controls as sc
    import wx.lib.mixins.inspection as wit

    class MyApp(wx.App, wit.InspectionMixin):
        def OnInit(self):
            self.Init()  # initialize the inspection tool
            return True

    app = MyApp()

    frame = sc.SizedFrame(None, -1, "WIT InspectionMixin")

    pane = frame.GetContentsPane()
    pane.SetSizerType("horizontal")

    b1 = wx.Button(pane, wx.ID_ANY)
    t1 = wx.TextCtrl(pane, -1)
    t1.SetSizerProps(expand=True)

    frame.Show()

    app.MainLoop()

"""


import wx
from wx.lib.inspection import InspectionTool


#----------------------------------------------------------------------------

class InspectionMixin(object):
    """
    This class is intended to be used as a mix-in with the :class:`App`.
    When used it will add the ability to popup a
    :class:`~lib.inspection.InspectionFrame` window
    where the widget under the mouse cursor will be selected in the tree and
    loaded into the shell's namespace as 'obj'.  The default key sequence to
    activate the inspector is Ctrl-Alt-I (or Cmd-Alt-I on Mac) but this can be
    changed via parameters to the `Init` method, or the application can call
    :meth:`~lib.mixins.inspection.InspectionMixin.ShowInspectionTool` from other
    event handlers if desired.

    To use this class simply derive a class from :class:`App` and
    :class:`InspectionMixin` and then call the
    :meth:`InspectionMixin.Init` method from the app's
    :meth:`AppConsole.OnInit` method.
    """
    def InitInspection(self, pos=wx.DefaultPosition, size=wx.Size(850,700),
                       config=None, locals=None,
                       alt=True, cmd=True, shift=False, keyCode=ord('I')):
        """
        Make the event binding that will activate the InspectionFrame window.

        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `config`: A :class:`Config` object to be used to store layout
            and other info to when the inspection frame is closed.
            This info will be restored the next time the inspection
            frame is used.
        :param `locals`: A dictionary of names to be added to the PyCrust
            namespace.
        :param boolean `alt`: use alt in the short cut sequence
        :param boolean `cmd`: use ctrl/cmd in the short cut sequence
        :param boolean `shift`: use shift in the short cut sequence
        :param string `keyCode`: the key code for the short cut sequence

        """
        self.Bind(wx.EVT_KEY_DOWN, self._OnKeyPress)
        self._alt = alt
        self._cmd = cmd
        self._shift = shift
        self._keyCode = keyCode
        InspectionTool().Init(pos, size, config, locals, self)

    def _OnKeyPress(self, evt):
        """
        Event handler, check for our hot-key.  Normally it is
        Ctrl-Alt-I but that can be changed by what is passed to the
        Init method.
        """
        if evt.AltDown() == self._alt  and \
               evt.CmdDown() == self._cmd and \
               evt.ShiftDown() == self._shift and \
               evt.GetKeyCode() == self._keyCode:
            self.ShowInspectionTool()
        else:
            evt.Skip()

    Init = InitInspection  # compatibility alias

    def ShowInspectionTool(self):
        """
        Show the Inspection tool, creating it if necessary, setting it
        to display the widget under the cursor.
        """
        # get the current widget under the mouse
        wnd, pt = wx.FindWindowAtPointer()
        InspectionTool().Show(wnd)


#---------------------------------------------------------------------------

class InspectableApp(wx.App, InspectionMixin):
    """
    A simple mix of :class:`App` and :class:`InspectionMixin` that can be used
    stand-alone.
    """

    def OnInit(self):
        self.InitInspection()
        return True

#---------------------------------------------------------------------------

