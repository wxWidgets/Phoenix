import unittest
from unittests import wtc
import wx

import wx.lib.agw.fourwaysplitter as FWS

#---------------------------------------------------------------------------

class lib_agw_fourwaysplitter_Tests(wtc.WidgetTestCase):

    def test_lib_agw_fourwaysplitterCtor(self):
        splitter = FWS.FourWaySplitter(self.frame, -1, agwStyle=wx.SP_LIVE_UPDATE)


    def test_lib_agw_fourwaysplitterMethods(self):
        splitter = FWS.FourWaySplitter(self.frame, -1, agwStyle=wx.SP_LIVE_UPDATE)

        panels = []
        # Put in some coloured panels...
        for colour in [wx.RED, wx.WHITE, wx.BLUE, wx.GREEN]:

            panel = wx.Panel(splitter)
            panel.SetBackgroundColour(colour)

            splitter.AppendWindow(panel)
            panels.append(panel)

        # Some methods tests...
        for index in range(4):
            self.assertEqual(splitter.GetWindow(index), panels[index])

        splitter.ExchangeWindows(panels[0], panels[3])
        self.assertEqual(splitter.GetWindow(0), panels[3])
        self.assertEqual(splitter.GetWindow(3), panels[0])

        window = wx.Window(splitter)
        splitter.ReplaceWindow(panels[3], window)
        self.assertEqual(splitter.GetWindow(0), window)

        splitter.SetExpanded(0)

        for index in range(1, 4):
            self.assertTrue(not splitter.GetWindow(index).IsShown())


    def test_lib_agw_fourwaysplitterConstantsExist(self):
        FWS.FLAG_CHANGED
        FWS.FLAG_PRESSED
        FWS.NOWHERE
        FWS.SP_3DBORDER
        FWS.SP_LIVE_UPDATE
        FWS.SP_NOSASH

    def test_lib_agw_fourwaysplitterEvents(self):
        FWS.EVT_SPLITTER_SASH_POS_CHANGED
        FWS.EVT_SPLITTER_SASH_POS_CHANGING

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
