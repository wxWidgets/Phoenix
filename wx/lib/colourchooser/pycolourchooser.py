"""
PyColourChooser
Copyright (C) 2002 Michael Gilfix <mgilfix@eecs.tufts.edu>

This file is part of PyColourChooser.

This version of PyColourChooser is open source; you can redistribute it
and/or modify it under the licensed terms.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
"""

from __future__ import absolute_import

# 12/14/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o 2.5 compatibility update.
#
# 12/21/2003 - Jeff Grimmett (grimmtooth@softhome.net)
#
# o wxPyColorChooser -> PyColorChooser
# o wxPyColourChooser -> PyColourChooser
# o Added wx.InitAllImageHandlers() to test code since
#   that's where it belongs.
#
# Tags:     phoenix-port

import  wx
import wx.lib.newevent as newevent

from . import  pycolourbox
from . import  pypalette
from . import  pycolourslider
import  colorsys
from . import  intl

from .intl import _ # _

ColourChangedEventBase, EVT_COLOUR_CHANGED = newevent.NewEvent()

class ColourChangedEvent(ColourChangedEventBase):
    """Adds GetColour()/GetValue() for compatibility with ColourPickerCtrl and colourselect"""
    def __init__(self, newColour):
        super(ColourChangedEvent, self).__init__(newColour = newColour)

    def GetColour(self):
        return self.newColour

    def GetValue(self):
        return self.newColour

