import unittest
import wtc
import wx
import wx.msw
import os

fileName = 'metafiletest.emf'

#---------------------------------------------------------------------------

class MetafileDCTests(wtc.WidgetTestCase):

    @unittest.skipIf('wxMSW' in wx.PlatformInfo, "Metafile classes only implemented on Windows")
    def test_MetafileDC1(self):
        dc = wx.msw.MetafileDC(fileName)
        dc.DrawLine(0,0, 50,50)
        del dc
        
        os.remove(fileName)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
