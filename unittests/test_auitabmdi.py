import unittest
from unittests import wtc
import wx
import wx.aui

#---------------------------------------------------------------------------

class auitabmdi_Tests(wtc.WidgetTestCase):

    def test_auitabmdi01(self):
        parent = wx.aui.AuiMDIParentFrame(self.frame, title='AUI MDI')
        child = wx.aui.AuiMDIChildFrame(parent, title='Child')

        parent.Show()
        self.myYield()
        child.Close()
        self.myYield()
        parent.Close()


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
