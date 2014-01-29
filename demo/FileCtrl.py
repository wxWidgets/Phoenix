#!/usr/bin/env python


import wx

#---------------------------------------------------------------------------


class FileCtrl(wx.FileCtrl):
    def __init__(self, parent, id=wx.ID_ANY, defaultDirectory="",
                 defaultFilename="",
                 wildCard=wx.FileSelectorDefaultWildcardStr,
                 style=wx.FC_DEFAULT_STYLE,
                 # | wx.FC_OPEN
                 # | wx.FC_SAVE
                 # | wx.FC_MULTIPLE
                 # | wx.FC_NOSHOWHIDDEN
                 pos=wx.DefaultPosition, size=wx.DefaultSize, name="filectrl"):
        wx.FileCtrl.__init__(self, parent, id, defaultDirectory, defaultFilename,
                             wildCard, style, pos, size, name)
        self.Bind(wx.EVT_FILECTRL_FILEACTIVATED, self.OnFileActivated)
        self.Bind(wx.EVT_FILECTRL_SELECTIONCHANGED, self.OnSelectionChanged)
        self.Bind(wx.EVT_FILECTRL_FOLDERCHANGED, self.OnFolderChanged)
        self.Bind(wx.EVT_FILECTRL_FILTERCHANGED, self.OnFilterChanged)

    def OnFileActivated(self, event):
        self.GetGrandParent().SetStatusText('File Activated: %s' % self.GetFilename())

    def OnSelectionChanged(self, event):
        self.GetGrandParent().SetStatusText('Selection Changed: %s' % self.GetPath())

    def OnFolderChanged(self, event):
        self.GetGrandParent().SetStatusText('Directory Changed: %s' % self.GetDirectory())

    def OnFilterChanged(self, event):
        self.GetGrandParent().SetStatusText('Filter Changed: %s' % self.GetFilterIndex())


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.CreateStatusBar()
        panel = wx.Panel(self)

        fc = FileCtrl(panel)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(fc, 1, wx.EXPAND | wx.ALL, 0)
        panel.SetSizer(vsizer)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, event):
        self.Destroy()

#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent)

        b = wx.Button(self, -1, "Create and Show a FileCtrl")
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

    def OnButton(self, evt):
        win = MyFrame(self, -1, "This is a wx.FileCtrl",
                  style=wx.DEFAULT_FRAME_STYLE)
        win.Show(True)


#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = """\
This control allows the user to select a file.

Two implementations of this class exist, one for Gtk and another
generic one for all the other ports.

This class is only available if USE_FILECTRL is set to 1.

------------------------------------------------------------------
Window Styles
FileCtrl supports the following styles:
 * FC_DEFAULT_STYLE: The default style: FC_OPEN
 * FC_OPEN: Creates an file control suitable for opening files. Cannot be combined with FC_SAVE.
 * FC_SAVE: Creates an file control suitable for saving files. Cannot be combined with FC_OPEN.
 * FC_MULTIPLE: For open control only, Allows selecting multiple files. Cannot be combined with FC_SAVE
 * FC_NOSHOWHIDDEN: Hides the "Show Hidden Files" checkbox (Generic only)

Events
 * EVT_FILECTRL_FILEACTIVATED: The user activated a file(by double-clicking or pressing Enter)
 * EVT_FILECTRL_SELECTIONCHANGED: The user changed the current selection(by selecting or deselecting a file)
 * EVT_FILECTRL_FOLDERCHANGED: The current folder of the file control has been changed
 * EVT_FILECTRL_FILTERCHANGED: The current file filter of the file control has been changed.

"""


if __name__ == '__main__':
    import sys
    import os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
