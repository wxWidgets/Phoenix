#!/usr/bin/env python

#-Imports----------------------------------------------------------------------

#--Python Imports.
import os
import sys

#--wxPython Imports.
import wx
from wx.lib.embeddedimage import PyEmbeddedImage

#-Globals----------------------------------------------------------------------

paperairplane_arrow_blue24 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAACpUlEQVR42q3VC0hTYRgG4M6m"
    "m8uRmGaVV8SQSrDMbJ6azpZ40qXLXM05y2GikFdKS4PUrEINUygVQ0FalmU3soiIhEohbEGS"
    "RlQkRChUUAVBCL19/zBBNNDT+eBh8AO87LtsC6h+ExNRE45IWwo3d9DHBNETleQhfqEahMVa"
    "WMhPEkaUkgYErtHCWNSOkAgBnEz+mZ4CiKtkAaFRBmxNPwJDbj2Cw7eA42Tv6NmHuEgSEKY1"
    "wZjXgJiUYtiqLmNZcDjouZ94SxISrtsNS2kHNPG5EDKqkXe8G55LA1nIJeJJ5ER8rYszI6vC"
    "Dk1CgVNqXhMKTnVjoYc3C6kjHkQmOiBSn46cym5oth2ckl1uR9FJO5QqNbuRbKIWHbIxPgP5"
    "J65DY6iYpvT0Lew/2gq5q/L/boQXrDhQ34vo5GPT8Ck1qOvoQ1ZhDWRyF/E3EpOYiYqm+4je"
    "UTuDztwA+53nSDJls/UVdyO67XtQ3dKH6J2NsxJsbbj75BUieT0b+vxvJN64F7XtA+BNrf+U"
    "X30bjx2v4eamYiH3iNec11dItaHRPgje3DErU3EPHMMfoNE6v8E3kkaC5jwPQ5oNzVdegLdc"
    "nGGztQuOkTHssu7DAo5jgzaS9fNqU1KqFed7hsBbr86QU/UQff0OtkXsHkpIFFlOFHNeWSEx"
    "BeNfvuPZ8Bh6H42irWcElrIH2JR5Ew2dQzhUWft3uLFTrZlnwcvbBzp9AvJLDqOz6xrejI6j"
    "7MwgLvS+hZBsZgEtJIJ4ijm2QnKDvCSfqNe/fANCMPDUgfcffyAoZBULsJKVzmsWUWriT1aT"
    "tWQDKXdVKCfOnmuGr58/67+WrBD7yyojCuJOFk22YQmJI1/JBOHZm5T/1zKimhzq4GT/FxNJ"
    "iyMK4kP8nK0UUX8Azg5aSnmghYAAAAAASUVORK5CYII=")

paperairplane_arrow_white24 = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAB2ElEQVR4Aa3VsatSYRiA8Twd"
    "y5Pa5SoXi0RpErQuQehQIEREi+ka5KSLew4uDaKLgy26C7bkpIHgaOlgSINIEjgo0f0HqiFo"
    "eXve4UxO174PfogqPpzj971eYf3EQ/jggdnl8/mEh+84xzXjgUQiIdlsViNfEYfXeKDZbEoy"
    "mdTIR0RgGw30+31pt9sSjUY18h4hXDUWGAwGsl6vpV6vSzgc1shbnMAyFtjv97JYLKRarYrf"
    "79fIawRhGQuo6XQqlUpFvF7vX95+BT88xgJqPB5LsVgUy7J+85En7hkxFlD6Wj6f11v1wz0j"
    "RgO73U56vd7hGTEVUNvtVrrdrqRSqcMzYiKgNpuNtFqtwzNiKqBms5luX91ZGqnjJiwjgdVq"
    "JY1Gw72CL3iKW7D/O6A/dKfTcefUNzzHPZwauYLlcimlUkm//A+KeIAz2JeeprpbdOiNRiPR"
    "26KByWQimUxGAx/wCHeO2ariOI7E43FJp9NSKBSkVqvJfD6X4XAosVjMnUtJBI450c/wBu/w"
    "CXsNlstl0fsfCAQ08AKxY/+MHERwFwncx0vm0EUul5NgMPiL548ROXayemDjOm4giBDO8RkX"
    "yCAEY8sDDd5GF0mcwPiycYozOLj0+gej7JQuh90YaAAAAABJRU5ErkJggg==")


gFileDir = os.path.dirname(os.path.abspath(__file__))

