import unittest
import wx
import sys, os
import six

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
        self.frame.PostSizeEvent()

    def tearDown(self):
        def _cleanup():
            for tlw in wx.GetTopLevelWindows():
                if tlw:
                    if isinstance(tlw, wx.Dialog) and tlw.IsModal():
                        tlw.EndModal(0)
                        wx.CallAfter(tlw.Destroy)
                    else:
                        tlw.Close(force=True)
            wx.WakeUpIdle()

        timer = wx.PyTimer(_cleanup)
        timer.Start(100)
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
        self.myYield()


    def closeDialogs(self):
        """
        Close dialogs by calling their EndModal method
        """
        #self.myYield()
        for w in wx.GetTopLevelWindows():
            if isinstance(w, wx.Dialog):
                w.EndModal(wx.ID_CANCEL)


    def waitFor(self, milliseconds):
        INTERVAL = 100
        intervals = milliseconds/INTERVAL
        while True:
            wx.MilliSleep(INTERVAL)
            self.myYield()
            if hasattr(self, 'flag') and self.flag:
                break
            if intervals <= 0:
                break
            intervals -= 1


    def myExecfile(self, filename, ns):
        if not six.PY3:
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


class PubsubTestCase(unittest.TestCase):
    """
    A testcase specifically to test wx.lib.pubsub, as pub is a singleton
    the tearDown removes it from sys.modules to force a reinitialization on
    each test.
    """

    def setUp(self):
        from wx.lib.pubsub import pub

        self.pub = pub
        self.assertEqual(pub, self.pub)

    def tearDown(self):
        self.pub.unsubAll()
        self.pub.clearNotificationHandlers()
        self.pub.clearTopicDefnProviders()
        topicMgr = self.pub.getDefaultTopicMgr()
        try:
            # remove the test topic if present
            if topicMgr.getTopic('pubsub'):
                topicMgr.delTopic('pubsub')
        except:
            pass
        del self.pub

        if 'wx.lib.pubsub.pub' in sys.modules:
            del sys.modules['wx.lib.pubsub.pub']

        #skeys = sys.modules.keys()
        #for name in skeys:
            #del sys.modules[name]
