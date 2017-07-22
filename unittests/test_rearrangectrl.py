import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class rearrangectrl_Tests(wtc.WidgetTestCase):

    def test_rearrangectrl1(self):
        rl = wx.RearrangeList(self.frame, order=[0,1,2], items=['one', 'two', 'three'])

        order1 = rl.GetCurrentOrder()
        self.assertTrue(isinstance(order1, list))
        rl.SetSelection(1)
        rl.MoveCurrentDown()
        order2 = rl.GetCurrentOrder()
        self.assertNotEqual(order1, order2)

    def test_rearrangectrl2(self):
        rl = wx.RearrangeList()
        rl.Create(self.frame, order=[1,2,0], items=['one', 'two', 'three'])


    def test_rearrangectrl3(self):
        rc = wx.RearrangeCtrl(self.frame, order=[0,1,2], items=['one', 'two', 'three'])

    def test_rearrangectrl4(self):
        rc = wx.RearrangeCtrl()
        rc.Create(self.frame, order=[1,2,0], items=['one', 'two', 'three'])


    def test_rearrangectrl5(self):
        rd = wx.RearrangeDialog(self.frame, 'message', 'title',
                                  order=[0,1,2], items=['one', 'two', 'three'])
        rd.Destroy()

    def test_rearrangectrl6(self):
        rd = wx.RearrangeDialog()
        rd.Create(self.frame, 'message', 'title',
                  order=[0,1,2], items=['one', 'two', 'three'])
        rd.Destroy()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