class PyColourChooser(wx.Panel):
    """A Pure-Python implementation of the colour chooser dialog.

    The PyColourChooser is a pure python implementation of the colour
    chooser dialog. It's useful for embedding the colour choosing functionality
    inside other widgets, when the pop-up dialog is undesirable. It can also
    be used as a drop-in replacement on the GTK platform, as the native
    dialog is kind of ugly.
    """

    colour_names = [
        'ORANGE',
        'GOLDENROD',
        'WHEAT',
        'SPRING GREEN',
        'SKY BLUE',
        'SLATE BLUE',
        'MEDIUM VIOLET RED',
        'PURPLE',

        'RED',
        'YELLOW',
        'MEDIUM SPRING GREEN',
        'PALE GREEN',
        'CYAN',
        'LIGHT STEEL BLUE',
        'ORCHID',
        'LIGHT MAGENTA',

        'BROWN',
        'YELLOW',
        'GREEN',
        'CADET BLUE',
        'MEDIUM BLUE',
        'MAGENTA',
        'MAROON',
        'ORANGE RED',

        'FIREBRICK',
        'CORAL',
        'FOREST GREEN',
        'AQUAMARINE',
        'BLUE',
        'NAVY',
        'THISTLE',
        'MEDIUM VIOLET RED',

        'INDIAN RED',
        'GOLD',
        'MEDIUM SEA GREEN',
        'MEDIUM BLUE',
        'MIDNIGHT BLUE',
        'GREY',
        'PURPLE',
        'KHAKI',

        'BLACK',
        'MEDIUM FOREST GREEN',
        'KHAKI',
        'DARK GREY',
        'SEA GREEN',
        'LIGHT GREY',
        'MEDIUM SLATE BLUE',
        'WHITE',
    ]

    # Generate the custom colours. These colours are shared across
    # all instances of the colour chooser
    NO_CUSTOM_COLOURS = 16
    custom_colours = [ (wx.WHITE,
                        pycolourslider.PyColourSlider.HEIGHT / 2)
                     ] * NO_CUSTOM_COLOURS
    last_custom = 0

    idADD_CUSTOM = wx.NewIdRef()
    idSCROLL     = wx.NewIdRef()

    def __init__(self, parent, id):
        """Creates an instance of the colour chooser. Note that it is best to
        accept the given size of the colour chooser as it is currently not
        resizeable."""
        wx.Panel.__init__(self, parent, id)

        self.basic_label = wx.StaticText(self, -1, _("Basic Colours:"))
        self.custom_label = wx.StaticText(self, -1, _("Custom Colours:"))
        self.add_button = wx.Button(self, self.idADD_CUSTOM, _("Add to Custom Colours"))

        self.Bind(wx.EVT_BUTTON, self.onAddCustom, self.add_button)

        # Since we're going to be constructing widgets that require some serious
        # computation, let's process any events (like redraws) right now
        wx.Yield()

        # Create the basic colours palette
        self.colour_boxs = [ ]
        colour_grid = wx.GridSizer(rows=6, cols=8, vgap=0, hgap=0)
        for name in self.colour_names:
            new_id = wx.NewIdRef()
            box = pycolourbox.PyColourBox(self, new_id)

            box.GetColourBox().Bind(wx.EVT_LEFT_DOWN, lambda x, b=box: self.onBasicClick(x, b))

            self.colour_boxs.append(box)
            colour_grid.Add(box, 0, wx.EXPAND)

        # Create the custom colours palette
        self.custom_boxs = [ ]
        custom_grid = wx.GridSizer(rows=2, cols=8, vgap=0, hgap=0)
        for wxcolour, slidepos in self.custom_colours:
            new_id = wx.NewIdRef()
            custom = pycolourbox.PyColourBox(self, new_id)

            custom.GetColourBox().Bind(wx.EVT_LEFT_DOWN, lambda x, b=custom: self.onCustomClick(x, b))

            custom.SetColour(wxcolour)
            custom_grid.Add(custom, 0, wx.EXPAND)
            self.custom_boxs.append(custom)

        csizer = wx.BoxSizer(wx.VERTICAL)
        csizer.Add((1, 25))
        csizer.Add(self.basic_label, 0, wx.EXPAND)
        csizer.Add((1, 5))
        csizer.Add(colour_grid, 0, wx.EXPAND)
        csizer.Add((1, 25))
        csizer.Add(self.custom_label, 0, wx.EXPAND)
        csizer.Add((1, 5))
        csizer.Add(custom_grid, 0, wx.EXPAND)
        csizer.Add((1, 5))
        csizer.Add(self.add_button, 0, wx.EXPAND)

        self.palette = pypalette.PyPalette(self, -1)
        self.colour_slider = pycolourslider.PyColourSlider(self, -1)
        self.colour_slider.Bind(wx.EVT_LEFT_DOWN, self.onSliderDown)
        self.colour_slider.Bind(wx.EVT_LEFT_UP, self.onSliderUp)
        self.colour_slider.Bind(wx.EVT_MOTION, self.onSliderMotion)
        self.slider = wx.Slider(
                        self, self.idSCROLL, 86, 0, self.colour_slider.HEIGHT - 1,
                        style=wx.SL_VERTICAL, size=(-1, self.colour_slider.HEIGHT)
                        )

        self.Bind(wx.EVT_COMMAND_SCROLL, self.onScroll, self.slider)
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        psizer.Add(self.palette, 0, 0)
        psizer.Add((10, 1))
        psizer.Add(self.colour_slider, 0, wx.ALIGN_CENTER_VERTICAL)
        psizer.Add(self.slider, 0, wx.ALIGN_CENTER_VERTICAL)

        # Register mouse events for dragging across the palette
        self.palette.Bind(wx.EVT_LEFT_DOWN, self.onPaletteDown)
        self.palette.Bind(wx.EVT_LEFT_UP, self.onPaletteUp)
        self.palette.Bind(wx.EVT_MOTION, self.onPaletteMotion)

        self.solid = pycolourbox.PyColourBox(self, -1, size=(75, 50))
        slabel = wx.StaticText(self, -1, _("Solid Colour"))
        ssizer = wx.BoxSizer(wx.VERTICAL)
        ssizer.Add(self.solid, 0, 0)
        ssizer.Add((1, 2))
        ssizer.Add(slabel, 0, wx.ALIGN_CENTER_HORIZONTAL)

        hlabel = wx.StaticText(self, -1, _("H:"))
        self.hentry = wx.TextCtrl(self, -1)
        self.hentry.SetSize((40, -1))
        slabel = wx.StaticText(self, -1, _("S:"))
        self.sentry = wx.TextCtrl(self, -1)
        self.sentry.SetSize((40, -1))
        vlabel = wx.StaticText(self, -1, _("V:"))
        self.ventry = wx.TextCtrl(self, -1)
        self.ventry.SetSize((40, -1))
        hsvgrid = wx.FlexGridSizer(rows=1, cols=6, vgap=2, hgap=2)
        hsvgrid.AddMany ([
            (hlabel, 0, wx.ALIGN_CENTER_VERTICAL), (self.hentry, 0, wx.FIXED_MINSIZE),
            (slabel, 0, wx.ALIGN_CENTER_VERTICAL), (self.sentry, 0, wx.FIXED_MINSIZE),
            (vlabel, 0, wx.ALIGN_CENTER_VERTICAL), (self.ventry, 0, wx.FIXED_MINSIZE),
        ])

        self.hentry.Bind(wx.EVT_KILL_FOCUS, self.onHSVKillFocus)
        self.sentry.Bind(wx.EVT_KILL_FOCUS, self.onHSVKillFocus)
        self.ventry.Bind(wx.EVT_KILL_FOCUS, self.onHSVKillFocus)

        rlabel = wx.StaticText(self, -1, _("R:"))
        self.rentry = wx.TextCtrl(self, -1)
        self.rentry.SetSize((40, -1))
        glabel = wx.StaticText(self, -1, _("G:"))
        self.gentry = wx.TextCtrl(self, -1)
        self.gentry.SetSize((40, -1))
        blabel = wx.StaticText(self, -1, _("B:"))
        self.bentry = wx.TextCtrl(self, -1)
        self.bentry.SetSize((40, -1))
        lgrid = wx.FlexGridSizer(rows=1, cols=6, vgap=2, hgap=2)
        lgrid.AddMany([
            (rlabel, 0, wx.ALIGN_CENTER_VERTICAL), (self.rentry, 0, wx.FIXED_MINSIZE),
            (glabel, 0, wx.ALIGN_CENTER_VERTICAL), (self.gentry, 0, wx.FIXED_MINSIZE),
            (blabel, 0, wx.ALIGN_CENTER_VERTICAL), (self.bentry, 0, wx.FIXED_MINSIZE),
        ])

        self.rentry.Bind(wx.EVT_KILL_FOCUS, self.onRGBKillFocus)
        self.gentry.Bind(wx.EVT_KILL_FOCUS, self.onRGBKillFocus)
        self.bentry.Bind(wx.EVT_KILL_FOCUS, self.onRGBKillFocus)

        gsizer = wx.GridSizer(rows=2, cols=1, vgap=0, hgap=0)
        gsizer.SetVGap (10)
        gsizer.SetHGap (2)
        gsizer.Add(hsvgrid, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        gsizer.Add(lgrid, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(ssizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)
        hsizer.Add(gsizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add((1, 5))
        vsizer.Add(psizer, 0, 0)
        vsizer.Add((1, 15))
        vsizer.Add(hsizer, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((5, 1))
        sizer.Add(csizer, 0, wx.EXPAND)
        sizer.Add((10, 1))
        sizer.Add(vsizer, 0, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)

        self.InitColours()
        self.UpdateColour(self.solid.GetColour())

    def InitColours(self):
        """Initializes the pre-set palette colours."""
        for i in range(len(self.colour_names)):
            colour = wx.TheColourDatabase.FindColour(self.colour_names[i])
            self.colour_boxs[i].SetColourTuple((colour.Red(),
                                                colour.Green(),
                                                colour.Blue()))

    def onBasicClick(self, event, box):
        """Highlights the selected colour box and updates the solid colour
        display and colour slider to reflect the choice."""
        if hasattr(self, '_old_custom_highlight'):
            self._old_custom_highlight.SetHighlight(False)
        if hasattr(self, '_old_colour_highlight'):
            self._old_colour_highlight.SetHighlight(False)
        box.SetHighlight(True)
        self._old_colour_highlight = box
        self.UpdateColour(box.GetColour())

    def onCustomClick(self, event, box):
        """Highlights the selected custom colour box and updates the solid
        colour display and colour slider to reflect the choice."""
        if hasattr(self, '_old_colour_highlight'):
            self._old_colour_highlight.SetHighlight(False)
        if hasattr(self, '_old_custom_highlight'):
            self._old_custom_highlight.SetHighlight(False)
        box.SetHighlight(True)
        self._old_custom_highlight = box

        # Update the colour panel and then the slider accordingly
        box_index = self.custom_boxs.index(box)
        base_colour, slidepos = self.custom_colours[box_index]
        self.UpdateColour(box.GetColour())
        self.slider.SetValue(slidepos)

    def onAddCustom(self, event):
        """Adds a custom colour to the custom colour box set. Boxes are
        chosen in a round-robin fashion, eventually overwriting previously
        added colours."""
        # Store the colour and slider position so we can restore the
        # custom colours just as they were
        self.setCustomColour(self.last_custom,
                             self.solid.GetColour(),
                             self.colour_slider.GetBaseColour(),
                             self.slider.GetValue())
        self.last_custom = (self.last_custom + 1) % self.NO_CUSTOM_COLOURS

    def setCustomColour (self, index, true_colour, base_colour, slidepos):
        """Sets the custom colour at the given index. true_colour is wxColour
        object containing the actual rgb value of the custom colour.
        base_colour (wxColour) and slidepos (int) are used to configure the
        colour slider and set everything to its original position."""
        self.custom_boxs[index].SetColour(true_colour)
        self.custom_colours[index] = (base_colour, slidepos)

    def setSliderToV(self, v):
        """Set a new HSV value for the v slider. Does not update displayed colour."""
        min = self.slider.GetMin()
        max = self.slider.GetMax()
        val = (1 - v) * max
        self.slider.SetValue(int(val))

    def getVFromSlider(self):
        """Get the current value of "V" from the v slider."""
        val = self.slider.GetValue()
        min = self.slider.GetMin()
        max = self.slider.GetMax()

        # Snap to exact min/max values
        if val == 0:
            return 1
        if val == max - 1:
            return 0

        return 1 - (val / max)

    def colourToHSV(self, colour):
        """Convert wx.Colour to hsv triplet"""
        return colorsys.rgb_to_hsv(colour.Red() / 255.0, colour.Green() / 255.0, colour.Blue() / 255.0)

    def hsvToColour(self, hsv):
        """Convert hsv triplet to wx.Colour"""
        # Allow values to go full range from 0 to 255
        r, g, b = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])

        round_tenths = lambda x: int(x + 0.5)

        r = round_tenths(r * 255.0)
        g = round_tenths(g * 255.0)
        b = round_tenths(b * 255.0)

        return wx.Colour(r, g, b)

    def getColourFromControls(self):
        """
        Calculate current colour from HS box position and V slider.
        return - wx.Colour
        """
        # This allows colours to be exactly 0,0,0 or 255, 255, 255
        baseColour = self.colour_slider.GetBaseColour()
        h,s,v = self.colourToHSV(baseColour)
        v = self.getVFromSlider()
        if s < 0.04:                       # Allow pure white
            s = 0

        return self.hsvToColour((h, s, v))

    def updateDisplayColour(self, colour):
        """Update the displayed color box (solid) and send the EVT_COLOUR_CHANGED"""
        self.solid.SetColour(colour)
        evt = ColourChangedEvent(newColour=colour)
        wx.PostEvent(self, evt)

    def UpdateColour(self, colour):
        """Updates displayed colour and HSV controls with the new colour"""
        # Set the color info
        self.updateDisplayColour(colour)
        self.colour_slider.SetBaseColour(colour)
        self.colour_slider.ReDraw()

        # Update the Vslider and the HS current selection dot
        h,s,v = self.colourToHSV(colour)
        self.setSliderToV(v)

        # Convert RGB to (x,y) == (hue, saturation)

        width, height = self.palette.GetSize()
        x = width * h
        y = height * (1 - s)
        self.palette.HighlightPoint(x, y)

        self.UpdateEntries(colour)

    def UpdateEntries(self, colour):
        """Updates the color levels to display the new values."""
        # Temporary bindings
        r = colour.Red()
        g = colour.Green()
        b = colour.Blue()

        # Update the RGB entries
        self.rentry.SetValue(str(r))
        self.gentry.SetValue(str(g))
        self.bentry.SetValue(str(b))

        # Convert to HSV
        h,s,v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        self.hentry.SetValue("%.2f" % (h))
        self.sentry.SetValue("%.2f" % (s))
        self.ventry.SetValue("%.2f" % (v))

    def onColourSliderClick(self, y):
        """Shared helper for onSliderDown()/onSliderMotion()"""
        v = self.colour_slider.GetVFromClick(y)
        self.setSliderToV(v)

        # Now with the slider updated, update all controls
        colour = self.getColourFromControls()

        self.updateDisplayColour(colour)   # Update display
        self.UpdateEntries(colour)

        # We don't move on the palette...

        # width, height = self.palette.GetSize()
        # x = width * h
        # y = height * (1 - s)
        # self.palette.HighlightPoint(x, y)

    def onSliderDown(self, event):
        """Handle mouse click on the colour slider palette"""
        self.onColourSliderClick(event.GetY())
        self.colour_slider.CaptureMouse()

    def onSliderUp(self, event):
        if self.colour_slider.HasCapture():
            self.colour_slider.ReleaseMouse()

    def onSliderMotion(self, event):
        """Handle mouse-down drag on the colour slider palette"""
        if event.LeftIsDown():
            self.onColourSliderClick(event.GetY())

    def onPaletteDown(self, event):
        """Stores state that the mouse has been pressed and updates
        the selected colour values."""
        self.doPaletteClick(event.GetX(), event.GetY())

        # Prevent mouse from leaving window, so that we will also get events
        # when mouse is dragged along the edges of the rectangle.
        self.palette.CaptureMouse()

    def onPaletteUp(self, event):
        """Stores state that the mouse is no longer depressed."""
        if self.palette.HasCapture():
            self.palette.ReleaseMouse() # Must call once for each CaputreMouse()

    def onPaletteMotion(self, event):
        """Updates the colour values during mouse motion while the
        mouse button is depressed."""
        if event.LeftIsDown():
            self.doPaletteClick(event.GetX(), event.GetY())

    def onPaletteCaptureLost(self, event):
        pass # I don't think we have to call ReleaseMouse in this event

    def doPaletteClick(self, m_x, m_y):
        """Updates the colour values based on the mouse location
        over the palette."""
        # Get the colour value, combine with H slider value, and update
        colour = self.palette.GetValue(m_x, m_y)

        # Update colour, but do not move V slider
        self.colour_slider.SetBaseColour(colour)
        self.colour_slider.ReDraw()

        colour = self.getColourFromControls()

        self.updateDisplayColour(colour)   # Update display
        self.UpdateEntries(colour)

        # Highlight a fresh selected area
        self.palette.HighlightPoint(m_x, m_y)

    def onScroll(self, event):
        """Updates the display to reflect the new "Value"."""
        value = self.slider.GetValue()
        colour = self.getColourFromControls()
        self.updateDisplayColour(colour)
        self.UpdateEntries(colour)

    def getValueAsFloat(self, textctrl):
        """If you type garbage, you get, literally, nothing (0)"""
        try:
            return float(textctrl.GetValue())
        except ValueError:
            return 0

    def onHSVKillFocus(self, event):

        h = self.getValueAsFloat(self.hentry)
        s = self.getValueAsFloat(self.sentry)
        v = self.getValueAsFloat(self.ventry)

        if h > 0.9999:
            h = 0.9999
        if s > 0.9999:
            s = 0.9999
        if v > 0.9999:
            v = 0.9999

        if h < 0:
            h = 0
        if s < 0:
            s = 0
        if v < 0:
            v = 0

        colour = self.hsvToColour((h, s, v))
        self.SetValue(colour) # infinite loop?

    def onRGBKillFocus(self, event):
        r = self.getValueAsFloat(self.rentry)
        g = self.getValueAsFloat(self.gentry)
        b = self.getValueAsFloat(self.bentry)

        if r > 255:
            r = 255
        if g > 255:
            g = 255
        if b > 255:
            b = 255

        if r < 0:
            r = 0
        if g < 0:
            g = 0
        if b < 0:
            b = 0

        self.SetValue(wx.Colour((r, g, b)))

    def SetValue(self, colour):
        """Updates the colour chooser to reflect the given wxColour."""
        self.UpdateColour(colour)

    def GetValue(self):
        """Returns a wxColour object indicating the current colour choice."""
        return self.solid.GetColour()

def main():
    """Simple test display."""

    class CCTestDialog(wx.Dialog):
        def __init__(self, parent, initColour):
            super(CCTestDialog, self).__init__(parent, title="Pick A Colo(u)r")

            sizer = wx.BoxSizer(wx.VERTICAL)
            self.chooser = PyColourChooser(self, wx.ID_ANY)
            self.chooser.SetValue(initColour)
            sizer.Add(self.chooser)

            self.SetSizer(sizer)
            sizer.Fit(self)

    class CCTestFrame(wx.Frame):
        def __init__(self):
            super(CCTestFrame, self).__init__(None, -1, 'PyColourChooser Test')
            sizer = wx.BoxSizer(wx.VERTICAL)

            sizer.Add(wx.StaticText(self, label="CLICK ME"), 0, wx.CENTER)

            self.box = pycolourbox.PyColourBox(self, id=wx.ID_ANY, size=(100,100))
            sizer.Add(self.box, 0, wx.EXPAND)
            self.box.SetColour(wx.Colour((0x7f, 0x90, 0x21)))
            self.box.colour_box.Bind(wx.EVT_LEFT_DOWN, self.onClick) # should be an event. :(

            self.SetSizer(sizer)
            sizer.Fit(self)

        def onClick(self, cmdEvt):
            with CCTestDialog(self, self.box.GetColour()) as dialog:
                dialog.chooser.Bind(EVT_COLOUR_CHANGED, self.onColourChanged)
                dialog.ShowModal()
                self.box.SetColour(dialog.chooser.GetValue())

        def onColourChanged(self, event):
            self.box.SetColour(event.GetValue())

    class App(wx.App):
        def OnInit(self):
            frame = CCTestFrame()

            # Added here because that's where it's supposed to be,
            # not embedded in the library. If it's embedded in the
            # library, debug messages will be generated for duplicate
            # handlers.
            wx.InitAllImageHandlers()

            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(False)
    app.MainLoop()

if __name__ == '__main__':
    main()
