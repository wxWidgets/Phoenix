#!/usr/bin/env python

from collections import OrderedDict

import wx

#---------------------------------------------------------------------------


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, wx.ID_ANY, style=wx.CLIP_CHILDREN)

        ## self.SetDoubleBuffered(True)

        self.background = wx.Brush(self.GetBackgroundColour())
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        #--Rubberband Overlay
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.startPos = None
        self.endPos = None
        self.overlay = wx.Overlay()

        self.cropbitmap = wx.Bitmap('bitmaps/cropshot24x20.png')
        self.honeyBitmap = wx.Bitmap('bitmaps/honeycomb300.png')

        self.wxPenStylesDict = OrderedDict([
            ('Solid'               , wx.PENSTYLE_SOLID),
            ('Dot'                 , wx.PENSTYLE_DOT),
            ('Long Dash'           , wx.PENSTYLE_LONG_DASH),
            ('Short Dash'          , wx.PENSTYLE_SHORT_DASH),
            ('Dot Dash'            , wx.PENSTYLE_DOT_DASH),
            ('User Dash'           , wx.PENSTYLE_USER_DASH),
            ('Transparent'         , wx.PENSTYLE_TRANSPARENT),
            #('Stipple'             , wx.PENSTYLE_STIPPLE),
            ('BDiagonal Hatch'     , wx.PENSTYLE_BDIAGONAL_HATCH),
            ('CrossDiag Hatch'     , wx.PENSTYLE_CROSSDIAG_HATCH),
            ('FDiagonal Hatch'     , wx.PENSTYLE_FDIAGONAL_HATCH),
            ('Cross Hatch'         , wx.PENSTYLE_CROSS_HATCH),
            ('Horizontal Hatch'    , wx.PENSTYLE_HORIZONTAL_HATCH),
            ('Vertical Hatch'      , wx.PENSTYLE_VERTICAL_HATCH),
        ])

        list = []
        for key, value in self.wxPenStylesDict.items():
            list.append(key)
        self.penstylesCombo = wx.ComboBox(self, -1, choices=list,
                                          size=(150, -1),
                                          style=wx.CB_READONLY)
        self.penstylesCombo.SetSelection(0)
        self.penstylesCombo.SetToolTip('Pen Style')

        self.overlayPenWidth = wx.SpinCtrl(self, -1, value='',
                                           style=wx.SP_ARROW_KEYS,
                                           min=1, max=24, initial=1)
        self.overlayPenWidth.SetToolTip('Pen Width')

        from wx.lib.colourselect import ColourSelect
        self.overlayPenColor = ColourSelect(self, -1, colour=wx.BLUE)
        self.overlayPenColor.SetToolTip('Pen Color')

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.penstylesCombo, 0, wx.ALL, 5)
        sizer.Add(self.overlayPenWidth, 0, wx.ALL, 5)
        sizer.Add(self.overlayPenColor, 0, wx.ALL, 5)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(sizer, 0)
        box.Add((1,1), 1)

        self.SetSizer(box)

        self.OnSize()


    def OnLeftDown(self, event):
        # Capture the mouse and save the starting posiiton for the rubber-band
        self.CaptureMouse()
        self.startPos = event.GetPosition()
        ## print('self.startPos:', self.startPos)
        self.SetFocus()
        ## print('OnLeftDown')


    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            evtPos = event.GetPosition()

            try:
                rect = wx.Rect(topLeft=self.startPos, bottomRight=evtPos)
            except TypeError as exc:  # topLeft = NoneType. Attempting to double click image or something
                return
            except Exception as exc:
                raise exc

            # Draw the rubber-band rectangle using an overlay so it
            # will manage keeping the rectangle and the former window
            # contents separate.
            dc = wx.ClientDC(self)
            odc = wx.DCOverlay(self.overlay, dc)
            odc.Clear()

            # Mac's DC is already the same as a GCDC, and it causes
            # problems with the overlay if we try to use an actual
            # wx.GCDC so don't try it.  If you do not need to use a
            # semi-transparent background then you can leave this out.
            if 'wxMac' not in wx.PlatformInfo:
                dc = wx.GCDC(dc)

            # Set the pen, for the box's border
            dc.SetPen(wx.Pen(colour=self.overlayPenColor.GetColour(),
                             width=self.overlayPenWidth.GetValue(),
                             style=self.wxPenStylesDict[self.penstylesCombo.GetString(self.penstylesCombo.GetSelection())]))

            # Create a brush (for the box's interior) with the same colour,
            # but 50% transparency.
            bc = self.overlayPenColor.GetColour()
            bc = wx.Colour(bc.red, bc.green, bc.blue, 0x80)
            dc.SetBrush(wx.Brush(bc))

            # Draw the rectangle
            dc.DrawRectangle(rect)

            if evtPos[0] < self.startPos[0]:  # draw on left side of rect, not inside it
                dc.DrawBitmap(self.cropbitmap,
                              evtPos[0] - 25 - self.overlayPenWidth.GetValue(),
                              evtPos[1] - 17)
            else:
                dc.DrawBitmap(self.cropbitmap,
                              evtPos[0] + 2 + self.overlayPenWidth.GetValue(),
                              evtPos[1] - 17)

            del odc  # Make sure the odc is destroyed before the dc is.
            ## print('OnMouseMove')


    def OnLeftUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        self.endPos = event.GetPosition()
        ## print('StartPos: %s' %self.startPos)
        ## print('EndPos: %s' %self.endPos)
        self.startPos = None
        self.endPos = None

        # When the mouse is released we reset the overlay and it
        # restores the former content to the window.
        dc = wx.ClientDC(self)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        del odc
        self.overlay.Reset()
        ## print('OnLeftUp')


    def OnSize(self, event=None):
        if event:
            event.Skip()

        x, y = self.GetSize()
        if x <= 0 or y <= 0:
            return

        self.buffer = wx.Bitmap(x, y)

        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        dc.SetBackground(self.background)
        dc.Clear()

        dc.DrawBitmap(self.honeyBitmap, 40, 40)
        dc.SetFont(wx.Font(wx.FontInfo(18)))
        dc.DrawText('Drag the mouse on this window.', 325, 100)

        del dc
        self.Refresh()
        #self.Update()

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)


#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------


overview = """\
Creates an overlay over an existing window, allowing for
 manipulations like rubberbanding, etc
"""


if __name__ == '__main__':
    import sys
    import os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
