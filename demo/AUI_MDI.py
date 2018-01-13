#!/usr/bin/env python

import wx
import wx.aui as aui



#----------------------------------------------------------------------


class ParentFrame(aui.AuiMDIParentFrame):
    def __init__(self, parent):
        aui.AuiMDIParentFrame.__init__(self, parent, -1,
                                          title="AuiMDIParentFrame",
                                          size=(640,480),
                                          style=wx.DEFAULT_FRAME_STYLE)
        self.count = 0
        self.mb = self.MakeMenuBar()
        self.SetMenuBar(self.mb)
        self.CreateStatusBar()
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def MakeMenuBar(self):
        mb = wx.MenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "New child window\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.OnNewChild, item)
        item = menu.Append(-1, "Close parent")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        mb.Append(menu, "&File")
        return mb

    def OnNewChild(self, evt):
        self.count += 1
        child = ChildFrame(self, self.count)
        #child.Show()

    def OnDoClose(self, evt):
        self.Close()

    def OnCloseWindow(self, evt):
        # Close all ChildFrames first else Python crashes
        for m in self.GetChildren():
            if isinstance(m, aui.AuiMDIClientWindow):
                for k in list(m.GetChildren()):
                    if isinstance(k, ChildFrame):
                        k.Close()
        evt.Skip()


#----------------------------------------------------------------------

class ChildFrame(aui.AuiMDIChildFrame):
    def __init__(self, parent, count):
        aui.AuiMDIChildFrame.__init__(self, parent, -1,
                                         title="Child: %d" % count)
        mb = parent.MakeMenuBar()
        menu = wx.Menu()
        item = menu.Append(-1, "This is child %d's menu" % count)
        mb.Append(menu, "&Child")
        self.SetMenuBar(mb)

        p = wx.Panel(self)
        wx.StaticText(p, -1, "This is child %d" % count, (10,10))
        p.SetBackgroundColour('light blue')

        sizer = wx.BoxSizer()
        sizer.Add(p, 1, wx.EXPAND)
        self.SetSizer(sizer)

        wx.CallAfter(self.Layout)

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Show a AuiMDIParentFrame", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):
        pf = ParentFrame(self)
        pf.Show()



#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>aui.AuiMDI</center></h2>

The aui.AuiMDIParentFrame and aui.AuiMDIChildFrame classes
implement the same API as wx.MDIParentFrame and wx.MDIChildFrame, but
implement the multiple document interface with a aui.AuiNotebook.


</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