ID_PAPERAIRPLANE_ARROW_BLUE = 2001
ID_PAPERAIRPLANE_ARROW_RED = 2002
ID_PAPERAIRPLANE_ARROW_GREY = 2003
ID_PAPERAIRPLANE_ARROW_DARK = 2004
ID_PAPERAIRPLANE_ARROW_BLUE_FADEOUT80 = 2005
ID_PAPERAIRPLANE_ARROW_COLORSHIFT = 2006
ID_PAPERAIRPLANE_ARROW_WHITE = 2006

ID_PAPERAIRPLANE_ARROW_WHITE_PNG = 2007

ID_PAPERAIRPLANE_ARROW_BLUE_PY = 2008
ID_PAPERAIRPLANE_ARROW_WHITE_PY = 2009

cursors = {
    # .cur, .ani loose files.
    "paperairplane_arrow_blue.cur" : ID_PAPERAIRPLANE_ARROW_BLUE,
    "paperairplane_arrow_red.cur" : ID_PAPERAIRPLANE_ARROW_RED,
    "paperairplane_arrow_grey.cur" : ID_PAPERAIRPLANE_ARROW_GREY,
    "paperairplane_arrow_dark.cur" : ID_PAPERAIRPLANE_ARROW_DARK,
    "paperairplane_arrow_blue_fadeout80.cur" : ID_PAPERAIRPLANE_ARROW_BLUE_FADEOUT80,
    "paperairplane_arrow_white.cur" : ID_PAPERAIRPLANE_ARROW_WHITE,
    "paperairplane_arrow_colorshift.ani" : ID_PAPERAIRPLANE_ARROW_COLORSHIFT,
    # .png loose files.
    "paperairplane_arrow_white24.png" : ID_PAPERAIRPLANE_ARROW_WHITE_PNG,
    # PyEmbeddedImages
    "paperairplane_arrow_blue24 [PyEmbeddedImage]" : ID_PAPERAIRPLANE_ARROW_BLUE_PY,
    "paperairplane_arrow_white24 [PyEmbeddedImage]" : ID_PAPERAIRPLANE_ARROW_WHITE_PY,
    # wxPython Stock Cursors.
    "wx.CURSOR_ARROW" : wx.CURSOR_ARROW,
    "wx.CURSOR_RIGHT_ARROW" : wx.CURSOR_RIGHT_ARROW,
    "wx.CURSOR_BULLSEYE" : wx.CURSOR_BULLSEYE,
    "wx.CURSOR_CHAR" : wx.CURSOR_CHAR,
    "wx.CURSOR_CROSS" : wx.CURSOR_CROSS,
    "wx.CURSOR_HAND" : wx.CURSOR_HAND,
    "wx.CURSOR_IBEAM" : wx.CURSOR_IBEAM,
    "wx.CURSOR_LEFT_BUTTON" : wx.CURSOR_LEFT_BUTTON,
    "wx.CURSOR_MAGNIFIER" : wx.CURSOR_MAGNIFIER,
    "wx.CURSOR_MIDDLE_BUTTON" : wx.CURSOR_MIDDLE_BUTTON,
    "wx.CURSOR_NO_ENTRY" : wx.CURSOR_NO_ENTRY,
    "wx.CURSOR_PAINT_BRUSH" : wx.CURSOR_PAINT_BRUSH,
    "wx.CURSOR_PENCIL" : wx.CURSOR_PENCIL,
    "wx.CURSOR_POINT_LEFT" : wx.CURSOR_POINT_LEFT,
    "wx.CURSOR_POINT_RIGHT" : wx.CURSOR_POINT_RIGHT,
    "wx.CURSOR_QUESTION_ARROW" : wx.CURSOR_QUESTION_ARROW,
    "wx.CURSOR_RIGHT_BUTTON" : wx.CURSOR_RIGHT_BUTTON,
    "wx.CURSOR_SIZENESW" : wx.CURSOR_SIZENESW,
    "wx.CURSOR_SIZENS" : wx.CURSOR_SIZENS,
    "wx.CURSOR_SIZENWSE" : wx.CURSOR_SIZENWSE,
    "wx.CURSOR_SIZEWE" : wx.CURSOR_SIZEWE,
    "wx.CURSOR_SIZING" : wx.CURSOR_SIZING,
    "wx.CURSOR_SPRAYCAN" : wx.CURSOR_SPRAYCAN,
    "wx.CURSOR_WAIT" : wx.CURSOR_WAIT,
    "wx.CURSOR_WATCH" : wx.CURSOR_WATCH,
    "wx.CURSOR_BLANK" : wx.CURSOR_BLANK,
    "wx.CURSOR_DEFAULT" : wx.CURSOR_DEFAULT,
    "wx.CURSOR_COPY_ARROW" : wx.CURSOR_COPY_ARROW,
    "wx.CURSOR_ARROWWAIT" : wx.CURSOR_ARROWWAIT,
}


