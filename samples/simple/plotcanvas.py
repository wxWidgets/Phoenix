# A PlotCanvas is a Subclass of a wx.Panel which holds two scrollbars and the
# actual plotting zoom canvas (self.canvas). It allows for simple general
# plotting of data with zo om, labels, and automatic axis scaling.

import wx
import wx.lib.plot as plot


class MyFrame(wx.Frame):

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 400))

        # Create a PlotCanvas instance
        self.plot_canvas = plot.PlotCanvas(self)

        # Define some sample data
        data1 = [(1, 2), (2, 5), (3, 4), (4, 7), (5, 6)]
        data2 = [(1, 1), (2, 3), (3, 6), (4, 5), (5, 8)]

        # Create PolyLine objects for the data
        line1 = plot.PolyLine(data1, colour='blue', width=2, legend='Line 1')
        line2 = plot.PolyLine(data2, colour='red', width=2, legend='Line 2')

        # Create a PlotGraphics object to hold the lines and define labels
        graphics = plot.PlotGraphics([line1, line2],
                                     "Sample Plot",
                                     "X-axis Label",
                                     "Y-axis Label")

        # Draw the plot on the canvas
        self.plot_canvas.Draw(graphics)

        self.Centre()
        self.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "PlotCanvas Demo")
    app.MainLoop()
