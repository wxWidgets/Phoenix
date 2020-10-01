import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class sizer_Tests(wtc.WidgetTestCase):

    def test_sizerBox(self):
        bs = wx.BoxSizer()

    def test_sizerStatBox(self):
        sbs1 = wx.StaticBoxSizer(wx.StaticBox(self.frame, label='label'), wx.VERTICAL)
        sbs2 = wx.StaticBoxSizer(wx.HORIZONTAL, self.frame, 'label')

    def test_sizerGrid(self):
        gs1 = wx.GridSizer(4, 5, 6)
        gs2 = wx.GridSizer(4, (5,6))
        gs3 = wx.GridSizer(cols=4, hgap=5, vgap=6)

    def test_sizerFlexGrid(self):
        fgs1 = wx.FlexGridSizer(4, 5, 6)
        fgs2 = wx.FlexGridSizer(4, (5,6))
        fgs3 = wx.FlexGridSizer(cols=4, hgap=5, vgap=6)

    def test_sizerFlexGrid2(self):
        fgs = wx.FlexGridSizer(cols=4, hgap=5, vgap=6)
        for x in range(20):
            fgs.Add(wx.StaticText(self.frame, -1, str(x)))
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableCol(3, 2)
        fgs.AddGrowableRow(2)
        fgs.RemoveGrowableRow(2)

        self.frame.SetSizer(fgs)
        self.frame.Layout()

        widths = fgs.GetColWidths()
        heights = fgs.GetRowHeights()
        self.assertEqual(4, len(widths))
        self.assertEqual(5, len(heights))


    def test_sizer2(self):
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(wx.Panel(self.frame))
        s2 = wx.BoxSizer()
        s.Add(s2)
        self.frame.SetSizer(s)

    def test_sizerUserData(self):
        bs = wx.BoxSizer()
        si = bs.Add(wx.Panel(self.frame), userData="MyData")
        self.assertTrue(si.GetUserData() == "MyData")

    def test_sizerFlags(self):
        bs = wx.BoxSizer()
        bs.Add(wx.Panel(self.frame),
               wx.SizerFlags(2).Border(wx.ALL, 5).Align(wx.ALIGN_TOP))

    def test_sizerAddMany(self):
        bs = wx.BoxSizer()
        bs.AddMany([ wx.Panel(self.frame),                  # item w/o tuple
                     (5,10),                                # spacer
                     (wx.Panel(self.frame), 1, wx.ALL, 5),  # item in tuple w/ other args
                     ])
        items = bs.GetChildren()
        self.assertTrue(len(items) == 3)
        self.assertTrue(isinstance(items[0], wx.SizerItem))
        self.assertTrue(items[0].IsWindow())
        self.assertTrue(items[1].IsSpacer())
        self.assertTrue(items[2].Border == 5)

    def test_iter(self):
        bs = wx.BoxSizer()
        widgetlist = [wx.Panel(self.frame) for _ in range(5)]
        for w in widgetlist:
            bs.Add(w)

        sizeritems = [x for x in bs]
        for item in sizeritems:
            self.assertTrue(isinstance(item, wx.SizerItem))

        self.assertEqual([x.GetWindow() for x in bs], widgetlist)

    def test_sizerSpacers1(self):
        bs = wx.BoxSizer()
        w = 5
        h = 10
        bs.Add(w, h)
        bs.Add( (w, h) )
        bs.Add(wx.Size(w,h))

    def test_sizerSpacers2(self):
        bs = wx.BoxSizer()
        w = 5
        h = 10
        bs.Add(w, h, wx.SizerFlags(1))
        bs.Add( (w, h), wx.SizerFlags(2) )
        bs.Add(wx.Size(w,h), wx.SizerFlags(3))

    def test_sizerSpacers3(self):
        bs = wx.BoxSizer()
        w = 5
        h = 10
        bs.Prepend(w, h)
        bs.Prepend( (w, h) )
        bs.Prepend(wx.Size(w,h))

    def test_sizerSpacers4(self):
        bs = wx.BoxSizer()
        w = 5
        h = 10
        bs.Prepend(w, h, wx.SizerFlags(1))
        bs.Prepend( (w, h), wx.SizerFlags(2) )
        bs.Prepend(wx.Size(w,h), wx.SizerFlags(3))

    def test_sizerSpacers5(self):
        bs = wx.BoxSizer()
        w = 5
        h = 10
        bs.Insert(0, w, h)
        bs.Insert(0, (w, h) )
        bs.Insert(0, wx.Size(w,h))

    def test_sizerSpacers6(self):
        bs = wx.BoxSizer()
        w = 5
        h = 10
        bs.Insert(0, w, h, wx.SizerFlags(1))
        bs.Insert(0, (w, h), wx.SizerFlags(2) )
        bs.Insert(0, wx.Size(w,h), wx.SizerFlags(3))

    def test_sizerOrientation(self):
        bs = wx.BoxSizer(wx.HORIZONTAL)
        self.assertEqual(bs.GetOrientation(), wx.HORIZONTAL)
        bs.SetOrientation(wx.VERTICAL)
        self.assertEqual(bs.Orientation, wx.VERTICAL)

    def test_sizerBool(self):
        # Test if deleted sizers evaluate to False
        bs = wx.BoxSizer()
        self.assertTrue(bs)
        bs.Destroy()
        self.assertFalse(bs)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