#-Classes----------------------------------------------------------------------


class DrawWindow(wx.Window):
    def __init__(self, parent, log, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.Window.__init__(self, parent, id, pos, size, style)
        self.log = log
        self.SetBackgroundColour(wx.WHITE)
        self.lines = []
        self.x = self.y = 0

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP,  self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.DrawSavedLines(dc)

    def DrawSavedLines(self, dc):
        dc.SetPen(wx.Pen(wx.BLUE, 1))
        for line in self.lines:
            for coords in line:
                dc.DrawLine(*coords)

    def OnLeftDown(self, event):
        self.curLine = []
        self.x, self.y = event.GetPosition()
        self.CaptureMouse()

    def OnLeftUp(self, event):
        if self.HasCapture():
            self.lines.append(self.curLine)
            self.curLine = []
            self.ReleaseMouse()

    def OnMotion(self, event):
        if self.HasCapture() and event.Dragging():
            dc = wx.ClientDC(self)
            dc.SetPen(wx.Pen(wx.BLUE, 1))
            evtPos = event.GetPosition()
            coords = (self.x, self.y) + (evtPos.x, evtPos.y)
            self.curLine.append(coords)
            dc.DrawLine(*coords)
            self.x, self.y = event.GetPosition()


class CursorTestPanel(wx.Panel):
    """
    Cursor Test Panel inspired by AniFX cursor test panel.
    """
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1, style=wx.BORDER_SUNKEN)

        # Create all the widgets for the test panel.
        pnl = wx.Panel(self, -1, style=wx.BORDER_SIMPLE)
        pnl.SetBackgroundColour(wx.BLACK)

        self.win = wx.Window(pnl, -1, size=(200, 100))
        self.win.SetBackgroundColour("white")
        self.win.Bind(wx.EVT_LEFT_DOWN, self.OnDrawDot)

        self.drawWin = DrawWindow(pnl, log, size=(200, 100))

        vbSizer0 = wx.BoxSizer(wx.VERTICAL)
        vbSizer0.Add(self.win, 1, wx.EXPAND | wx.BOTTOM, 1)
        vbSizer0.Add(self.drawWin, 1, wx.EXPAND)
        pnl.SetSizer(vbSizer0)

        b = wx.Button(self, -1, 'Button')
        tc = wx.TextCtrl(self, -1, 'Text Ctrl')
        rb1 = wx.RadioButton(self, -1, 'Radio Button 1')
        rb2 = wx.RadioButton(self, -1, 'Radio Button 2')
        cb = wx.CheckBox(self, -1, 'Check Box')
        combo = wx.ComboBox(self, -1, 'One', choices=('One', 'Two', 'Three', 'Four', 'Five'))
        sl = wx.Slider(self, -1)
        sc = wx.SpinCtrl(self, -1)

        # Add all the widgets to a tuple that we will access when changing cursors.
        self.allWidgets = (self, pnl, self.win, self.drawWin, b, tc, rb1, rb2, cb, combo, sl, sc)

        # Do the panel layout.
        vbSizer = wx.BoxSizer(wx.VERTICAL)
        hbSizer = wx.BoxSizer(wx.HORIZONTAL)

        gSizer = wx.GridSizer(rows=4, cols=2, vgap=5, hgap=5)
        gSizer.AddMany((b, tc, rb1, rb2, cb, combo, sl, sc))

        hbSizer.Add(pnl, 0, wx.EXPAND | wx.ALL, 10)
        hbSizer.Add(gSizer, 0, wx.EXPAND | wx.ALL, 10)

        vbSizer.Add(hbSizer, 0, wx.ALL, 10)

        self.SetSizer(vbSizer)

    def OnDrawDot(self, event):
        # Draw a dot so the user can see where the hotspot is.
        dc = wx.ClientDC(self.win)
        dc.SetPen(wx.Pen("RED"))
        dc.SetBrush(wx.Brush("RED"))
        pos = event.GetPosition()
        dc.DrawCircle(pos.x, pos.y, 4)


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        # Create a list of choices from the dictionary above.
        choices = cursors.keys()
        choices = sorted(choices)

        # Create the controls.
        self.cb = wx.ComboBox(self, -1, "wx.CURSOR_DEFAULT", choices=choices,
                              style=wx.CB_READONLY)
        self.tx = wx.StaticText(self, -1, """\
This sample allows you to see all the stock cursors available to wxPython,
and also custom cursors loaded from images, .cur, or .ani files. Simply
select a name from the wx.Choice and then move the mouse into the window
or the widgets below to see the cursor.

NOTE: not all stock cursors have a specific representation on all platforms.
""")

        self.testPanel = CursorTestPanel(self, log)

        # Bind events.
        self.Bind(wx.EVT_COMBOBOX, self.OnChooseCursor, self.cb)

        # Setup the layout.
        vbSizer = wx.BoxSizer(wx.VERTICAL)
        vbSizer.Add(self.tx, 0, wx.ALL, 10)
        vbSizer.Add(self.cb, 0, wx.LEFT | wx.BOTTOM, 10)

        gbs = wx.GridBagSizer(8, 8)
        gbs.Add(self.testPanel, (0, 1), (1, 4), wx.ALIGN_LEFT)
        vbSizer.Add(gbs, 0, wx.ALL)

        self.SetSizer(vbSizer)

        wx.CallAfter(self.cb.SetFocus) # Convienience start for mousewheel switching.

    def OnChooseCursor(self, evt):
        # Clear the dots.
        self.testPanel.win.Refresh()
        self.testPanel.drawWin.lines = []
        self.testPanel.drawWin.Refresh()

        choice = self.cb.GetStringSelection()

        self.log.WriteText("Selecting the %s cursor\n" % choice)

        cnum = cursors[choice]

        if cnum in (ID_PAPERAIRPLANE_ARROW_BLUE,
                    ID_PAPERAIRPLANE_ARROW_RED,
                    ID_PAPERAIRPLANE_ARROW_GREY,
                    ID_PAPERAIRPLANE_ARROW_DARK,
                    ID_PAPERAIRPLANE_ARROW_BLUE_FADEOUT80,
                    ID_PAPERAIRPLANE_ARROW_WHITE,
                    ID_PAPERAIRPLANE_ARROW_COLORSHIFT): # .cur or .ani loose files.

            if choice.endswith('.ani'):
                cursor = wx.Cursor(gFileDir + os.sep + 'cursors' + os.sep + choice, wx.BITMAP_TYPE_ANI)
            if choice.endswith('.cur'):
                cursor = wx.Cursor(gFileDir + os.sep + 'cursors' + os.sep + choice, wx.BITMAP_TYPE_CUR)

        elif cnum == ID_PAPERAIRPLANE_ARROW_WHITE_PNG: # .png loose files.
            image = wx.Image(gFileDir + os.sep + 'cursors' + os.sep + choice, wx.BITMAP_TYPE_PNG)

            # Since these image didn't come from a .cur or .ani file,
            # tell it where the hotspot is.
            image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 0)
            image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 0)
            # Make the image into a cursor.
            cursor = wx.Cursor(image)

        elif cnum in (ID_PAPERAIRPLANE_ARROW_BLUE_PY,
                      ID_PAPERAIRPLANE_ARROW_WHITE_PY): # PyEmbeddedImages
            if cnum == ID_PAPERAIRPLANE_ARROW_BLUE_PY:
                image = paperairplane_arrow_blue24.GetImage()
            elif cnum == ID_PAPERAIRPLANE_ARROW_WHITE_PY:
                image = paperairplane_arrow_white24.GetImage()

            # Since these image didn't come from a .cur or .ani file,
            # tell it where the hotspot is.
            image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 0)
            image.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 0)
            # Make the image into a cursor.
            cursor = wx.Cursor(image)

        else:
            # Create one of the stock (built-in) cursors.
            cursor = wx.Cursor(cnum)

        # Set the cursors for all the testPanels widgets.
        [widget.SetCursor(cursor) for widget in self.testPanel.allWidgets]

    def OnDrawDot(self, evt):
        # Draw a dot so the user can see where the hotspot is.
        dc = wx.ClientDC(self.win)
        dc.SetPen(wx.Pen("RED"))
        dc.SetBrush(wx.Brush("RED"))
        pos = evt.GetPosition()
        dc.DrawCircle(pos.x, pos.y, 3)


#-wxPython Demo----------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


overview = """<html><body>
<h2><center>wx.Cursor</center></h2>

This demo shows the stock mouse cursors that are available to wxPython.

</body></html>
"""


if __name__ == '__main__':
    import os
    import sys
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
