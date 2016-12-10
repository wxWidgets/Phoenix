"""
A simple sample of using a wx.Overlay to draw a rubberband effect
"""

import wx
print(wx.version())

class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

        self.startPos = None
        self.overlay = wx.Overlay()

        wx.TextCtrl(self, pos=(140,20))


    def OnPaint(self, evt):
        # Just some simple stuff to paint in the window for an example
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("sky blue"))
        dc.Clear()
        dc.DrawLabel("Drag the mouse across this window to see \n"
                     "a rubber-band effect using wx.Overlay",
                     (140, 50, -1, -1))

        coords = ((40,40),(200,220),(210,120),(120,300))
        dc = wx.GCDC(dc)
        dc.SetPen(wx.Pen("red", 2))
        dc.SetBrush(wx.CYAN_BRUSH)
        dc.DrawPolygon(coords)


    def OnLeftDown(self, evt):
        # Capture the mouse and save the starting position for the
        # rubber-band
        self.CaptureMouse()
        self.startPos = evt.GetPosition()


    def OnMouseMove(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            rect = wx.Rect(topLeft=self.startPos, bottomRight=evt.GetPosition())

            # Draw the rubber-band rectangle using an overlay so it
            # will manage keeping the rectangle and the former window
            # contents separate.
            dc = wx.ClientDC(self)
            odc = wx.DCOverlay(self.overlay, dc)
            odc.Clear()

            # Mac's DC is already the same as a GCDC, and it causes
            # problems with the overlay if we try to use an actual
            # wx.GCDC so don't try it.
            if 'wxMac' not in wx.PlatformInfo:
                dc = wx.GCDC(dc)

            dc.SetPen(wx.Pen("black", 2))
            dc.SetBrush(wx.Brush(wx.Colour(0xC0, 0xC0, 0xC0, 0x80)))
            dc.DrawRectangle(rect)


    def OnLeftUp(self, evt):
        if self.HasCapture():
            self.ReleaseMouse()
        self.startPos = None

        # When the mouse is released we reset the overlay and it
        # restores the former content to the window.
        dc = wx.ClientDC(self)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        del odc
        self.overlay.Reset()



app = wx.App(redirect=False)
frm = wx.Frame(None, title="wx.Overlay Test", size=(450,450))
#frm.SetDoubleBuffered(True)
pnl = TestPanel(frm)
frm.Show()
app.MainLoop()
