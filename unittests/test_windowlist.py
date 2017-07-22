import sys
import unittest
import wx
from unittests import wtc
##import os; print 'PID:', os.getpid(); raw_input('Ready to start, press enter...')

#---------------------------------------------------------------------------

class WindowList(wtc.WidgetTestCase): #unittest.TestCase):
    def setUp(self):
        super(WindowList, self).setUp()
        self.frames = list()
        for i in range(5):
            frm = wx.Frame(self.frame, title='frm%d' % i)
            self.frames.append( frm )
            frm.Show()
        for i in range(5):
            w = wx.Window(self.frames[4])

    def _tearDown(self):
        def _closeAll():
            for frm in wx.GetTopLevelWindows():
                if frm:
                    frm.Close()
            self.myYield()
        wx.CallAfter(_closeAll)
        self.app.MainLoop()
        del self.app


    def test_WindowList_GetTLW1(self):
        TLWs = wx.GetTopLevelWindows()

        #self.assertEqual(len(TLWs), 6) # 1 created in the base class plus 5 here
        # since TLWs delay destroying themselves there may be more than 6 of them here
        # when we're running the whole test suite, so we have to comment out that
        # assert...

        for tlw in TLWs:
            self.assertTrue(isinstance(tlw, wx.TopLevelWindow))

    def test_WindowList_GetChildren(self):
        children = self.frames[0].GetChildren()
        self.assertEqual(len(children), 0)
        children = self.frames[4].GetChildren()
        self.assertEqual(len(children), 5)

    def test_WindowList_repr(self):
        TLWs = wx.GetTopLevelWindows()
        self.assertTrue(repr(TLWs).startswith("WindowList:"))


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
