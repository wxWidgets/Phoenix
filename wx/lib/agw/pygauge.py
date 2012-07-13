# --------------------------------------------------------------------------------- #
# PYGAUGE wxPython IMPLEMENTATION
#
# Mark Reed, @ 28 Jul 2010
# Latest Revision: 17 Aug 2011, 15.00 GMT
#
# TODO List
#
# 1. Indeterminate mode (see wx.Gauge)
# 2. Vertical bar
# 3. Bitmap support (bar, background)
# 4. UpdateFunction - Pass a function to PyGauge which will be called every X 
#    milliseconds and the value will be updated to the returned value.
# 5. Currently the full gradient is drawn from 0 to value. Perhaps the gradient
#    should be drawn from 0 to range and clipped at 0 to value.
# 6. Add a label? 
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To The:
#
# wxPython Mailing List!!!
#
# End Of Comments
# --------------------------------------------------------------------------------- #

"""
:class:`PyGauge` is a generic :class:`Gauge` implementation.


Description
===========

:class:`PyGauge` supports the determinate mode functions as :class:`Gauge` and adds an meth:~PyGauge.Update` function
which takes a value and a time parameter. The `value` is added to the current value over 
a period of `time` milliseconds.


Usage
=====

Usage example::

    import wx
    import wx.lib.agw.pygauge as PG

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "PyGauge Demo")

            panel = wx.Panel(self)
            
            gauge1 = PG.PyGauge(panel, -1, size=(100, 25), style=wx.GA_HORIZONTAL)
            gauge1.SetValue(80)
            gauge1.SetBackgroundColour(wx.WHITE)
            gauge1.SetBorderColor(wx.BLACK)
            
            gauge2 = PG.PyGauge(panel, -1, size=(100, 25), style=wx.GA_HORIZONTAL)
            gauge2.SetValue([20, 80])
            gauge2.SetBarColor([wx.Colour(162, 255, 178), wx.Colour(159, 176, 255)])
            gauge2.SetBackgroundColour(wx.WHITE)
            gauge2.SetBorderColor(wx.BLACK)
            gauge2.SetBorderPadding(2)
            gauge2.Update([30, 0], 2000)
            
            gauge3 = PG.PyGauge(panel, -1, size=(100, 25), style=wx.GA_HORIZONTAL)
            gauge3.SetValue(50)
            gauge3.SetBarColor(wx.GREEN)
            gauge3.SetBackgroundColour(wx.WHITE)
            gauge3.SetBorderColor(wx.BLACK)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(gauge1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 20)
            sizer.Add(gauge2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 20)
            sizer.Add(gauge3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 20)
        
            panel.SetSizer(sizer)
            sizer.Layout()


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()


Supported Platforms
===================

:class:`PyGauge` has been tested on the following platforms:
  * Windows (Windows XP);
  

License And Version
===================

:class:`PyGauge` is distributed under the wxPython license.

:class:`PyGauge` has been kindly contributed to the AGW library by Mark Reed.

Latest Revision: Andrea Gavana @ 17 Aug 2011, 15.00 GMT

Version 0.1

"""

import wx
import copy


