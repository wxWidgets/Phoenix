import imp_unittest, unittest
import wx

#---------------------------------------------------------------------------

class WidgetTestCase(unittest.TestCase):
    """
    A testcase that will create an app and frame for various widget test
    modules to use. They can inherit from this class to save some work. This
    is also good for test cases that just need to have an application object
    created.
    """
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None, title='WTC: '+self.__class__.__name__)
        self.frame.Show()

    def tearDown(self):
        def _cleanup():
            self.frame.Close()
            self.app.ExitMainLoop()   
        wx.CallLater(50, _cleanup)
        self.app.MainLoop()
        del self.app

    #def tearDown(self):
    #    wx.CallAfter(self.frame.Close)
    #    self.app.MainLoop()
    #    del self.app
            

    # helper methods
    
    def myYield(self, eventsToProcess=wx.EVT_CATEGORY_ALL):
        """
        Since the tests are usually run before MainLoop is called then we
        need to make our own EventLoop for Yield to actually do anything
        useful.
        """
        evtLoop = self.app.GetTraits().CreateEventLoop()
        activator = wx.EventLoopActivator(evtLoop) # automatically restores the old one
        evtLoop.YieldFor(eventsToProcess)

            
#---------------------------------------------------------------------------


