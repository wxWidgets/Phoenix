import wx
import images


pen_styles = ["wx.SOLID", "wx.TRANSPARENT", "wx.DOT", "wx.LONG_DASH",
              "wx.SHORT_DASH", "wx.DOT_DASH", "wx.BDIAGONAL_HATCH",
              "wx.CROSSDIAG_HATCH", "wx.FDIAGONAL_HATCH", "wx.CROSS_HATCH",
              "wx.HORIZONTAL_HATCH", "wx.VERTICAL_HATCH", "wx.USER_DASH"]
if 'wxMSW' in wx.PlatformInfo:
    pen_styles.append("wx.STIPPLE")

brush_styles = ["wx.SOLID", "wx.TRANSPARENT", "wx.STIPPLE", "wx.BDIAGONAL_HATCH",
                "wx.CROSSDIAG_HATCH", "wx.FDIAGONAL_HATCH", "wx.CROSS_HATCH",
                "wx.HORIZONTAL_HATCH", "wx.VERTICAL_HATCH"]




class BasePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER|wx.WANTS_CHARS)

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)

        self.Bind(wx.EVT_SIZE, self.OnSize)        
        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnSize(self, event):
        event.Skip()
        self.Refresh()


class PenPanel(BasePanel):

    def __init__(self, parent, pen_name):
        BasePanel.__init__(self, parent)
        self.pen_name = pen_name
        

    def OnPaint(self, event):
        width, height = self.GetClientSize()

        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.MakeSmaller()
        dc.SetFont(font)
        w, labelHeight = dc.GetTextExtent('Wy')
        
        name = self.pen_name        

        if "STIPPLE" in name:
            bmp = images.Smiles.GetBitmap()
            penWidth = 8 #bmp.GetHeight()
            pen = wx.Pen(wx.BLUE, penWidth, eval(name))
            pen.SetStipple(bmp)
        else:
            penWidth = 3
            if 'HATCH' in name:
                penWidth = 8
            pen = wx.Pen(wx.BLUE, penWidth, eval(name))

        if "USER" in name:
            # dash values represent units on, off, on. off...
            pen.SetDashes([2, 5, 2, 2])
            name += " ([2, 5, 2, 2])"
        
        dc.SetTextForeground(wx.BLACK)
        dc.DrawText(name, 1, 1)

        dc.SetPen(pen)
        y = labelHeight + (height - labelHeight)/2
        dc.DrawLine(5, y, width-5, y)


class BrushPanel(BasePanel):
    def __init__(self, parent, brush_name):
        BasePanel.__init__(self, parent)
        self.brush_name = brush_name
        

    def OnPaint(self, event):
        width, height = self.GetClientSize()

        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.MakeSmaller()
        dc.SetFont(font)
        w, labelHeight = dc.GetTextExtent('Wy')

        dc.SetPen(wx.TRANSPARENT_PEN)        
        name = self.brush_name
        
        if "STIPPLE" in name:
            bmp = images.Smiles.GetBitmap()
            bmp.SetMask(None)
            brush = wx.BrushFromBitmap(bmp)
        else:
            brush = wx.Brush(wx.BLUE, eval(name))
        
        dc.SetTextForeground(wx.BLACK)
        dc.DrawText(name, 1, 1)

        dc.SetBrush(brush)
        dc.DrawRectangle(5, labelHeight+2, width-10, height-labelHeight-5-2)



class TestPanel(wx.Panel):
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.BOLD)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        label1 = wx.StaticText(self, -1, "Pen Styles:")
        label1.SetFont(font)

        mainSizer.Add(label1, 0, wx.EXPAND|wx.ALL, 10)
        
        gs1 = wx.GridSizer(4, 4, 3, 3)  # rows, cols, vgap, hgap

        for pen_name in pen_styles:
            small = PenPanel(self, pen_name)
            gs1.Add(small, 0, wx.EXPAND)

        mainSizer.Add(gs1, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)

        label2 = wx.StaticText(self, -1, "Brush Styles:")
        label2.SetFont(font)

        mainSizer.Add(label2, 0, wx.EXPAND|wx.ALL, 10)
        
        gs2 = wx.GridSizer(3, 3, 3, 3)  # rows, cols, vgap, hgap

        for brush_name in brush_styles:
            small = BrushPanel(self, brush_name)
            gs2.Add(small, 0, wx.EXPAND)

        mainSizer.Add(gs2, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 10)
        
        self.SetSizer(mainSizer)
       



#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>Pen and Brush Styles</center></h2>

This sample shows an e3xample of drawing with each of the available
wx.Pen and wx.Brush styles.

</body></html>
"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])



