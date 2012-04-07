import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class cshelp_Tests(wtc.WidgetTestCase):

    def test_cshelp1(self):
        provider = wx.SimpleHelpProvider()
        wx.HelpProvider.Set(provider)
        
        pnl = wx.Panel(self.frame)
        pnl.SetHelpText("HelpMe!")
        cBtn = wx.ContextHelpButton(pnl)
        
        
    def test_cshelp2(self):
        wx.wxEVT_HELP
        wx.wxEVT_DETAILED_HELP
        
        wx.EVT_HELP
        wx.EVT_HELP_RANGE
        wx.EVT_DETAILED_HELP
        wx.EVT_DETAILED_HELP_RANGE
        
        
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
