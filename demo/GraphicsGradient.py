#!/usr/bin/env python

import wx
g = wx

import wx.lib.scrolledpanel as scrolled

# To test compatibility of gradients with the generic GraphicsContext classes
# uncomment this line
#import wx.lib.graphics as g

#----------------------------------------------------------------------

class GradientPanel(wx.Panel):
    """
    This panel will be painted with the gradient brush created by the
    rest of the sample.
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        # Create a simple default brush we can use until a gradient
        # brush is given to us
        self.brush = wx.WHITE_BRUSH

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.SetInitialSize((600,100))


    def DrawWithBrush(self, brush):
        self.brush = brush
        self.Refresh()


    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        gc = g.GraphicsContext.Create(dc)
        gc.SetBrush(self.brush)
        gc.SetPen(wx.Pen('black', 1))
        w, h = gc.GetSize()
        gc.DrawRectangle(0,0,w,h)



class GradientStopPanel(wx.Panel):
    """
    Contains the controls for editing each gradient stop. (Colour,
    alpha and relative position.)
    """
    def __init__(self, parent, posVal, colour=wx.BLACK, alpha=wx.ALPHA_OPAQUE):
        wx.Panel.__init__(self, parent)

        # make some widgets
        self.pos = wx.SpinCtrlDouble(self, value='%2f' % posVal, size=(65,-1),
                                     min=0.0, max=1.0, initial=posVal, inc=0.01)
        self.pos.SetToolTip(
            "A value between 0 and 1 representing the distance between (x1,y1) "
            "and (x2,y2) for this gradient stop.")
        self.clrPicker = wx.ColourPickerCtrl(self, colour=colour)
        self.clrPicker.SetToolTip("The colour for this gradient stop")
        self.minusBtn = wx.Button(self, -1, " - ", style=wx.BU_EXACTFIT)
        self.minusBtn.SetToolTip("Remove this gradient stop")

        # put them in a sizer
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.pos, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.clrPicker, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 10)
        sizer.Add(self.minusBtn, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 25)
        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.EXPAND|wx.ALL, 4)
        self.SetSizer(border)

        self.Bind(wx.EVT_BUTTON, self.OnMinusButton, self.minusBtn)


    @property
    def colour(self):
        return self.clrPicker.GetColour()

    @property
    def position(self):
        return self.pos.GetValue()


    def OnMinusButton(self, evt):
        wx.CallAfter(self.Parent.RemoveStop, self)



class TestPanel(scrolled.ScrolledPanel):
    """
    The main panel for this sample
    """
    def __init__(self, parent, log):
        self.log = log
        scrolled.ScrolledPanel.__init__(self, parent, -1)

        # make the panel that will display the gradient
        self.gpanel = GradientPanel(self)

        # and the other widgets for collecting data about the gradient
        label1 = wx.StaticText(self, -1, "Geometry")
        label1.SetFont(wx.FFont(15, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD))
        x1 = 0
        x2 = self.gpanel.Size.width
        y0 = self.gpanel.Size.height / 2
        self.x1 = wx.TextCtrl(self, value=str(x1), size=(50,-1))
        self.y1 = wx.TextCtrl(self, value=str(y0), size=(50,-1))
        self.x2 = wx.TextCtrl(self, value=str(x2), size=(50,-1))
        self.y2 = wx.TextCtrl(self, value=str(y0), size=(50,-1))

        label2 = wx.StaticText(self, -1, "Stops")
        label2.SetFont(wx.FFont(15, wx.FONTFAMILY_SWISS, wx.FONTFLAG_BOLD))
        firstStop = GradientStopPanel(self, 0.0)
        lastStop =  GradientStopPanel(self, 1.0, wx.WHITE)
        self.stops = [firstStop, lastStop]
        addStopBtn = wx.Button(self, -1, " + ", style=wx.BU_EXACTFIT)


        # bind some events
        self.Bind(wx.EVT_BUTTON, self.OnAddStop, addStopBtn)
        self.Bind(wx.EVT_SPINCTRLDOUBLE, self.OnPositionUpdated)
        self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnColourChanged)
        self.Bind(wx.EVT_TEXT, self.OnGeometryChanged)


        # do the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.gpanel)
        sizer.Add((1,15))
        sizer.Add(label1)
        sizer.Add((1, 5))

        fgs = wx.FlexGridSizer(cols=11, hgap=5, vgap=5)
        fgs.AddMany([ (wx.StaticText(self, -1, "x1:"), 0, wx.ALIGN_CENTER_VERTICAL),
                      self.x1,
                      ((5,1)),
                      (wx.StaticText(self, -1, "y1:"), 0, wx.ALIGN_CENTER_VERTICAL),
                      self.y1] )
        fgs.Add((40,1))
        fgs.AddMany([ (wx.StaticText(self, -1, "x2:"), 0, wx.ALIGN_CENTER_VERTICAL),
                      self.x2,
                      ((5,1)),
                      (wx.StaticText(self, -1, "y2:"), 0, wx.ALIGN_CENTER_VERTICAL),
                      self.y2] )
        sizer.Add(fgs, 0, wx.LEFT, 25)

        sizer.Add((1,15))
        sizer.Add(label2)
        sizer.Add((1, 5))
        self.stopSizer = wx.BoxSizer(wx.VERTICAL)
        self.stopSizer.Add(firstStop)
        self.stopSizer.Add(lastStop)
        self.stopSizer.Add(addStopBtn, 0, wx.TOP, 10)
        sizer.Add(self.stopSizer, 0, wx.LEFT, 25)

        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.EXPAND|wx.ALL, 15)
        self.SetSizer(border)

        self.SetLimits()
        self.UpdateBrush()

        self.SetupScrolling()

    def RemoveStop(self, stop):
        self.stops.remove(stop)
        stop.Destroy()
        self.Layout()
        self.SetLimits()
        self.UpdateBrush()
        self.SetupScrolling()


    def OnAddStop(self, evt):
        newstop = GradientStopPanel(self, 1.0)
        self.stopSizer.Insert(len(self.stops), newstop)
        self.stops.append(newstop)
        self.Layout()
        self.SetLimits()
        self.UpdateBrush()
        self.SetupScrolling()


    def OnPositionUpdated(self, evt):
        # called when any of the spinctrls in the nested panels are updated
        self.SetLimits()
        self.UpdateBrush()


    def OnColourChanged(self, evt):
        # called when any of the color pickers are updated
        self.UpdateBrush()


    def OnGeometryChanged(self, evt):
        # called for changes to x1,y1 or x2,y2
        self.UpdateBrush()


    def SetLimits(self):
        # Tweak the panels in self.stops to set limits on the allowed
        # positions, and to disable those that should not be changed or
        # removed.
        first = self.stops[0]
        last = self.stops[-1]

        first.pos.Disable()
        first.minusBtn.Disable()
        last.pos.Disable()
        last.minusBtn.Disable()

        for idx in range(1, len(self.stops)-1):
            prev = self.stops[idx-1]
            next = self.stops[idx+1]
            stop = self.stops[idx]

            stop.pos.SetMin(prev.position)
            stop.pos.SetMax(next.position)
            stop.pos.Enable()
            stop.minusBtn.Enable()


    def UpdateBrush(self):
        """
        This is where the magic happens. We convert all the values from the
        widgets on this panel into a collection of gradient stops and then
        create a brush from them, and finally, ask the display panel to
        repaint itself with that new brush.
        """
        def floatOrZero(value):
            try:
                return float(value)
            except ValueError:
                return 0.0

        x1 = floatOrZero(self.x1.Value)
        y1 = floatOrZero(self.y1.Value)
        x2 = floatOrZero(self.x2.Value)
        y2 = floatOrZero(self.y2.Value)

        gstops = g.GraphicsGradientStops()
        gstops.SetStartColour(self.stops[0].colour)
        gstops.SetEndColour(self.stops[-1].colour)
        for s in self.stops[1:-1]:
            gs = g.GraphicsGradientStop(s.colour, s.position)
            gstops.Add(gs)

        ctx = g.GraphicsContext.Create()
        brush = ctx.CreateLinearGradientBrush(x1,y1, x2,y2, gstops)
        self.gpanel.DrawWithBrush(brush)



#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center> Gradients on a GraphicsContext </center></h2>

Multi-stop gradients can be used as fills in a wx.GraphicsContext.
This sample shows how to use the GraphicsGradientStops class to
accomplish this and allows the user to experiment with gradients.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

