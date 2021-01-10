import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class vlbox_Tests(wtc.WidgetTestCase):

    def test_vlbox1(self):
        with self.assertRaises(TypeError):
            lb = wx.VListBox()

    def test_vlbox2(self):
        with self.assertRaises(TypeError):
            lb = wx.VListBox(self.frame)


    def test_vlbox3(self):
        panel = wx.Panel(self.frame)
        self.frame.SendSizeEvent()

        lb = MyVListBox(panel, pos=(10,10), size=(100,150), style=wx.BORDER_THEME)
        lb.data = ['zero', 'one two', 'three four', 'five six', 'seven eight', 'nine ten']
        lb.SetItemCount(len(lb.data))
        self.waitFor(100)

        # check the ItemCount property
        self.assertEqual(len(lb.data), lb.ItemCount)

        # check that the overridden virtuals were called
        self.assertTrue(len(lb.drawItemCalls) > 0)
        self.assertTrue(len(lb.drawBackgroundCalls) > 0)
        self.assertTrue(len(lb.drawSeparatorCalls) > 0)
        self.assertTrue(len(lb.measureItemCalls) > 0)

        lb.SetSelection(2)
        self.waitFor(50)
        self.assertEqual(lb.GetSelectedCount(), 1)
        self.assertEqual(lb.GetSelection(), 2)
        self.assertTrue(lb.IsSelected(2))
        self.assertFalse(lb.IsSelected(3))



    def test_vlbox4(self):
        panel = wx.Panel(self.frame)
        self.frame.SendSizeEvent()

        lb = MyVListBox(panel, pos=(10,10), size=(100,150),
                        style=wx.BORDER_SIMPLE|wx.LB_MULTIPLE)
        lb.data = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        lb.SetItemCount(len(lb.data))
        self.waitFor(50)

        lb.Select(2)
        lb.Select(5)
        lb.Select(7)
        lb.Select(8)
        self.waitFor(50)

        self.assertTrue(lb.IsSelected(2))
        self.assertTrue(lb.IsSelected(8))
        self.assertFalse(lb.IsSelected(3))

        sel = list()
        idx, cookie = lb.GetFirstSelected()
        while idx != wx.NOT_FOUND:
            sel.append(idx)
            idx, cookie = lb.GetNextSelected(cookie)

        self.assertEqual(sel, [2,5,7,8])



class MyVListBox(wx.VListBox):
    def __init__(self, *args, **kw):
        wx.VListBox.__init__(self, *args, **kw)
        self.data = list()
        self.drawItemCalls = list()
        self.drawBackgroundCalls = list()
        self.drawSeparatorCalls = list()
        self.measureItemCalls = list()

    # overridable methods
    def OnDrawItem(self, dc, rect, idx):
        self.drawItemCalls.append(idx)
        assert isinstance(dc, wx.DC)
        color = 'black'
        if self.IsSelected(idx):
            color = 'white'
        dc.SetTextForeground(color)
        dc.DrawLabel(self.data[idx], rect)

    def OnDrawBackground(self, dc, rect, idx):
        self.drawBackgroundCalls.append(idx)
        assert isinstance(dc, wx.DC)
        color = 'white'
        if self.IsSelected(idx):
            color = self.GetSelectionBackground()
            if not color.IsOk():
                color = 'navy'
        dc.SetPen(wx.Pen(color, 1))
        dc.SetBrush(wx.Brush(color))
        dc.DrawRectangle(rect)

    def OnDrawSeparator(self, dc, rect, idx):
        self.drawSeparatorCalls.append(idx)
        if idx == 0:
            return
        assert isinstance(dc, wx.DC)
        dc.SetPen(wx.Pen('#c0c0c0', 1, wx.PENSTYLE_DOT_DASH))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        assert isinstance(rect, wx.Rect)
        dc.DrawLine(rect.x, rect.y, rect.right, rect.y)
        rect.y += 1
        rect.height -= 2

    def OnMeasureItem(self, idx):
        self.measureItemCalls.append(idx)
        #dc = wx.ClientDC(self)
        w, h = self.GetTextExtent(self.data[idx])
        return h + 6


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
