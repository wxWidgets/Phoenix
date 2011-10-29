import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class srchctrl_Tests(wtc.WidgetTestCase):

    def test_srchctrlCtor(self):
        t = wx.SearchCtrl(self.frame)

    def test_srchctrlDefaultCtor(self):
        t = wx.SearchCtrl()
        t.Create(self.frame)
        
    def test_srchctrlProperties(self):
        t = wx.SearchCtrl(self.frame)
        t.Menu
        t.SearchButtonVisible
        t.CancelButtonVisible
        t.DescriptiveText
        
        # these are grafted-on methods, just make sure that they are there
        t.SetSearchBitmap
        t.SetSearchMenuBitmap
        t.SetCancelBitmap
        
    def test_srchctrlEventBinding(self):
        t = wx.SearchCtrl(self.frame)
        self.frame.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, lambda e: None, t)
        self.frame.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, lambda e: None, t)
        

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
