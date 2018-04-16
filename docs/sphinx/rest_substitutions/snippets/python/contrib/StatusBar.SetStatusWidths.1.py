##Andrea Gavana
#!/usr/bin/env python

# This sample shows how to create a wx.StatusBar with 2 fields,
# set the second field to have double width with respect to the
# first and and display the date of today in the second field.

import wx
import datetime

class MainWindow(wx.Frame):

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title)

        # A Statusbar in the bottom of the window
        # Set it up so it has two fields
        self.CreateStatusBar(2)

        # Set the second field to be double in width wrt the first
        self.SetStatusWidths([-1, -2])

        # Get today date via datetime
        today = datetime.datetime.today()
        today = today.strftime('%d-%b-%Y')

        # Set today date in the second field
        self.SetStatusText(today, 1)

        self.Show()

app = wx.App(False)
frame = MainWindow(None, 'SetStatusWidths example')
app.MainLoop()
