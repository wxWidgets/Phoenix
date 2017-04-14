import unittest
from unittests import wtc
import wx

import wx.lib.agw.hyperlink as HL

#---------------------------------------------------------------------------

class lib_agw_hyperlink_Tests(wtc.WidgetTestCase):

    def test_lib_agw_hyperlinkCtor(self):
        link = HL.HyperLinkCtrl(self.frame, -1, 'wxPython Main Page', pos=(100, 100),
                                URL='http://www.wxpython.org/')

    def test_lib_agw_hyperlinkMethods(self):
        url = 'http://www.wxpython.org/'
        link = HL.HyperLinkCtrl(self.frame, -1, 'wxPython Main Page', pos=(100, 100),
                                URL=url)

        link.AutoBrowse(False)
        link.SetColours('RED', 'GREEN', 'BLUE')
        link.EnableRollover(True)
        link.SetUnderlines(False, False, True)
        link.SetBold(True)
        link.OpenInSameWindow(True)
        link.SetToolTip(wx.ToolTip('Hello World!'))
        link.UpdateLink()

        self.assertTrue(link.GetColours(), ('RED', 'GREEN', 'BLUE'))
        self.assertTrue(not link.GetUnderlines()[0])
        self.assertTrue(not link.GetVisited())

        self.assertEqual(link.GetURL(), url)


    def test_lib_agw_hyperlinkEvents(self):
        HL.EVT_HYPERLINK_LEFT
        HL.EVT_HYPERLINK_MIDDLE
        HL.EVT_HYPERLINK_RIGHT
        HL.wxEVT_HYPERLINK_LEFT
        HL.wxEVT_HYPERLINK_MIDDLE
        HL.wxEVT_HYPERLINK_RIGHT

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
