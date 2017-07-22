import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class radiobox_Tests(wtc.WidgetTestCase):

    def test_radioboxCtor(self):
        r = wx.RadioBox(self.frame, label='Label', choices='one two three four'.split(),
                        majorDimension=2)

    def test_radioboxDefaultCtor(self):
        r = wx.RadioBox()
        r.Create(self.frame, label='Label', choices='one two three four'.split(),
                        majorDimension=2, style=wx.RA_SPECIFY_ROWS)

    def test_radioboxTweaks(self):
        r = wx.RadioBox(self.frame, label='Label', choices='one two three four'.split(),
                        majorDimension=2)
        r.SetItemLabel(0, 'ZERO')
        self.assertTrue(r.GetItemLabel(0) == 'ZERO')

        r.Enable(False)
        r.Enable(True)
        r.EnableItem(1, False)
        r.ShowItem(2, False)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
