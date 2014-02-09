#----------------------------------------------------------------------
# Name:        wx.lib.progressindicator
# Purpose:     
#
# Author:      Robin Dunn
#
# Created:     22-Oct-2009
# Copyright:   (c) 2009 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------

"""
A simple gauge with a label that is suitable for use in places like a
status bar.  It can be used in either an automatic indeterminant
(pulse) mode or in determinante mode where the programmer will need to
update the position of the progress bar.  The indicator can be set to
hide itself when it is not active.
"""

import wx

#----------------------------------------------------------------------
# Supported Styles

PI_PULSEMODE = 1
PI_HIDEINACTIVE = 2

#----------------------------------------------------------------------

class ProgressIndicator(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.label = wx.StaticText(self)
        self.gauge = wx.Gauge(self, range=100,
                              style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)

        self._startCount = 0
        self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Sizer.Add(self.label, 0, wx.ALIGN_CENTER_VERTICAL)
        self.Sizer.Add(self.gauge, 1, wx.EXPAND)

        size = wx.DefaultSize
        if 'size' in kw:
            size = kw['size']
        elif len(args) >= 4:
            size=args[3] # parent, id, pos, size, style, name
            
        self.SetInitialSize(size)
        
        if self.HasFlag(PI_PULSEMODE):
            self.timer = wx.Timer(self)
            self.Bind(wx.EVT_TIMER, self.onTimer)
        if self.HasFlag(PI_HIDEINACTIVE):
            self.Hide()

            
    def __del__(self):
        if hasattr(self, 'timer'):
            self.timer.Stop()
            del self.timer

            
    def Start(self, label=None):
        """
        Show (if necessary) and begin displaying progress
        """
        self._startCount += 1
        if label is not None:
            self.SetLabel(label)
        if self.HasFlag(PI_HIDEINACTIVE):
            self.Show()
            self.Layout()            
        if self.HasFlag(PI_PULSEMODE):
            self.gauge.Pulse()
            self.timer.Start(250)
        else:
            self.gauge.SetValue(0)

            
    def Stop(self, clearLabel=False):
        """
        Stop showing progress
        """
        # Make sure Stop is called as many times as Start was. Only really
        # stop when the count reaches zero.
        if self._startCount == 0:
            return  # should be already stopped...
        self._startCount -= 1
        if self._startCount:
            return # there's still more starts than stops...
        
        if self.HasFlag(PI_HIDEINACTIVE):
            self.Hide()
            
        if self.HasFlag(PI_PULSEMODE):
            self.timer.Stop()
            
        if clearLabel:
            self.label.SetLabel("")
            
            
    def SetLabel(self, text):
        """
        Set the text displayed in the label.
        """
        self.label.SetLabel(text)
        self.Layout()
        
        
    def SetValue(self, value, label=None):
        """
        For determinante mode (non-pulse) update the progress indicator to the
        given value. For example, if the job is 45% done then pass 45 to this
        method (as long as the range is still set to 100.)
        """
        if label is not None:
            self.SetLabel(label)
        self.gauge.SetValue(value)

        
    def SetRange(self, maxval):
        """
        For determinante mode (non-pulse) set the max value that the gauge can
        be set to. Defaults to 100.
        """
        self.gauge.SetRange(maxval)
        
        
    def onTimer(self, evt):
        self.gauge.Pulse()


#----------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App(redirect=False)
    frm = wx.Frame(None, title="ProgressIndicator")
    pnl = wx.Panel(frm)
    pi1 = ProgressIndicator(pnl, pos=(20,20), size=(150,-1),
                            style=PI_HIDEINACTIVE|PI_PULSEMODE)
    
    pi2 = ProgressIndicator(pnl, pos=(20,60), size=(150,-1),
                            style=PI_HIDEINACTIVE)

    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()
    
    frm.Show()
    app.MainLoop()
    
