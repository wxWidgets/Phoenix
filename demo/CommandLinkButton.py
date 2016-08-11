#!/usr/bin/env python

import wx
import wx.adv
from textwrap import dedent

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        cmd = wx.adv.CommandLinkButton(self, -1, "wx.CommandLinkButton",
            dedent("""\
            This type of button includes both a main label and a 'note' that
            is meant to contain a description of what the button does or
            what is used for.  On Windows 7 it is a new native widget type,
            on the other platforms it is implemented generically.
            """),
            pos=(25,25), size=(500,-1))

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.CommandLinkButton</center></h2>

This type of button includes both a main label and a 'note' that is meant to
contain a description of what the button does or what it is used for.  On
Windows 7 it is a new native widget type, on the other platforms it is
implemented generically.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

