import imp_unittest, unittest
import wtc
import wx

#---------------------------------------------------------------------------

class fswatcher_Tests(wtc.WidgetTestCase):

    def test_fswatcher1(self):
        
        evtLoop = self.app.GetTraits().CreateEventLoop()
        activator = wx.EventLoopActivator(evtLoop) # automatically restores the old one
        watcher = wx.FileSystemWatcher()
        watcher.Add(__file__)
        watcher.Bind(wx.EVT_FSWATCHER, lambda evt: None)
        
        
#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
