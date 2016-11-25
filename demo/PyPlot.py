
import wx

hadImportError = False
try:
    import numpy
    import wx.lib.plot
except ImportError:
    hadImportError = True


#############################################################################
# Where's the code???
#
# The wx.lib.plot package comes with its own excellent demo built in, for
# testing purposes, but it serves quite well to demonstrate the code and
# classes within, so we are simply importing and using that code for this
# sample in the wxPython demo. Please load up wx/lib/plot/examples/demo.py
# for a review of the demo code itself.
#############################################################################

#---------------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Show the PyPlot sample", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        from wx.lib.plot.examples.demo import PlotDemoMainFrame
        win = PlotDemoMainFrame(self, -1, "wx.lib.plot Demo")
        win.Show()

#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    if not hadImportError:
        win = TestPanel(nb, log)
    else:
        from wx.lib.msgpanel import MessagePanel
        win = MessagePanel(nb, """\
This demo requires the numpy module, which could not be imported.
It probably is not installed (it's not part of the standard Python
distribution). See https://pypi.python.org/pypi/numpy for information
about the numpy package.""", 'Sorry', wx.ICON_WARNING)

    return win


#----------------------------------------------------------------------

if hadImportError:
    overview = ""
else:
    overview = """\
<html><body>
<center><h2>PyPlot</h2></center>

This demo illustrates the features of the PyPlot modules, found
in the wx.lib.plot package.

<p>
The demo illustrates several different plot styles (with appropriate
variations on fonts, etc, to show how flexible it is) as well as
provides you with a means to tinker with all the features that
come with the class itself. Be sure to explore the options in the
Plot and Options menus to explore some of the capabilities of this
plotting package.

</body></html>
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

