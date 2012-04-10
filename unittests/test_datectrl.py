import imp_unittest, unittest
import wtc
import wx
import wx.adv

#---------------------------------------------------------------------------

class datectrl_Tests(wtc.WidgetTestCase):

    def test_datectrl1(self):
        dp = wx.adv.DatePickerCtrl(self.frame, dt=wx.DateTime.Now())
        
    def test_datectrl2(self):
        dp = wx.adv.DatePickerCtrl()
        dp.Create(self.frame, dt=wx.DateTime.Now())
        
    def test_genericdatectrl1(self):
        dp = wx.adv.GenericDatePickerCtrl(self.frame, dt=wx.DateTime.Now())
        
    def test_genericdatectrl2(self):
        dp = wx.adv.GenericDatePickerCtrl()
        dp.Create(self.frame, dt=wx.DateTime.Now())

        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
