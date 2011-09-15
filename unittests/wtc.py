import imp_unittest, unittest
import wx

#---------------------------------------------------------------------------

class WidgetTestCase(unittest.TestCase):
    """
    A testcase that will create an app and frame for various widget test
    modules to use. They can inherit from this class to save some work. This
    is also good for test cases that need to have an application object
    created.
    """
    def setUp(self):
        self.app = wx.App()
        self.frame = wx.Frame(None, title='WTC: '+self.__class__.__name__)
        self.frame.Show()

    def tearDown(self):
        wx.CallAfter(self.frame.Close)
        self.app.MainLoop()
        del self.app
            
#---------------------------------------------------------------------------


