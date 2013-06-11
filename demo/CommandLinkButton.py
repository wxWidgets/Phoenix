
import wx

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        cmd = wx.CommandLinkButton(self, -1,
                                   "wx.CommandLinkButton",
                                   """\
This type of button includes both a main label and a 'note' that is meant to
contain a description of what the button does or what it is used for.  On
Windows 7 it is a new native widget type, on the other platforms it is
implemented generically.""",
                                   pos=(25,25))

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

