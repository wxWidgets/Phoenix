import unittest
from unittests import wtc
import wx
import wx.adv


#---------------------------------------------------------------------------

class odcombo_Tests(wtc.WidgetTestCase):

    def test_odcombo1(self):
        wx.adv.ODCB_DCLICK_CYCLES
        wx.adv.ODCB_STD_CONTROL_PAINT
        wx.adv.ODCB_PAINTING_CONTROL
        wx.adv.ODCB_PAINTING_SELECTED


    def test_odcombo2(self):
        class MyODCombo(wx.adv.OwnerDrawnComboBox):
            def __init__(self, *args, **kw):
                wx.adv.OwnerDrawnComboBox.__init__(self, *args, **kw)

                self._OnDrawBackground_Called = False
                self._OnDrawItem_Called = False
                self._OnMeasureItem_Called = False
                self._OnMeasureItemWidth_Called = False

            def OnDrawBackground(self, dc, rect, item, flags):
                self._OnDrawBackground_Called = True
                wx.adv.OwnerDrawnComboBox.OnDrawBackground(self, dc, rect, item, flags)

            def OnDrawItem(self, dc, rect, item, flags):
                self._OnDrawItem_Called = True
                wx.adv.OwnerDrawnComboBox.OnDrawItem(self, dc, rect, item, flags)

            def OnMeasureItem(self, item):
                self._OnMeasureItem_Called = True
                return wx.adv.OwnerDrawnComboBox.OnMeasureItem(self, item)

            def OnMeasureItemWidth(self, item):
                self._OnMeasureItemWidth_Called = True
                return wx.adv.OwnerDrawnComboBox.OnMeasureItemWidth(self, item)


        pnl = wx.Panel(self.frame)
        cb = MyODCombo(pnl, pos=(10,10))
        cb.Append("one two three four".split())
        cb.SetSelection(2)
        self.assertEqual(cb.GetSelection(), 2)
        self.assertEqual(cb.GetString(1), 'two')

        self.waitFor(100)
        cb.Popup()
        self.waitFor(100)
        cb.Dismiss()
        self.myYield()

        self.assertTrue(cb._OnDrawBackground_Called)
        self.assertTrue(cb._OnDrawItem_Called)
        self.assertTrue(cb._OnMeasureItemWidth_Called)
        self.assertTrue(cb._OnMeasureItem_Called)


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
