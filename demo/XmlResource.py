#!/usr/bin/env python

import  wx
import  wx.xrc  as  xrc

from Main import opj

#----------------------------------------------------------------------

RESFILE = opj("data/resource_wdr.xrc")

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.log = log

        # make the components
        label = wx.StaticText(self, -1, "The lower panel was built from this XML:")
        label.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        with open(RESFILE, 'rb') as f:
            resourceBytes = f.read()

        text = wx.TextCtrl(self, -1, resourceBytes,
                          style=wx.TE_READONLY|wx.TE_MULTILINE)
        text.SetInsertionPoint(0)

        line = wx.StaticLine(self, -1)

        # This shows a few different ways to load XML Resources
        if 0:
            # XML Resources can be loaded from a file like this:
            res = xrc.XmlResource(RESFILE)

        elif 1:
            # or from a Virtual FileSystem:
            wx.FileSystem.AddHandler(wx.MemoryFSHandler())
            wx.MemoryFSHandler.AddFile("my_XRC_data", resourceBytes)
            # notice the matching filename
            res = xrc.XmlResource("memory:my_XRC_data")

        else:
            # or from a buffer compatible object, like this:
            res = xrc.XmlResource()
            res.LoadFromBuffer(resourceBytes)


        # Now create a panel from the resource data
        panel = res.LoadPanel(self, "MyPanel")

        # and do the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.EXPAND|wx.TOP|wx.LEFT, 5)
        sizer.Add(text, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(line, 0, wx.EXPAND)
        sizer.Add(panel, 1, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

