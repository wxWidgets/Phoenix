import imp_unittest, unittest
import wtc
import wx
import sys
import os

fileName = 'metafiletest.emf'

#---------------------------------------------------------------------------

class MetafileDCTests(wtc.WidgetTestCase):
            
    def test_MetafileDC1(self):
        dc = wx.MetafileDC(fileName)
        dc.DrawLine(0,0, 50,50)
        del dc
        
        os.remove(fileName)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
