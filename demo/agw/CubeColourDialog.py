#!/usr/bin/env python

import wx

import os
import sys

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import cubecolourdialog as CCD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.cubecolourdialog as CCD


class CubeColourDialogDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent, -1)

        static = wx.StaticText(self, -1, "Notice the panel background colour!", (50, 50))
        b = wx.Button(self, -1, "Create and Show a CubeColourDialog", (50, 70))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

        self.log = log


    def OnButton(self, evt):

        if not hasattr(self, "colourData"):
            self.colourData = wx.ColourData()

        self.colourData.SetColour(self.GetBackgroundColour())

        dlg = CCD.CubeColourDialog(self, self.colourData)

        if dlg.ShowModal() == wx.ID_OK:

            # If the user selected OK, then the dialog's wx.ColourData will
            # contain valid information. Fetch the data ...
            self.colourData = dlg.GetColourData()
            h, s, v, a = dlg.GetHSVAColour()

            # ... then do something with it. The actual colour data will be
            # returned as a three-tuple (r, g, b) in this particular case.
            colour = self.colourData.GetColour()
            self.log.WriteText('You selected: %s: %d, %s: %d, %s: %d, %s: %d\n' % ("Red", colour.Red(),
                                                                                   "Green", colour.Green(),
                                                                                   "Blue", colour.Blue(),
                                                                                   "Alpha", colour.Alpha()))
            self.log.WriteText('HSVA Components: %s: %d, %s: %d, %s: %d, %s: %d\n\n' % ("Hue", h,
                                                                                        "Saturation", s,
                                                                                        "Brightness", v,
                                                                                        "Alpha", a))
            self.SetBackgroundColour(self.colourData.GetColour())
            self.Refresh()

        # Once the dialog is destroyed, Mr. wx.ColourData is no longer your
        # friend. Don't use it again!
        dlg.Destroy()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = CubeColourDialogDemo(nb, log)
    return win

#----------------------------------------------------------------------

overview = CCD.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

