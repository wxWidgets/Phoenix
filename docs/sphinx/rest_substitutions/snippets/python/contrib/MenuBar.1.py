##Andrea Gavana
#!/usr/bin/env python

# This sample shows how to create a simple wx.MenuBar
# and a simple wx.StatusBar

import wx

class MainWindow(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title)

        # A Statusbar in the bottom of the window
        self.CreateStatusBar()

        # Setting up the menu
        file_menu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided
        # by wxWidgets.
        file_menu.Append(wx.ID_ABOUT, '&About',
                         'Information about this application')
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_EXIT, 'E&xit', 'Exit the application')

        # Creating the menubar
        menu_bar = wx.MenuBar()

        # Adding the 'file_menu' to the menu bar
        menu_bar.Append(file_menu, '&File')

        # Adding the menu bar to the frame content
        self.SetMenuBar(menu_bar)
        self.Show()

app = wx.App(False)
frame = MainWindow(None, 'MenuBar and StatusBar')
app.MainLoop()
