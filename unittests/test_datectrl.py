import unittest
from unittests import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class datectrl_Tests(wtc.WidgetTestCase):

    def tearDown(self):
        '''
        Destroying the date picker early helps WidgetTestCase's tearDown to
        run smoothly and avoid "R6025 - pure virtual function call".

        '''
        self.dp.Destroy()
        super(datectrl_Tests, self).tearDown()

    def test_datectrl1(self):
        self.dp = wx.adv.DatePickerCtrl(self.frame, dt=wx.DateTime.Now())

    def test_datectrl2(self):
        self.dp = wx.adv.DatePickerCtrl()
        self.dp.Create(self.frame, dt=wx.DateTime.Now())

    def test_genericdatectrl1(self):
        self.dp = wx.adv.GenericDatePickerCtrl(self.frame, dt=wx.DateTime.Now())

    def test_genericdatectrl2(self):
        self.dp = wx.adv.GenericDatePickerCtrl()
        self.dp.Create(self.frame, dt=wx.DateTime.Now())


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
