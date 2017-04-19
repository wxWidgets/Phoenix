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
                 pos=wx.DefaultPosition, size=wx.DefaultSize, name="filectrl", log=None):
        wx.FileCtrl.__init__(self, parent, id, defaultDirectory, defaultFilename,
                             wildCard, style, pos, size, name)

        self.log = log
        self.Bind(wx.EVT_FILECTRL_FILEACTIVATED, self.OnFileActivated)
        self.Bind(wx.EVT_FILECTRL_SELECTIONCHANGED, self.OnSelectionChanged)
        self.Bind(wx.EVT_FILECTRL_FOLDERCHANGED, self.OnFolderChanged)
        self.Bind(wx.EVT_FILECTRL_FILTERCHANGED, self.OnFilterChanged)

    def OnFileActivated(self, event):
        self.log.write('File Activated: %s\n' % self.GetFilename())

    def OnSelectionChanged(self, event):
        self.log.write('Selection Changed: %s\n' % self.GetPath())

    def OnFolderChanged(self, event):
        self.log.write('Directory Changed: %s\n' % self.GetDirectory())

    def OnFilterChanged(self, event):
        self.log.write('Filter Changed: %s\n' % self.GetFilterIndex())



#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent)

        wx.StaticText(self, -1,
                      "This is a generic control with features like a file dialog",
                      pos=(10,10))
        fc = FileCtrl(self, pos=(10,35), log=log)
        fc.SetSize((500,350))
        fc.BackgroundColour = 'sky blue'


#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = """\
This control allows the user to select a file.

Two implementations of this class exist, one for Gtk and another
generic one for all the other ports.

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
