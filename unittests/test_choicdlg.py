import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class choicdlg_Tests(wtc.WidgetTestCase):

    def test_choicdlgSingle(self):
        d = wx.SingleChoiceDialog(self.frame, 'message', 'caption',
                                  choices="one two three four five".split())
        d.SetSelection(2)
        d.Destroy()

    def test_choicdlgSingleFunc(self):
        wx.GetSingleChoice


    def test_choicdlgMulti(self):
        d = wx.MultiChoiceDialog(self.frame, 'message', 'caption',
                                 choices="one two three four five".split())
        d.SetSelections([2, 4])
        s = d.GetSelections()
        #self.assertEqual(s, [2,4])   the internal list isn't updated right away, can't test this here
        d.Destroy()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
