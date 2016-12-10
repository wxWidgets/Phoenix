import unittest
from unittests import wtc
import wx

import wx.lib.agw.pycollapsiblepane as PCP

#---------------------------------------------------------------------------

class lib_agw_pycollapsiblepane_Tests(wtc.WidgetTestCase):

    def test_lib_agw_pycollapsiblepaneCtor(self):
        pane = PCP.PyCollapsiblePane(self.frame, label='Some Data',
                                     style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

    def test_lib_agw_pycollapsiblepaneMethods(self):
        pane = PCP.PyCollapsiblePane(self.frame, label='Some Data',
                                     style=wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE)

        content = pane.GetPane()

        nameLbl = wx.StaticText(content, -1, "Name:")
        name = wx.TextCtrl(content, -1, "");

        # Some methods tests...
        self.assertTrue(pane.GetWindowStyleFlag() & wx.CP_USE_STATICBOX == 0)
        self.assertEqual(pane.GetLabel(), 'Some Data')
        self.assertTrue(pane.IsCollapsed())
        self.assertTrue(not pane.IsExpanded())

        pane.Expand()
        self.assertTrue(pane.IsExpanded())

    def test_lib_agw_pycollapsiblepaneConstantsExist(self):
        PCP.CP_DEFAULT_STYLE
        PCP.CP_GTK_EXPANDER
        PCP.CP_LINE_ABOVE
        PCP.CP_NO_TLW_RESIZE
        PCP.CP_USE_STATICBOX

    def test_lib_agw_pycollapsiblepaneEvents(self):
        PCP.EVT_COLLAPSIBLEPANE_CHANGED


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
