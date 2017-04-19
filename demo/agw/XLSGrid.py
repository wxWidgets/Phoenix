#!/usr/bin/env python

import os
import sys
import wx

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

_isStandalone = False

try:
    from agw import xlsgrid as XG
    dataDir = os.path.join(dirName, "data")
    _isStandalone = True
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.xlsgrid as XG
    dataDir = os.path.join(dirName, "data")

_hasXLRD = True

try:
    import xlrd
except ImportError:
    _hasXLRD = False

_hasWin32 = False

if wx.Platform == "__WXMSW__":
    try:
        from win32com.client import Dispatch
        _hasWin32 = True
    except ImportError:
        pass


_msg = "This is the about dialog of the XLSGrid demo.\n\n" + \
       "Author: Andrea Gavana @ 17 Aug 2011\n\n" + \
       "Please report any bugs/requests of improvements\n" + \
       "to me at the following addresses:\n\n" + \
       "andrea.gavana@gmail.com\n" + "andrea.gavana@maerskoil.com\n\n" + \
       "Welcome to wxPython " + wx.VERSION_STRING + "!!"


class XLSGridDemo(wx.Panel):

    def __init__(self, parent, log):

        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, " Test XLSGrid ", (50, 50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)


    def OnButton(self, evt):

        XLSGridFrame(None)


class XLSGridFrame(wx.Frame):

    def __init__(self, parent, size=(950, 730)):

        wx.Frame.__init__(self, parent, title="XLSGrid wxPython Demo", size=size)
        panel = XLSGridPanel(self)

        self.CreateMenuAndStatusBar()
        self.CenterOnScreen()
        self.Show()


    def CreateMenuAndStatusBar(self):

        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        item = wx.MenuItem(fileMenu, wx.ID_ANY, "E&xit", "Exit XLSGrid demo")
        self.Bind(wx.EVT_MENU, self.OnClose, item)
        fileMenu.Append(item)

        item = wx.MenuItem(helpMenu, wx.ID_ANY, "About...", "Shows the about dialog")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        helpMenu.Append(item)

        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)
        statusbar.SetStatusWidths([-2, -1])

        statusbar_fields = [("wxPython XLSGrid Demo, Andrea Gavana @ 08 Aug 2011"),
                            ("Welcome To wxPython!")]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)


    def OnClose(self, event):

        wx.CallAfter(self.Destroy)


    def OnAbout(self, event):

        dlg = wx.MessageDialog(self, _msg, "XLSGrid wxPython Demo",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class XLSGridPanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)

        self.start_button = wx.Button(self, -1, "Start")
        self.grid = XG.XLSGrid(self)

        self.grid.Hide()

        self.DoLayout()

        self.Bind(wx.EVT_BUTTON, self.OnStart, self.start_button)


    def DoLayout(self):

        xlrd_ver = xlrd.__VERSION__
        string_xlrd = "Version " + xlrd_ver

        if xlrd_ver <= "0.7.1":
            string_xlrd += ": hyperlink and rich-text functionalities will not work. xlrd 0.7.2 (SVN) is required for this."
        else:
            string_xlrd += ": hyperlink and rich-text functionalities will work!"

        if _hasWin32:
            string_pywin32 = "You have pywin32! XLSGrid cells should appear exactly as in Excel (WYSIWYG)."
        else:
            string_pywin32 = "You don't have pywin32. Cell string formatting will be severely limited."

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_right_sizer = wx.BoxSizer(wx.VERTICAL)
        top_center_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(self.start_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        label_1 = wx.StaticText(self, -1, "xlrd:")
        label_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        top_center_sizer.Add(label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5)
        top_center_sizer.Add((0, 0), 1, wx.EXPAND, 0)
        label_2 = wx.StaticText(self, -1, "pywin32:")
        label_2.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        top_center_sizer.Add(label_2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT, 5)
        top_sizer.Add(top_center_sizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        label_xlrd = wx.StaticText(self, -1, string_xlrd)
        top_right_sizer.Add(label_xlrd, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        top_right_sizer.Add((0, 0), 1, wx.EXPAND, 0)
        label_pywin32 = wx.StaticText(self, -1, string_pywin32)
        top_right_sizer.Add(label_pywin32, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        top_sizer.Add(top_right_sizer, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
        main_sizer.Add(top_sizer, 0, wx.ALL|wx.EXPAND, 5)
        main_sizer.Add((0, 10))
        main_sizer.Add(self.grid, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(main_sizer)

        main_sizer.Layout()


    def OnStart(self, event):

        event.Skip()

        filename = os.path.join(os.path.abspath(dataDir), "Example_1.xls")

        if not os.path.isfile(filename):
            dlg = wx.MessageDialog(self, 'Error: the file "Example_1.xls" is not in the "data" directory',
                                   'XLSGridDemo Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        busy = wx.BusyInfo("Reading Excel file, please wait...")

        sheetname = "Example_1"
        book = xlrd.open_workbook(filename, formatting_info=1)

        sheet = book.sheet_by_name(sheetname)
        rows, cols = sheet.nrows, sheet.ncols

        comments, texts = XG.ReadExcelCOM(filename, sheetname, rows, cols)

        del busy

        self.grid.Show()
        self.grid.PopulateGrid(book, sheet, texts, comments)

        self.start_button.Enable(False)
        self.Layout()


#----------------------------------------------------------------------

def runTest(frame, nb, log):

    if _hasXLRD:
        win = XLSGridDemo(nb, log)
        return win
    else:
        msg = 'This demo requires the xlrd package to be installed.\n' \
              'See: http://pypi.python.org/pypi/xlrd'

        if _isStandalone:
            dlg = wx.MessageDialog(nb, msg, 'Sorry', wx.ICON_WARNING|wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return None
        else:
            from Main import MessagePanel
            win = MessagePanel(nb, msg, 'Sorry', wx.ICON_WARNING)

        return win

#----------------------------------------------------------------------

overview = XG.__doc__

if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

