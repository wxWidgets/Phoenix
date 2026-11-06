import datetime
import pathlib

import wx
import wx.adv
import wx.grid


# Parameters accept the types that SIP converts to the parameter's class
# automatically, even when that class is defined by a different etg script
# than the method (#2775)

def bitmapBundles(info: wx.adv.AboutDialogInfo) -> None:
    # (#2933)
    info.SetIcon(wx.BitmapBundle())
    info.SetIcon(wx.Icon())
    info.SetIcon(wx.Bitmap())
    info.SetIcon(wx.Image())
    info.SetIcon('icon.png')  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def colours(win: wx.Window, grid: wx.grid.Grid) -> None:
    win.SetBackgroundColour((255, 0, 0))
    win.SetBackgroundColour((255, 0, 0, 128))
    win.SetBackgroundColour('red')
    grid.SetDefaultCellBackgroundColour((255, 0, 0))
    win.SetBackgroundColour((255, 0))  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]


def tuples(grid: wx.grid.Grid) -> None:
    wx.Frame(None, pos=(10, 20), size=(200, 100))
    grid.SetGridCursor((1, 2))


def dates(calendar: wx.adv.CalendarCtrl) -> None:
    calendar.SetDate(datetime.date(2026, 1, 1))
    calendar.SetDate(datetime.datetime(2026, 1, 1, 12, 0))


# File system path parameters also accept os.PathLike objects (#2560)
def paths(win: wx.Window, path: pathlib.Path) -> None:
    wx.FileDialog(win, defaultDir=path, defaultFile='file.txt')
    wx.Image(path)
    wx.Image(path, wx.BITMAP_TYPE_PNG)
    wx.Bitmap().SaveFile(path, wx.BITMAP_TYPE_PNG)
    wx.FileSystem.FileNameToURL(path)
    win.SetLabel(path)  # type: ignore[arg-type]  # ty: ignore[invalid-argument-type]
