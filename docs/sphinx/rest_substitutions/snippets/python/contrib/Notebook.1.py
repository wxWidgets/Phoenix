##Andrea Gavana
#!/usr/bin/env python

# This sample creates a "File->Open" menu, and lets the user select
# a Python file. Upon selection, the file is read in memory and a new
# wx.TextCtrl showing the file content is added as a page of a wx.Notebook

import wx
import os

class NotebookFrame(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title)

        # Create the notebook
        self.notebook = wx.Notebook(self, style=wx.NB_BOTTOM)

        # Setting up the menu
        file_menu = wx.Menu()

        # wx.ID_OPEN
        menu_item = file_menu.Append(wx.ID_OPEN, '&Open...', 'Open and read a new Python file')
        # Bind the "select menu item" event to the OnOpen event handler
        self.Bind(wx.EVT_MENU, self.OnOpen, menu_item)

        # Creating the menubar
        menu_bar = wx.MenuBar()

        # Adding the 'file_menu' to the menu bar
        menu_bar.Append(file_menu, '&File')

        # Adding the menu bar to the frame content
        self.SetMenuBar(menu_bar)

        self.Show()


    def OnOpen(self, event):

        # This is how you pre-establish a file filter so that the dialog
        # only shows the extension(s) you want it to.
        wildcard = 'Python source (*.py)|*.py'

        dlg = wx.FileDialog(None, message="Choose a Python file", defaultDir=os.getcwd(),
                            defaultFile="", wildcard=wildcard, style=wx.FD_OPEN)

        # Show the dialog and retrieve the user response. If it is the OK response,
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns the file that was selected
            path = dlg.GetPath()

            # Open the file as read-only and slurp its content
            with open(path, 'rt') as fid:
                text = fid.read()

            # Create the notebook page as a wx.TextCtrl and
            # add it as a page of the wx.Notebook
            text_ctrl = wx.TextCtrl(self.notebook, style=wx.TE_MULTILINE)
            text_ctrl.SetValue(text)

            filename = os.path.split(os.path.splitext(path)[0])[1]
            self.notebook.AddPage(text_ctrl, filename, select=True)

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()


app = wx.App(False)
frame = NotebookFrame(None, 'Notebook example')
app.MainLoop()
