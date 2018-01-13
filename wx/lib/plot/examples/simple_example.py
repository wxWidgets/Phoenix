# -*- coding: utf-8 -*-
"""
A simple example showing how to use lib.plot from wxPython.

It is intended to be run as a standalone script via::

  user@host:.../site-packages/wx/lib/plot$ python examples/simple_example.py

"""
__docformat__ = "restructuredtext en"

# Third Party
import wx
from wx.lib import plot as wxplot

class PlotExample(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Example of wx.lib.plot", size=(640,480))

        # Generate some Data
        x_data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y_data = [2, 4, 6, 4, 2, 5, 6, 7, 1]

        # most items require data as a list of (x, y) pairs:
        #    [[1x, y1], [x2, y2], [x3, y3], ..., [xn, yn]]
        xy_data = list(zip(x_data, y_data))

        # Create your Poly object(s).
        # Use keyword args to set display properties.
        line = wxplot.PolySpline(
            xy_data,
            colour=wx.Colour(128, 128, 0),   # Color: olive
            width=3,
        )

        # create your graphics object
        graphics = wxplot.PlotGraphics([line])

        # create your canvas
        panel = wxplot.PlotCanvas(self)

        # Edit panel-wide settings
        axes_pen = wx.Pen(wx.BLUE, 1, wx.PENSTYLE_LONG_DASH)
        panel.axesPen = axes_pen

        # draw the graphics object on the canvas
        panel.Draw(graphics)


if __name__ == '__main__':
    app = wx.App()
    frame = PlotExample()
    frame.Show()
    app.MainLoop()
