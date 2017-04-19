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
    from agw import multidirdialog as MDD
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.multidirdialog as MDD

import images


class MultiDirDialogDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent)

        self.log = log

        self.mainPanel = wx.Panel(self)
        self.dialogSizer_staticbox = wx.StaticBox(self.mainPanel, -1, "Dialog Styles")

        self.dd_multiple = wx.CheckBox(self.mainPanel, -1, "MDD.DD_MULTIPLE")
        self.dd_must = wx.CheckBox(self.mainPanel, -1, "wx.DD_DIR_MUST_EXIST")
        self.dd_new = wx.CheckBox(self.mainPanel, -1, "wx.DD_NEW_DIR_BUTTON")

        self.showDialog = wx.Button(self.mainPanel, -1, "Show MultiDirDialog")

        self.SetProperties()
        self.DoLayout()

        self.Bind(wx.EVT_BUTTON, self.OnShowDialog, self.showDialog)


    def SetProperties(self):

        self.showDialog.SetDefault()


    def DoLayout(self):

        frameSizer = wx.BoxSizer(wx.VERTICAL)
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.StaticBoxSizer(self.dialogSizer_staticbox, wx.VERTICAL)
        buttonSizer.Add(self.dd_multiple, 0, wx.LEFT|wx.RIGHT|wx.TOP, 5)
        buttonSizer.Add((0, 2), 0, 0, 0)
        buttonSizer.Add(self.dd_must, 0, wx.LEFT|wx.RIGHT, 5)
        buttonSizer.Add((0, 2), 0, 0, 0)
        buttonSizer.Add(self.dd_new, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM, 5)

        mainSizer.Add(buttonSizer, 0, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add((10, 0), 0, 0, 0)
        mainSizer.Add(self.showDialog, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        mainSizer.Add((10, 0), 0, 0, 0)

        panelSizer.Add(mainSizer, 0, wx.EXPAND)
        self.mainPanel.SetSizer(panelSizer)

        frameSizer.Add(self.mainPanel, 1, wx.EXPAND)
        self.SetSizer(frameSizer)
        frameSizer.Layout()


    def OnShowDialog(self, event):

        dlgStyle = 0
        for child in self.mainPanel.GetChildren():
            if isinstance(child, wx.CheckBox):
                if child.GetValue():
                    dlgStyle |= eval(child.GetLabel())

        userPath = wx.StandardPaths.Get().GetUserDataDir()
        dlg = MDD.MultiDirDialog(self, title="Custom MultiDirDialog :-D", defaultPath=userPath,
                                 agwStyle=dlgStyle)

        dlg.SetIcon(images.Mondrian.GetIcon())
        if dlg.ShowModal() != wx.ID_OK:
            self.log.write("You Cancelled The Dialog!\n")
            dlg.Destroy()
            return

        paths = dlg.GetPaths()
        for indx, path in enumerate(paths):
            self.log.write("Path %d: %s\n"%(indx+1, path))

        dlg.Destroy()


#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = MultiDirDialogDemo(nb, log)
    return win

#----------------------------------------------------------------------


overview = MDD.__doc__


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

