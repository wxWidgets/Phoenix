#!/usr/bin/env python

import wx
import wx.stc as stc


demoText = """\
wx.MouseState

In this demo we will replicate the styled text ctrl's mousewheel functionality
and also show how to add a new feature...
Drum roll please.
Shift+MouseWheel = Horizontal Scrolling
Alt+MouseWheel = Hyper Scrolling

ba dump dump chshshshshshshsh%s
bada-boom! ...
...
..
%s
%s
""" % ('sh' * 300, '.\n' * 50, ('Hyper Scroll or Horizontal Scroll... ' * 50 + '\n') * 300)


class MySTC(stc.StyledTextCtrl):
    def __init__(self, parent, id, log):
        stc.StyledTextCtrl.__init__(self, parent, id)
        self.log = log

        self.Bind(wx.EVT_MOUSEWHEEL, self.OnMouseWheel)

    def OnMouseWheel(self, event):
        """
        wx.EVT_MOUSEWHEEL
        Allow Shift + MouseWheel Horizontal Scrolling
        """
        xoffset = self.GetXOffset()
        wr = event.GetWheelRotation()

        ms = wx.GetMouseState()
        ctrlDown = ms.ControlDown()
        shiftDown = ms.ShiftDown()
        altDown = ms.AltDown()

        print('GetWheelRotation: ', wr)
        #negative/down Ex: -120
        #positive/up Ex: 120

        # print('GetWheelDelta: ', event.GetWheelDelta())
        # print('GetXOffset: ', xoffset)
        if xoffset < 0:  # Dont scroll back past zero position
            self.SetXOffset(0)
            self.Refresh()
            return

        #-- Alt + MouseWheel = Hyper Scrolling Vertically
        #Imitate hyperscrolling functionality with a clickwheel only style mouse
        if altDown and wr < 0 and not shiftDown and not ctrlDown:
            while wx.GetKeyState(wx.WXK_ALT):
                wx.MilliSleep(1)
                self.LineScroll(0, 1)
                # print('Alt + WheelDown')
            return
        elif altDown and wr > 0 and not shiftDown and not ctrlDown:
            while wx.GetKeyState(wx.WXK_ALT):
                wx.MilliSleep(1)
                self.LineScroll(0, -1)
                # print('Alt + WheelUp')
            return

        #-- Shift + MouseWheel = Scroll Horizontally
        if shiftDown and wr < 0 and not altDown and not ctrlDown:
            self.SetXOffset(xoffset + 30)
            # print('Shift + WheelDown')
            return
        elif shiftDown and wr > 0 and not altDown and not ctrlDown:
            if not xoffset <= 0:
                self.SetXOffset(xoffset - 30)
                # print('Shift + WheelUp')
                return
            else:
                return

        #-- Ctrl + MouseWheel = Zoom
        # Duplicate Default stc ctrl zooming behavior to bypass
        # (MouseWheel not working after a undetermined amount of time)BUG
        if ctrlDown and wr < 0 and not altDown and not shiftDown:
            self.SetZoom(self.GetZoom() - 1)
            # print('Ctrl + WheelDown')
            return
        elif ctrlDown and wr > 0 and not altDown and not shiftDown:
            self.SetZoom(self.GetZoom() + 1)
            # print('Ctrl + WheelUp')
            return

        #-- MouseWheel = Scroll Vertically
        # Duplicate Default stc scrolling behavior to bypass
        # (MouseWheel not working after a undetermined amount of time)BUG
        elif wr < 0:
            self.LineScroll(0, 3)
            # print('WheelDown')
            return
        elif wr > 0:
            self.LineScroll(0, -3)
            # print('WheelUp')
            return


#----------------------------------------------------------------------

_USE_PANEL = 1


def runTest(frame, nb, log):
    if not _USE_PANEL:
        ed = p = MySTC(nb, -1, log)

    else:
        p = wx.Panel(nb, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
        ed = MySTC(p, -1, log)
        s = wx.BoxSizer(wx.HORIZONTAL)
        s.Add(ed, 1, wx.EXPAND)
        p.SetSizer(s)
        p.SetAutoLayout(True)

    ed.SetText(demoText)
    ed.EmptyUndoBuffer()

    return p


#----------------------------------------------------------------------


overview = """\
wx.MouseState

Represents the mouse state.

This class is used as a base class by MouseEvent and so its
methods may be used to obtain information about the mouse state
for the mouse events. It also inherits from KeyboardState and so
carries information about the keyboard state and not only the mouse one.
"""


if __name__ == '__main__':
    import sys
    import os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
