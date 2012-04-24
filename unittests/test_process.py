import imp_unittest, unittest
import wtc
import wx
import sys, os

testscript = os.path.join(os.path.dirname(__file__), 'process_test.py')

#---------------------------------------------------------------------------

class process_Tests(wtc.WidgetTestCase):

    def test_process1(self):        
        # wx.Execute and wx.Process can only launch app bundles on OSX!! It's
        # a good thing we have the subprocess module that can be used instead.
        if 'wxMac' not in wx.PlatformInfo:
            p = wx.Process.Open('%s %s' % (sys.executable, testscript))
            pid = p.GetPid()


    def test_process2(self):        
        flag = False
        def onEndProcess(evt):
            flag = True
            
        if 'wxMac' not in wx.PlatformInfo:
            p = wx.Process(self.frame)
            self.frame.Bind(wx.EVT_END_PROCESS, onEndProcess)            
            wx.Execute('%s %s' % (sys.executable, testscript), callback=p)
            
    # TODO: When the stream classes are wrapped add tests for writing to and
    # reading from the process

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
