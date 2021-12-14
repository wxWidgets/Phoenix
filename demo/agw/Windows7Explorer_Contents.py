#!/usr/bin/env python

import sys
import os
import wx
import six
import time
import datetime
import operator

from wx.lib.embeddedimage import PyEmbeddedImage

import images

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.append(os.path.split(dirName)[0])

try:
    from agw import ultimatelistctrl as ULC
except ImportError: # if it's not there locally, try the wxPython lib.
    from wx.lib.agw import ultimatelistctrl as ULC

bitmapDir = os.path.join(dirName, 'bitmaps')
sys.path.append(os.path.split(dirName)[0])

# helper function to make sure we don't convert unicode objects to strings
# or vice versa when converting lists and None values to text.
convert = str
if six.PY2:
    if 'unicode' in wx.PlatformInfo:
        convert = unicode


def FormatFileSize(size):

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']:

        if size < 1024.0:
            return "%3.2f %s" % (size, x)

        size /= 1024.0


class FirstColumnRenderer(object):

    def __init__(self, parent, fileName):

        self.parent = parent
        self.fileName = fileName

        self.normalFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.normalFont.SetPointSize(self.normalFont.GetPointSize() + 1)
        self.smallerFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)

        self.greyColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)

        if os.path.isdir(fileName):
            self.text = fileName
            bitmap = wx.Bitmap(os.path.join(bitmapDir, "folder.png"), wx.BITMAP_TYPE_PNG)
            self.icon = wx.Icon(bitmap)
            self.description = ""
            return

        self.text = os.path.split(fileName)[1]
        extension = os.path.splitext(fileName)[1]

        if not extension:
            self.text = fileName
            bitmap = wx.Bitmap(os.path.join(bitmapDir, "empty_icon.png"), wx.BITMAP_TYPE_PNG)
            self.icon = wx.Icon(bitmap)
            self.description = "File"
            return

        fileType = wx.TheMimeTypesManager.GetFileTypeFromExtension(extension)

        bmp = wx.Bitmap(os.path.join(bitmapDir, "empty_icon.png"), wx.BITMAP_TYPE_PNG)
        bmp = wx.Icon(bmp)

        if not fileType:
            icon = wx.Icon(wx.IconLocation(fileName))
            if not icon.IsOk():
                self.icon = bmp
            else:
                self.icon = icon

            self.description = "%s File"%extension[1:].upper()
            return

        #------- Icon info
        info = fileType.GetIconInfo()
        icon = None

        if info is not None:
            icon, file, idx = info
            if icon.IsOk():
                bmp = icon
            else:
                icon = None

        if icon is None:
            icon = wx.Icon(wx.IconLocation(fileName))
            if icon.IsOk():
                bmp = icon
            else:
                command = fileType.GetOpenCommand(fileName)
                command = " ".join(command.split()[0:-1])
                command = command.replace('"', "")
                if " -" in command:
                    command = command[0:command.index(" -")]

                icon = wx.Icon(wx.IconLocation(command))
                if icon.IsOk():
                    bmp = icon

        self.icon = bmp
        self.description = convert(fileType.GetDescription())

        if not self.description:
            self.description = "%s File"%extension[1:].upper()


    def DrawSubItem(self, dc, rect, line, highlighted, enabled):
        """Draw a custom progress bar using double buffering to prevent flicker"""

        bmpWidth, bmpHeight = self.icon.GetWidth(), self.icon.GetHeight()
        dc.DrawIcon(self.icon, rect.x+5, rect.y+(rect.height-bmpHeight)//2)

        dc.SetFont(self.normalFont)

        textWidth, textHeight = dc.GetTextExtent(self.text)
        dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
        dc.DrawText(self.text, rect.x+bmpWidth+10, rect.y+(rect.height - textHeight)//4)

        if not self.description:
            return

        dc.SetFont(self.smallerFont)

        dummy1, dummy2= dc.GetTextExtent("Type: ")
        textWidth, textHeight = dc.GetTextExtent("Type: " + self.description)

        dc.SetTextForeground(self.greyColour)
        dc.DrawText("Type: ", rect.x+bmpWidth+10, rect.y+3*(rect.height - textHeight)//4)

        dc.SetTextForeground(wx.BLACK)
        dc.DrawText(self.description, rect.x+bmpWidth+dummy1+10, rect.y+3*(rect.height - textHeight)//4)


    def GetLineHeight(self):

        dc = wx.MemoryDC()
        dc.SelectObject(wx.Bitmap(100, 20))

        bmpWidth, bmpHeight = self.icon.GetWidth(), self.icon.GetHeight()
        dc.SetFont(self.normalFont)

        textWidth, textHeight = dc.GetTextExtent(self.text)

        dc.SetFont(self.smallerFont)
        dummy1, dummy2= dc.GetTextExtent("Type: ")
        textWidth, textHeight = dc.GetTextExtent("Type: " + self.description)

        dc.SelectObject(wx.NullBitmap)

        return max(2*textHeight, bmpHeight) + 20


    def GetSubItemWidth(self):

        return 250


class SecondColumnRenderer(object):

    def __init__(self, parent, fileName):

        self.parent = parent
        self.fileName = fileName

        self.smallerFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)

        self.greyColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT)

        t = os.path.getmtime(fileName)
        date = datetime.datetime.fromtimestamp(t)
        self.date = date.strftime("%d/%m/%Y %H:%M")

        if os.path.isdir(fileName):
            self.size = ""
            return

        s = os.path.getsize(fileName)
        self.size = FormatFileSize(s)


    def DrawSubItem(self, dc, rect, line, highlighted, enabled):
        """Draw a custom progress bar using double buffering to prevent flicker"""

        dc.SetFont(self.smallerFont)

        date = self.date
        dummy1, dummy2= dc.GetTextExtent("Date modified: ")
        textWidth, textHeight = dc.GetTextExtent("Date modified: " + date)

        dc.SetTextForeground(self.greyColour)
        dc.DrawText("Date modified: ", rect.x+5, rect.y+(rect.height - textHeight)//4)

        dc.SetTextForeground(wx.BLACK)
        dc.DrawText(date, rect.x+dummy1+5, rect.y+(rect.height - textHeight)//4)

        if not self.size:
            return

        dummy1, dummy2= dc.GetTextExtent("Size: ")

        dc.SetTextForeground(self.greyColour)
        dc.DrawText("Size: ", rect.x+5, rect.y+3*(rect.height - textHeight)//4)

        dc.SetTextForeground(wx.BLACK)
        dc.DrawText(self.size, rect.x+dummy1+5, rect.y+3*(rect.height - textHeight)//4)


    def GetLineHeight(self):

        dc = wx.MemoryDC()
        dc.SelectObject(wx.Bitmap(100, 20))
        textWidth, textHeight, d1, d2 = dc.GetFullTextExtent("Date modified: %s"%self.date,
                                                             self.smallerFont)

        dc.SelectObject(wx.NullBitmap)
        return 2*textHeight + 20


    def GetSubItemWidth(self):

        dc = wx.MemoryDC()
        dc.SelectObject(wx.Bitmap(100, 20))

        textWidth, textHeight, d1, d2 = dc.GetFullTextExtent("Date modified: %s"%self.date,
                                                             self.smallerFont)

        dc.SelectObject(wx.NullBitmap)

        return textWidth+10


class Windows7Explorer(ULC.UltimateListCtrl):

    def __init__(self, parent, log):

        ULC.UltimateListCtrl.__init__(self, parent, -1, style=wx.BORDER_THEME,
                                      agwStyle=wx.LC_REPORT|wx.LC_NO_HEADER|wx.LC_HRULES|
                                      ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)

        self.EnableSelectionVista()
        self.PopulateList()


    def PopulateList(self, path=""):

        self.ClearAll()

        self.InsertColumn(0, "Column 1")
        self.InsertColumn(1, "Column 2")

        if not path.strip():
            path = os.getcwd()

        os.chdir(path)
        files1 = os.listdir(path)
        files1.sort()

        files = []
        for file in files1:
            kind = not os.path.isdir(file)
            name = os.path.split(file)[1]
            files.append((kind, name, name.lower()))

        files = sorted(files, key=operator.itemgetter(0, 2))
        dummy_log = wx.LogNull()

        for kind, file, lower in files:
            index = self.InsertStringItem(sys.maxsize, "")

            klass = FirstColumnRenderer(self, file)
            self.SetItemCustomRenderer(index, 0, klass)

            self.SetStringItem(index, 1, "")
            klass = SecondColumnRenderer(self, file)
            self.SetItemCustomRenderer(index, 1, klass)

        self.SetColumnWidth(0, ULC.ULC_AUTOSIZE_FILL)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)


#---------------------------------------------------------------------------

class TestFrame(wx.Frame):

    def __init__(self, parent, log):

        wx.Frame.__init__(self, parent, -1, "UltimateListCtrl - Windows 7 Explorer", size=(800, 600))

        self.log = log

        panel = wx.Panel(self)
        panelSizer = wx.BoxSizer(wx.VERTICAL)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)

        static = wx.StaticText(panel, -1, "Choose a folder to display:")
        static.SetFont(font)
        panelSizer.Add(static, 0, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, 10)

        dp1 = wx.DirPickerCtrl(panel, path=os.getcwd(), style=wx.DIRP_USE_TEXTCTRL)
        dp1.SetTextCtrlProportion(2)
        panelSizer.Add(dp1, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        # Create the CustomTreeCtrl, using a derived class defined below
        self.ulc = Windows7Explorer(panel, self.log)

        panelSizer.Add(self.ulc, 1, wx.EXPAND|wx.ALL, 10)
        panel.SetSizer(panelSizer)

        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.OnPickDir, dp1)

        self.ulc.SetFocus()
        self.SetIcon(images.Mondrian.GetIcon())
        self.CenterOnScreen()
        self.Show()


    def OnPickDir(self, event):

        wx.BeginBusyCursor()
        self.Freeze()
        path = event.GetPath()

        try:
            self.ulc.PopulateList(path)
        except OSError:
            self.log.write("You dont have permission to access folder: %s"%path)
            wx.EndBusyCursor()
            self.Thaw()
            return

        self.Layout()
        self.SendSizeEvent()
        self.Thaw()

        self.ulc.DoLayout()
        wx.EndBusyCursor()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    app = wx.App(0)
    frame = TestFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()
