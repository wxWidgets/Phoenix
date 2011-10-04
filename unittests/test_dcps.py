import imp_unittest, unittest
import wtc
import wx
import sys
import os

fileName = 'svgtest.svg'

#---------------------------------------------------------------------------

class dcps_tests(wtc.WidgetTestCase):
            
    def test_PostscriptDC1(self):
        return
        pd = wx.PrintData()
        pd.SetFilename(fileName)
        dc = wx.PostScriptDC(pd)
        dc.StartDoc("message")
        dc.DrawLine(0,0, 50,50)
        del dc
        os.remove(fileName)
        

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
