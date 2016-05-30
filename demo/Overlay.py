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

        self.cropbitmap = wx.Bitmap('bitmaps/cropshot24x20.png', wx.BITMAP_TYPE_PNG)

        self.wxPenStylesDict = OrderedDict([
            ('Solid'               , wx.PENSTYLE_SOLID),
            ('Dot'                 , wx.PENSTYLE_DOT),
            ('Long Dash'           , wx.PENSTYLE_LONG_DASH),
            ('Short Dash'          , wx.PENSTYLE_SHORT_DASH),
            ('Dot Dash'            , wx.PENSTYLE_DOT_DASH),
            ('User Dash'           , wx.PENSTYLE_USER_DASH),
            ('Transparent'         , wx.PENSTYLE_TRANSPARENT),
            ('Stipple'             , wx.PENSTYLE_STIPPLE),
            ('BDiagonal Hatch'     , wx.PENSTYLE_BDIAGONAL_HATCH),
            ('CrossDiag Hatch'     , wx.PENSTYLE_CROSSDIAG_HATCH),
            ('FDiagonal Hatch'     , wx.PENSTYLE_FDIAGONAL_HATCH),
            ('Cross Hatch'         , wx.PENSTYLE_CROSS_HATCH),
            ('Horizontal Hatch'    , wx.PENSTYLE_HORIZONTAL_HATCH),
            ('Vertical Hatch'      , wx.PENSTYLE_VERTICAL_HATCH),
            ('First Hatch'         , wx.PENSTYLE_FIRST_HATCH),
            ('Last Hatch'          , wx.PENSTYLE_LAST_HATCH),
        ])

        list = []
        for key, value in self.wxPenStylesDict.items():
            list.append(key)
        self.penstylesCombo = wx.ComboBox(self, -1, choices=list,
                                          pos=(10, 5), size=(100, -1),
                                          style=wx.CB_READONLY)
        self.penstylesCombo.SetSelection(0)
        self.penstylesCombo.SetToolTip('Pen Style')

        self.overlayPenWidth = wx.SpinCtrl(self, -1, value='',
                                           pos=(120, 5),
                                           size=(100, -1),
                                           style=wx.SP_ARROW_KEYS,
                                           min=1, max=24, initial=1)
        self.overlayPenWidth.SetToolTip('Pen Width')

        self.overlayPenColor = wx.ColourPickerCtrl(self, -1, colour=wx.BLUE,
                                                   pos=(230, 5), size=(100, -1))
        self.overlayPenColor.SetToolTip('Pen Color')

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

            dc.SetPen(wx.Pen(colour=self.overlayPenColor.GetColour(),
                             width=self.overlayPenWidth.GetValue(),
                             style=self.wxPenStylesDict[self.penstylesCombo.GetString(self.penstylesCombo.GetSelection())]))
            if 'wxMac' in wx.PlatformInfo:
                dc.SetBrush(wx.Brush(wx.Colour(0xC0, 0xC0, 0xC0, 0x80)))
            else:
                dc.SetBrush(wx.TRANSPARENT_BRUSH)

            dc.DrawRectangle(rect)

            #Draw Pos Text
            ## text = u'%s'%evtPos
            ## width, height = dc.GetTextExtent(text)
            ## dc.DrawText(text, x=evtPos[0]+2, y=evtPos[1]-height)

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
        x, y = self.GetSize()
        if x <= 0 or y <= 0:
            return

        self.buffer = wx.Bitmap(x, y)

        dc = wx.MemoryDC()
        dc.SelectObject(self.buffer)
        dc.SetBackground(self.background)
        dc.Clear()

        dc.DrawBitmap(wx.Bitmap('bitmaps/snakey_render.png'), 10, 35)
        dc.DrawBitmap(wx.Bitmap('bitmaps/honeycomb300.png'), 100, 210)

        del dc
        self.Refresh()
        self.Update()

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
