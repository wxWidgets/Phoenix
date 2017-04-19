import unittest
from unittests import wtc
import wx
import sys
import os

fileName = os.path.join(os.path.dirname(__file__), 'dcpstest.svg')

#---------------------------------------------------------------------------

class dcps_tests(wtc.WidgetTestCase):

    def test_PostscriptDC1(self):
        pd = wx.PrintData()
        pd.SetPrintMode(wx.PRINT_MODE_FILE)
        pd.SetFilename(fileName)

        dc = wx.PostScriptDC(pd)
        pen = wx.Pen('black')
        self.assertTrue(pen.IsOk())
        dc.StartDoc("message")
        dc.SetPen(pen)
        dc.DrawLine(0,0, 50,50)
        dc.EndDoc()
        del dc

        os.remove(fileName)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
