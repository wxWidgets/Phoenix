#!/usr/bin/env python

import wx
import os

#----------------------------------------------------------------------
class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent)

        # Event Handlers
        self.Bind(wx.EVT_PAINT, self.OnPaint)


    def OnPaint(self, event):
        dc = wx.GCDC(wx.PaintDC(self))
        #dc = wx.PaintDC(self)
        render = wx.RendererNative.Get()

        # Setup Brushes
        dc.SetBrush(wx.BLACK_BRUSH)
        dc.SetTextForeground(wx.BLACK)
        dc.SetFont(wx.NORMAL_FONT)

        # The below code will use RendererNative to draw controls in
        # various states. The wx.CONTROL_* flags are used to tell the
        # Renderer which state to draw the control in.

        # Draw some checkboxes
        cb_lbl = "DrawCheckBoxes:"
        dc.DrawText(cb_lbl, 15, 15)
        render.DrawCheckBox(self, dc, (25, 35, 16, 16), wx.CONTROL_CHECKED)
        render.DrawCheckBox(self, dc, (45, 35, 16, 16), wx.CONTROL_CHECKABLE)
        render.DrawCheckBox(self, dc, (65, 35, 16, 16))
        render.DrawCheckBox(self, dc, (85, 35, 16, 16), wx.CONTROL_CHECKED | wx.CONTROL_DISABLED)

        lbl = "DrawRadioBitmap:"
        dc.DrawText(lbl, 375, 15)
        render.DrawRadioBitmap(self, dc, (385, 35, 16, 16), wx.CONTROL_CHECKED)
        render.DrawRadioBitmap(self, dc, (405, 35, 16, 16), wx.CONTROL_CHECKABLE)
        render.DrawRadioBitmap(self, dc, (425, 35, 16, 16))
        render.DrawRadioBitmap(self, dc, (445, 35, 16, 16), wx.CONTROL_CHECKED | wx.CONTROL_DISABLED)

        # Draw ComboBoxDropButton
        xpos = self.GetTextExtent(cb_lbl)[0] + 40
        cb_lbl = "DrawComboBoxDropButton:"
        dc.DrawText(cb_lbl, xpos, 15)
        render.DrawComboBoxDropButton(self, dc, (xpos + 4, 35, 24, 24), wx.CONTROL_CURRENT)
        render.DrawComboBoxDropButton(self, dc, (xpos + 44, 35, 24, 24), wx.CONTROL_PRESSED)
        render.DrawComboBoxDropButton(self, dc, (xpos + 84, 35, 24, 24), wx.CONTROL_CURRENT | wx.CONTROL_DISABLED)
        render.DrawComboBoxDropButton(self, dc, (xpos + 124, 35, 24, 24), wx.CONTROL_PRESSED | wx.CONTROL_DISABLED)

        # Draw DropArrow
        da_lbl = "DrawDropArrow:"
        dc.DrawText(da_lbl, 15, 80)
        render.DrawDropArrow(self, dc, (15, 100, 24, 24), wx.CONTROL_CURRENT)
        render.DrawDropArrow(self, dc, (35, 100, 24, 24), wx.CONTROL_PRESSED)
        render.DrawDropArrow(self, dc, (55, 100, 24, 24), wx.CONTROL_CURRENT | wx.CONTROL_DISABLED)

        # Draw HeaderButton
        dc.DrawText("DrawHeaderButton:", xpos, 80)
        # Set some extra options for drawing
        opts = wx.HeaderButtonParams()
        hb_lbl = "HeaderButton Selected"
        opts.m_labelText = hb_lbl
        render.DrawHeaderButton(self, dc, (xpos, 100, self.GetTextExtent(hb_lbl)[0] + 30, 16),
                                wx.CONTROL_SELECTED, wx.HDR_SORT_ICON_DOWN, opts)
        hb_lbl = "HeaderButton Normal"
        opts.m_labelText = hb_lbl
        render.DrawHeaderButton(self, dc, (xpos, 125, self.GetTextExtent(hb_lbl)[0] + 30, 16),
                                sortArrow=wx.HDR_SORT_ICON_UP, params=opts)

        hb_lbl = "HeaderButton Current"
        opts.m_labelText = hb_lbl
        render.DrawHeaderButton(self, dc, (xpos, 150, self.GetTextExtent(hb_lbl)[0] + 30, 16),
                                wx.CONTROL_CURRENT, params=opts)

        # Draw ItemSelectionRect
        isr_lbl = "DrawItemSelectionRect:"
        dc.DrawText(isr_lbl, 15, 185)
        render.DrawItemSelectionRect(self, dc, (15, 205, 40, 24), wx.CONTROL_SELECTED)
        render.DrawItemSelectionRect(self, dc, (65, 205, 40, 24), wx.CONTROL_CURRENT)
        render.DrawItemSelectionRect(self, dc, (115, 205, 40, 24), wx.CONTROL_FOCUSED)

        # DrawPushButton
        pb_lbl = "DrawPushButton:"
        dc.DrawText(pb_lbl, 15, 255)
        render.DrawPushButton(self, dc, (15, 275, 45, 24), wx.CONTROL_CURRENT)
        render.DrawPushButton(self, dc, (70, 275, 45, 24), wx.CONTROL_PRESSED | wx.CONTROL_SELECTED)
        render.DrawPushButton(self, dc, (125, 275, 45, 24), wx.CONTROL_ISDEFAULT)
        render.DrawPushButton(self, dc, (180, 275, 45, 24), wx.CONTROL_CURRENT | wx.CONTROL_DISABLED)

        # DrawTreeItemButton
        ti_lbl = "DrawTreeItemButton:"
        dc.DrawText(ti_lbl, 15, 330)
        render.DrawTreeItemButton(self, dc, (15, 350, 16, 16))
        render.DrawTreeItemButton(self, dc, (45, 350, 16, 16), wx.CONTROL_EXPANDED)

        # DrawComboBox
        dc.DrawText("DrawComboBox:", 270, 185)
        render.DrawComboBox(self, dc, (270, 205, 100, 21))
        render.DrawComboBox(self, dc, (270, 230, 100, 21), wx.CONTROL_DISABLED)
        render.DrawComboBox(self, dc, (270, 255, 100, 21), wx.CONTROL_CURRENT)
        render.DrawComboBox(self, dc, (270, 280, 100, 21), wx.CONTROL_PRESSED | wx.CONTROL_SELECTED)
        render.DrawComboBox(self, dc, (270, 305, 100, 21), wx.CONTROL_FOCUSED)

        # DrawChoice
        dc.DrawText("DrawChoice:", 400, 185)
        render.DrawChoice(self, dc, (400, 205, 100, 21))
        render.DrawChoice(self, dc, (400, 230, 100, 21), wx.CONTROL_DISABLED)
        render.DrawChoice(self, dc, (400, 255, 100, 21), wx.CONTROL_CURRENT)
        render.DrawChoice(self, dc, (400, 280, 100, 21), wx.CONTROL_PRESSED | wx.CONTROL_SELECTED)
        render.DrawChoice(self, dc, (400, 305, 100, 21), wx.CONTROL_FOCUSED)

        # DrawTextCtrl
        dc.DrawText("DrawTextCtrl:", 270, 350)
        render.DrawTextCtrl(self, dc, (270, 375, 100, 21))
        render.DrawTextCtrl(self, dc, (380, 375, 100, 21), wx.CONTROL_FOCUSED)

        # DrawItemText
        render.DrawItemText(self, dc, 'DrawItemText: wx.CONTROL_ISDEFAULT', (270, 420, 300, 21), align=wx.ALIGN_LEFT|wx.ALIGN_TOP, flags=wx.CONTROL_ISDEFAULT, ellipsizeMode=wx.ELLIPSIZE_END)
        render.DrawItemText(self, dc, 'DrawItemText: wx.CONTROL_SELECTED', (270, 440, 300, 21), align=wx.ALIGN_LEFT|wx.ALIGN_TOP, flags=wx.CONTROL_SELECTED, ellipsizeMode=wx.ELLIPSIZE_END)
        render.DrawItemText(self, dc, 'DrawItemText: wx.CONTROL_DISABLED', (270, 460, 300, 21), align=wx.ALIGN_LEFT|wx.ALIGN_TOP, flags=wx.CONTROL_DISABLED, ellipsizeMode=wx.ELLIPSIZE_END)

        # DrawGauge
        dc.DrawText("DrawGauge:", 15, 380)
        render.DrawGauge(self, dc, (15, 400, 100, 21), value=20, max= 100, flags=wx.CONTROL_ISDEFAULT)
        render.DrawGauge(self, dc, (15, 430, 100, 21), value=20, max= 100, flags=wx.CONTROL_DISABLED)
        render.DrawGauge(self, dc, (15, 460, 100, 21), value=20, max= 100, flags=wx.CONTROL_CURRENT)
        render.DrawGauge(self, dc, (15, 490, 100, 21), value=20, max= 100, flags=wx.CONTROL_FOCUSED)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------

overview = """<html><body>
<h2><center>wx.RendererNative</center></h2>
<p>wx.RendererNative is a class which virtualizes drawing. It abstracts the
operations of drawing controls and allows you to draw say, a button, without
caring about exactly how it is done, in a native and platform independent way.
</p>

<p>All drawing functions take some standard parameters:<p>
<ul>
<li><b>win</b>: is the window being drawn.</li>
<li><b>dc</b>: is the wxDC to draw on. Only this device context should be used
               for drawing.</li>
<li><b>rect</b>: The bounding rectangle for the element to be drawn.</li>
<li><b>flags</b>: The optional flags (none by default) which can be a
                  combination of the wx.CONTROL_XXX constants.</li>
</ul>

<p><b>Note</b>: Each drawing function restores the wxDC attributes if it
changes them, so it is safe to assume that the same pen, brush and colours
that were active before the call to this function are still in effect
after it.</p>
</body></html>
"""

#----------------------------------------------------------------------

if __name__ == '__main__':
    import sys
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
