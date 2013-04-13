import imp_unittest, unittest
import wx
import sys, os
import wx.lib.six as six

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
        wx.Log.SetActiveTarget(wx.LogStderr())
        self.frame = wx.Frame(None, title='WTC: '+self.__class__.__name__)
        self.frame.Show()

    def tearDown(self):
        def _cleanup():
            self.frame.Close()
            self.app.ExitMainLoop()   
        wx.CallLater(50, _cleanup)
        self.app.MainLoop()
        del self.app


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

    def myUpdate(self, window):
        """
        Since Update() will not trigger paint events on Mac faster than
        1/30 of second we need to wait a little to ensure that there will
        actually be a paint event while we are yielding.
        """
        if 'wxOSX' in wx.PlatformInfo:
            wx.MilliSleep(40)  # a little more than 1/30, just in case
        window.Update()
        
        
    def closeDialogs(self):
        """
        Close dialogs by calling their EndModal method
        """
        #self.myYield()
        for w in wx.GetTopLevelWindows():
            if isinstance(w, wx.Dialog):
                w.EndModal(wx.ID_CANCEL)


    def waitFor(self, milliseconds):
        intervals = milliseconds/100
        while intervals > 0:
            wx.MilliSleep(100)
            self.myYield()
            if hasattr(self, 'flag') and self.flag:
                break
            intervals -= 1
    
    
    def myExecfile(self, filename, ns):
        if sys.version_info < (3,):
            execfile(filename, ns)
        else:
            with open(filename, 'r') as f:
                source = f.read()
            exec(source, ns)
        
        
    def execSample(self, name):
        ns = Namespace()
        samplesDir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../samples'))        
        self.myExecfile(os.path.join(samplesDir, name), ns.dict())
        return ns
    
    
    
#---------------------------------------------------------------------------

class Namespace(object):
    def dict(self):
        return self.__dict__

#---------------------------------------------------------------------------

def mybytes(text):
    if six.PY3:
        return bytes(text, 'utf-8')
    else:
        return str(text)

#---------------------------------------------------------------------------