class PyGauge(wx.PyWindow):
    """ 
    This class provides a visual alternative for :class:`Gauge`. It currently 
    only support determinate mode (see :meth:`PyGauge.SetValue() <PyGauge.SetValue>` and
    :meth:`PyGauge.SetRange() <PyGauge.SetRange>`).
    """
    
    def __init__(self, parent, id=wx.ID_ANY, range=100, pos=wx.DefaultPosition,
                 size=(-1,30), style=0):
        """
        Default class constructor.

        :param `parent`: parent window. Must not be ``None``;
        :param `id`: window identifier. A value of -1 indicates a default value;
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform;
        :param `style`: the underlying :class:`PyWindow` window style.
        """

        wx.PyWindow.__init__(self, parent, id, pos, size, style)
        
        self._size = size
        
        self._border_colour = None
        self._barColour    = self._barColourSorted   = [wx.Colour(212,228,255)]
        self._barGradient  = self._barGradientSorted = None
        
        self._border_padding = 0
        self._range = range
        self._value = [0]
        self._valueSorted = [0]
        
        self._timerId = wx.NewId()
        self._timer = None
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        
        
    def DoGetBestSize(self):
        """
        Gets the size which best suits :class:`PyGauge`: for a control, it would be
        the minimal size which doesn't truncate the control, for a panel - the
        same size as it would have after a call to `Fit()`.

        :note: Overridden from :class:`PyWindow`.        
        """
        
        return wx.Size(self._size[0], self._size[1])
       
        
    def GetBorderColour(self):
        """ Returns the :class:`PyGauge` border colour. """
        
        return self._border_colour

    
    def SetBorderColour(self, colour):
        """
        Sets the :class:`PyGauge` border colour.

        :param `colour`: an instance of :class:`Colour`.
        """
        
        self._border_colour = colour
        
    SetBorderColor = SetBorderColour
    GetBorderColor = GetBorderColour
    

    def GetBarColour(self):
        """ Returns the :class:`PyGauge` main bar colour. """

        return self._barColour[0]
    

    def SetBarColour(self, colour):
        """
        Sets the :class:`PyGauge` main bar colour.

        :param `colour`: an instance of :class:`Colour`.
        """

        if type(colour) != type([]):
            self._barColour = [colour]
        else:
            self._barColour = list(colour)
            
        self.SortForDisplay() 
        
    SetBarColor = SetBarColour
    GetBarColor = GetBarColour
    
    
    def GetBarGradient(self):
        """ Returns a tuple containing the gradient start and end colours. """
       
        if self._barGradient == None:
            return None 
        
        return self._barGradient[0]

    
    def SetBarGradient(self, gradient):
        """ 
        Sets the bar gradient. 
       
        :param `gradient`: a tuple containing the gradient start and end colours.

        :note: This overrides the bar colour previously set with :meth:`PyGauge.SetBarColour`.        
        """
        
        if type(gradient) != type([]):
            self._barGradient = [gradient]
        else:
            self._barGradient = list(gradient)
            
        self.SortForDisplay() 
        
        
    def GetBorderPadding(self):
        """ Gets the border padding. """
        
        return self._border_padding
    

    def SetBorderPadding(self, padding):
        """ 
        Sets the border padding.
       
        :param `padding`: pixels between the border and the progress bar.
        """
        
        self._border_padding = padding
        
        
    def GetRange(self):
        """ Returns the maximum value of the gauge. """
        
        return self._range
    

    def SetRange(self, range):
        """ 
        Sets the range of the gauge. The gauge length is its 
        value as a proportion of the range.
        
        :param `range`: The maximum value of the gauge.
        """

        if range <= 0:
            raise Exception("ERROR:\n Gauge range must be greater than 0.")
        
        self._range = range
        
        
    def GetValue(self):
        """ Returns the current position of the gauge. """
        
        return self._value[0]
    

    def SetValue(self, value):
        """
        Sets the current position of the gauge.

        :param `value`: an integer specifying the current position of the gauge.
        """
        
        if type(value) != type([]):
            self._value = [value]
        else:
            self._value = list(value)
            
        self.SortForDisplay()
      
        for v in self._value:
            if v < 0 or v > self._range:
                raise Exception("ERROR:\n Gauge value must be between 0 and its range.")
        
        
    def OnEraseBackground(self, event):
        """
        Handles the ``wx.EVT_ERASE_BACKGROUND`` event for :class:`PyGauge`.

        :param `event`: a :class:`EraseEvent` event to be processed.

        :note: This method is intentionally empty to reduce flicker.        
        """

        pass


    def OnPaint(self, event):
        """
        Handles the ``wx.EVT_PAINT`` event for :class:`PyGauge`.

        :param `event`: a :class:`PaintEvent` event to be processed.
        """

        dc = wx.BufferedPaintDC(self)
        rect = self.GetClientRect()
        
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        colour = self.GetBackgroundColour()
        dc.SetBrush(wx.Brush(colour))
        dc.SetPen(wx.Pen(colour))
        dc.DrawRectangleRect(rect)
        
        
        if self._border_colour:
            dc.SetPen(wx.Pen(self.GetBorderColour()))
            dc.DrawRectangleRect(rect)
            pad = 1 + self.GetBorderPadding()
            rect.Deflate(pad,pad)


        if self.GetBarGradient():
            for i, gradient in enumerate(self._barGradientSorted):
                c1,c2 = gradient
                w = rect.width * (float(self._valueSorted[i]) / self._range)
                r = copy.copy(rect)
                r.width = w 
                dc.GradientFillLinear(r, c1, c2, wx.EAST)
        else:       
            for i, colour in enumerate(self._barColourSorted):
                dc.SetBrush(wx.Brush(colour))
                dc.SetPen(wx.Pen(colour))
                w = rect.width * (float(self._valueSorted[i]) / self._range)
                r = copy.copy(rect)
                r.width = w 
                dc.DrawRectangleRect(r)

        
    def OnTimer(self,event):
        """
        Handles the ``wx.EVT_TIMER`` event for :class:`PyGauge`.

        :param `event`: a :class:`TimerEvent` event to be processed.
        """
        
        if self._timerId == event.GetId():
            stop_timer = True
            for i, v in enumerate(self._value):
                self._value[i] += self._update_step[i]
                
                if self._update_step[i] > 0:
                    if self._value[i] > self._update_value[i]:
                        self._value[i] = self._update_value[i]
                    else: stop_timer = False
                else:
                    if self._value[i] < self._update_value[i]:
                        self._value[i] = self._update_value[i]
                    else: stop_timer = False
                    
            if stop_timer:
                self._timer.Stop()
                    
            self.SortForDisplay()
                        
            self.Refresh()
                
        
    def Update(self, value, time=0):
        """
        Update the gauge by adding `value` to it over `time` milliseconds. The `time` parameter
        **must** be a multiple of 50 milliseconds.

        :param `value`: The value to be added to the gauge;
        :param `time`: The length of time in milliseconds that it will take to move the gauge.
        """
       
        if type(value) != type([]):
            value = [value]
             
        if len(value) != len(self._value):
            raise Exception("ERROR:\n len(value) != len(self.GetValue())")

        self._update_value = []
        self._update_step  = []
        for i, v in enumerate(self._value):
            if value[i]+v <= 0 or value[i]+v > self._range:
                raise Exception("ERROR:\n Gauge value must be between 0 and its range. ")
        
            self._update_value.append(value[i] + v)
            self._update_step.append(float(value[i])/(time/50))
            
        #print self._update_

        if not self._timer:       
            self._timer = wx.Timer(self, self._timerId)
            
        self._timer.Start(100)

        
    def SortForDisplay(self):
        """ Internal method which sorts things so we draw the longest bar first. """
        
        if self.GetBarGradient():
            tmp = sorted(zip(self._value,self._barGradient)); tmp.reverse()
            a,b = zip(*tmp)
            self._valueSorted       = list(a)
            self._barGradientSorted = list(b)
        else:
            tmp = sorted(zip(self._value,self._barColour)); tmp.reverse()
            a,b = zip(*tmp)
            self._valueSorted     = list(a)
            self._barColourSorted = list(b)

