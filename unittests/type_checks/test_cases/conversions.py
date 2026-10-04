import datetime

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
