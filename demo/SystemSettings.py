#!/usr/bin/env python
###############################################################################
# Name: SystemSettingsDemo.py                                                 #
# Purpose: SystemSettings Test and Demo File                                  #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2009 Cody Precord <staff@editra.org>                         #
# Licence: wxWindows Licence                                                  #
###############################################################################

"""
<b>wx.SystemSettings</b>:

<p>Allows the application to ask for details about the system.</p>

<p>This can include settings such as standard colours, fonts, and user interface
element sizes.</p>

"""

__author__ = "Cody Precord <cprecord@editra.org>"

#-----------------------------------------------------------------------------#
# Imports
import os
import sys
import wx
import wx.lib.scrolledpanel as scrolled

#-----------------------------------------------------------------------------#

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent)

        # Attributes
        self.log = log
        self._nb = wx.Notebook(self)

        # Setup
        panel1 = ScrolledWrapper(self._nb, SysColorPanel, self.log)
        self._nb.AddPage(panel1, "System Colors")
        panel2 = ScrolledWrapper(self._nb, SysFontPanel, self.log)
        self._nb.AddPage(panel2, "System Fonts")
        panel3 = ScrolledWrapper(self._nb, SysMetricPanel, self.log)
        self._nb.AddPage(panel3, "System Metrics")
        panel4 = ScrolledWrapper(self._nb, SysFeaturePanel, self.log)
        self._nb.AddPage(panel4, "System Features")

        # Layout
        self.__DoLayout()

    def __DoLayout(self):
        """Layout the panel"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._nb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

#----------------------------------------------------------------------

class SysPanelBase(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent)#, size=(500, 500))

        # Attributes
        self.log = log
        self._vals = list()

        ## Event Handlers
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SCROLLWIN, self.OnScroll)


    def DoGetBestSize(self):
        """Return the best size for this panel"""
        maxw = 0
        for vals in self._vals:
            extent = self.GetTextExtent(vals)[0]
            if extent > maxw:
                maxw = extent

        self._maxw = maxw
        maxw += 75
        maxh = (len(self._vals) + 1) * 22
        return (maxw, maxh)

    def SetupPaintDC(self, dc):
        """Paint the screen
        @param dc: paint DC

        """
        dc.SetFont(self.GetFont())
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.Clear()
        dc.DrawRectangle(self.GetClientRect())

        dc.SetPen(wx.BLACK_PEN)
        dc.SetTextForeground(wx.BLACK)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        evt.Skip()

    def OnSize(self, evt):
        self.Refresh()
        evt.Skip()

    def OnScroll(self, evt):
        self.Refresh()
        evt.Skip()

    def OnErase(self, evt):
        pass

#----------------------------------------------------------------------

class SysColorPanel(SysPanelBase):
    def __init__(self, parent, log):
        SysPanelBase.__init__(self, parent, log)

        # Attributes:
        self._box = (50, 15) # Color box dimensions
        self._maxw = 0
        self._vals = [ color for color in dir(wx)
                       if color.startswith('SYS_COLOUR_') and
                       color != 'SYS_COLOUR_MAX' ]

    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDCFactory(self)
        self.SetupPaintDC(dc)

        # Draw a sample box for each system color
        nextx = 10
        nexty = 10
        column = 0
        row_count = 0
        for val in self._vals:
            syscolor = wx.SystemSettings.GetColour(getattr(wx, val))
            dc.SetBrush(wx.Brush(syscolor))

            # Draw label
            dc.DrawText(val, nextx, nexty)

            # Calculate box position
            nextx += self._maxw + 8
            dc.DrawRectangle(nextx, nexty, self._box[0], self._box[1])

            nextx = 10
            nexty += 20

#----------------------------------------------------------------------

class SysFontPanel(SysPanelBase):
    def __init__(self, parent, log):
        SysPanelBase.__init__(self, parent, log)

        # Attributes:
        self._maxw = 0
        self._vals = ['SYS_ANSI_FIXED_FONT',
                      'SYS_ANSI_VAR_FONT',
                      'SYS_DEFAULT_GUI_FONT',
                      'SYS_DEVICE_DEFAULT_FONT',
                      # 'SYS_ICONTITLE_FONT',
                      'SYS_OEM_FIXED_FONT',
                      # 'SYS_SYSTEM_FIXED_FONT',
                      'SYS_SYSTEM_FONT'
                      ]


    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDCFactory(self)
        self.SetupPaintDC(dc)

        # Draw a sample box for each system color
        nextx = 10
        nexty = 10
        column = 0
        row_count = 0
        for val in self._vals:
            dc.SetFont(self.GetFont())
            sysfont = wx.SystemSettings.GetFont(getattr(wx, val))

            # Draw label
            dc.DrawText(val, nextx, nexty)

            # Calculate box position
            nextx += self._maxw + 8
            dc.SetFont(sysfont)
            dc.DrawText(sysfont.GetFaceName(), nextx, nexty)

            nextx = 10
            nexty += 20

#----------------------------------------------------------------------

class SysMetricPanel(SysPanelBase):
    def __init__(self, parent, log):
        SysPanelBase.__init__(self, parent, log)

        # Attributes:
        self._maxw = 0
        self._vals = ['SYS_BORDER_X', 'SYS_BORDER_Y', 'SYS_CAPTION_Y',
                      'SYS_CURSOR_X', 'SYS_CURSOR_Y', 'SYS_DCLICK_X',
                      'SYS_DCLICK_Y', 'SYS_DRAG_X', 'SYS_DRAG_Y',
                      'SYS_EDGE_X', 'SYS_EDGE_Y', 'SYS_FRAMESIZE_X',
                      'SYS_FRAMESIZE_Y', 'SYS_HSCROLL_ARROW_X',
                      'SYS_HSCROLL_ARROW_Y', 'SYS_HSCROLL_Y', 'SYS_HTHUMB_X',
                      'SYS_ICONSPACING_X', 'SYS_ICONSPACING_Y', 'SYS_ICON_X',
                      'SYS_ICON_Y', 'SYS_MENU_Y', 'SYS_SCREEN_X',
                      'SYS_SCREEN_Y', 'SYS_SMALLICON_X', 'SYS_SMALLICON_Y',
                      'SYS_VSCROLL_ARROW_X', 'SYS_VSCROLL_ARROW_Y',
                      'SYS_VSCROLL_X', 'SYS_VTHUMB_Y', 'SYS_WINDOWMIN_X',
                      'SYS_WINDOWMIN_Y', 'SYS_MOUSE_BUTTONS',
                      'SYS_NETWORK_PRESENT', 'SYS_PENWINDOWS_PRESENT',
                      'SYS_SHOW_SOUNDS', 'SYS_SWAP_BUTTONS']
        self._vals.sort()


    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDCFactory(self)
        self.SetupPaintDC(dc)

        # Draw a sample box for each system color
        nextx = 10
        nexty = 10
        column = 0
        row_count = 0
        for val in self._vals:
            sysmetric = wx.SystemSettings.GetMetric(getattr(wx, val))

            # Draw label
            dc.DrawText(val, nextx, nexty)

            # Calculate box position
            nextx += self._maxw + 8
            dc.DrawText(repr(sysmetric), nextx, nexty)

            nextx = 10
            nexty += 20

#----------------------------------------------------------------------

class SysFeaturePanel(SysPanelBase):
    def __init__(self, parent, log):
        SysPanelBase.__init__(self, parent, log)

        # Attributes:
        self._maxw = 0
        self._vals = ['SYS_CAN_DRAW_FRAME_DECORATIONS',
                      'SYS_CAN_ICONIZE_FRAME',
                      'SYS_TABLET_PRESENT' ]


    def OnPaint(self, evt):
        dc = wx.AutoBufferedPaintDCFactory(self)
        self.SetupPaintDC(dc)

        # Draw a sample box for each system color
        nextx = 10
        nexty = 10
        column = 0
        row_count = 0
        for val in self._vals:
            sysfeature = wx.SystemSettings.HasFeature(getattr(wx, val))

            # Draw label
            dc.DrawText(val, nextx, nexty)

            # Calculate box position
            nextx += self._maxw + 8
            dc.DrawText(repr(sysfeature), nextx, nexty)

            nextx = 10
            nexty += 20

#----------------------------------------------------------------------

class ScrolledWrapper(scrolled.ScrolledPanel):
    def __init__(self, parent, ctor, log):
        """Wrap the given window in a scrolled panel"""
        scrolled.ScrolledPanel.__init__(self, parent)

        # Attributes
        self._panel = ctor(self, log)

        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self._panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

        # Setup
        self.SetupScrolling()

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

class TestLog:
    def __init__(self):
        pass

    def write(self, msg):
        print(msg)

#----------------------------------------------------------------------

overview = __doc__

#-----------------------------------------------------------------------------#
if __name__ == '__main__':
    try:
        import sys
        import run
    except ImportError:
        app = wx.App(False)
        frame = wx.Frame(None, title="SystemSettings Demo", size=(500, 500))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(TestPanel(frame, TestLog()), 1, wx.EXPAND)
        frame.CreateStatusBar()
        frame.SetSizer(sizer)
        frame.Show()
        app.MainLoop()
    else:
        run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
