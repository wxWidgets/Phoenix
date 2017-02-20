# Samuel Dunn
# Application Test Case
# Allows testing wx features within the context of an application

# Benefits: As stated, allows unit testing within a full App mainloop.
#           Allows developers to quickly construct a test case by developing a
#               single widget
#           TestCase class is generated from the widget provided to atc. The
#               generated TestCase class  mimics the widget to allow pytest
#               to behave  normally. This allows  unsquashed testing (jamming
#               plural tests into one runtime)
#           Generated TestCase class should play nice with all unittest features
#           Generated TestCase classes are unique, allowing plural per test
#               module

# Drawbacks: Generated test case class has to be applied to a __main__ module
#               global scope member. Need to look into unittest.TestDiscorvery
#               to correct this behavior
#           Code is currently a bit sloppy, Revisions will be made before a
#               formal PR to improve documentation and clean up the code.
#

# TODO:
#   Ensure full TestCase API is available within the app
#   automatically apply TestCritical decorator to test_ methods in widget
#   Ensure TestCritical decorator plays nice with preserving other decorations
#       such that decoration order does not matter
#   Add stack trace printouts upon TestDone(False) or TestCritical exception


__version__ = "0.0.2"

import functools
import os
import sys
import unittest
import wx
import wx.lib.newevent

TestEvent, EVT_TEST = wx.lib.newevent.NewEvent()

class TestError(Exception):
    pass

def testCritical(func):
    """
    Wraps the provided function to ensure that uncaught exceptions
    will end execution.
    This is done by closing all top level windows and allowing the exception
    to be re-raised once the main event loop ends.
    """
    @functools.wraps(func)
    def method(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("Unbound exception caught in test procedure:\n%s\n%s" % (e.__class__, str(e)), file = sys.stderr)
            # give full stack trace
            wx.GetApp().exception = e
            for window in wx.GetTopLevelWindows():
                window.Close()

    return method

def createATC(widget_cls):
    """
    Creates and returns a class that derives unittest.TestCase the TestCase is generated from widget
    IMPORTANT NOTE: In order for the returned class to be picked up by the default unittest TestDiscovery process
        the returned class must be assigned to the main module's base level namespace
    If widget is not top level  (does not drive from wx.Frame) a container top level widget will be created
        Additionally, if the widget is not top level generated frame object will attempt to pass
            itself as a parameter to widget.__init__ (for assigning parent) 
            Be sure to expect this in such scenarios.

    The returned class will have test_ methods to match those of the widget class, all decorations are preserved
        so it is perfectly valid to apply unittest decorators (such as unittest.expectedFailure) to the widget class
        as such decorations will be reflected by the TestCase class methods and utilized during testing.

    Args:
        widget: A widget *class* that derives from TestWidget.

    Returns:
        unittest.TestCase derivation

    Example:
    class Foo(wx.Frame, atc.TestWidget):
        def __init__(self):
            wx.Frame.__init__(self, None, wx.NewId())
            atc.TestWidget.__init__(self)

        def test_pass(self):
            self.testPassed()

        @unittest.expectedFailure
        def test_fail(self):
            self.testFailed("Deliberate failure")

    FooTestCase = atc.createATC(Foo)

    # FooTestCase will have a methods test_pass and test_fail
    # when run by pytest test_pass will pass and test_fail will
    # xfail.
    """
    assert issubclass(widget_cls, TestWidget), "Testing requires the tested widget to derive from TestWidget for now"
    assert not issubclass(widget_cls, wx.Dialog), "Support for wx.Dialog derivatives suspended."
    tlw = None
    if not issubclass(widget_cls, wx.Frame):
        # need to stick this widget in a frame
        tlw = __CreateFrame(widget_cls)
    else:
        tlw = widget_cls

    app = __CreateApp(tlw)

    class ApplicationTestCase(unittest.TestCase):
        pass

    methods = [meth for meth in dir(widget_cls) if (meth.startswith("test_") and callable(getattr(widget_cls, meth)))]

    for meth in methods:
        test_func = __CreateTestMethod(app, meth)
        # ensure any other deocrated data is preserved:
        basemeth = getattr(widget_cls, meth)
        for attr in dir(basemeth):
            if not hasattr(test_func, attr):
                setattr(test_func, attr, getattr(basemeth, attr))

        setattr(ApplicationTestCase, meth, test_func)

    return ApplicationTestCase

class TestWidget:
    """
    Base Test Widget class. Widgets that are intended to be tested via ATC *MUST* derive this class
    It is likewise expected that these widgets derive from some actual wx widget, at the minimum from wx.EvtHandler,  the constructor for which must be called first
    This class provides test sequencing to its derived class, most notably in starting the test automatically, and providing methods for termination.
    For example usage please review unittests/test_atc.
    """
    def __init__(self):
        """
        Ensures that class being instantiated also derives from wx.EvtHandler and prepares for auto-launch
        Args: 
            self
        """
        assert isinstance(self, wx.EvtHandler), "Test widget needs to be an event handler"

        self.Bind(EVT_TEST, self.__OnTest)

        if "__WXGTK__" in wx.PlatformInfo:
            self.Bind(wx.EVT_WINDOW_CREATE, self.__OnLnxStart)

        else:
            wx.CallAfter(self.__OnCommence)
    
    def testPassed(self):
        """
        Indicates that the currently running test has passed successfully.
        The application will close clearly after this call, allowing  unittesting to proceed
        IMPORTANT NOTE: test sequences must terminate with either a call to this method or testFailed()
            otherwise runtime may not close until the watchdog triggers (treating the test as a failure)
        
        Args:
            None

        Returns:
            None
        """
        for window in wx.GetTopLevelWindows():
            window.Close()

    def testFailed(self, errmsg =  "A test failed."):
        """
        Indicates that the currently running test has failed. 
        The application will close after this call and an TestError exception will be raised
        IMPORTANT NOTE: test sequences must terminate with either a call to this method or testPassed()
            otherwise runtime may not close until the watchdog triggers (treating the test as a failure)

        Args: 
            errmsg: Message assigned to TestError exception.
        Returns:
            None
        """

        # do not rely on testCritical being applied to an above method
        wx.GetApp().exception = TestError(errmsg)
        for window in wx.GetTopLevelWindows():
            window.Close()
    
    def getTestCase(self):
        """
        Returns the encompassing TestCase class, which can then be used for its various
        testing methods.

        Args:
            None
        Returns:
            Encompassing ATC class.
        """
        return wx.GetApp().testcase

    def __OnCommence(self):
        """
        Invoked to start test procedures. Invokation is handled by atc.
        """
        # assert should exit properly if the mainloop is  not running
        assert wx.GetApp().IsMainLoopRunning(), "__OnCommence invoked before MainLoop was ready"

        # start test sequence
        evt = TestEvent()
        evt.case = wx.GetApp().case
        wx.PostEvent(self, evt)

        # set a watchdog incase of test error
        wx.CallLater(300000, self.__OnWatchdog) # 5 minutes in millis

    def __OnWatchdog(self):
        """ 
        Invoked with a test hass taken more than 5 minutes to complete
        """
        print("Test Timeout!!!")
        wx.GetApp().exception = RuntimeError("Watchdog timed out")
        for window in wx.GetTopLevelWindows():
            window.Close()

    def __OnLnxStart(self, evt):
        """
        Invoked on linux systems to signal mainloop readiness
        """
        wx.CallAfter(self.__OnCommence)
        evt.Skip()

    @testCritical   # automatically apply exception blocking to test_ methods.. indirectly
    def __OnTest(self, evt):
        testfunc = getattr(self, evt.case)

        print("Testing: %s" % evt.case)
        testfunc()
        
def __CreateApp(frame_cls):
    """
    Generates an app class that will create an instance of frame_cls on launch.
    This method is utilized inside atc and probably should not be used otherwise

    Args:
        frame_cls: Class that derives from wx.Frame
    Returns:
        wx.App derived class
    """
    class TestApp(wx.App):
        """ a generated App class """
        def OnInit(self):
            self.frame = frame_cls()
            self.frame.Show(True)
            return True

    return TestApp

def __CreateFrame(widget_cls):
    """
    Creates a wx.Frame derivation to create an instance of widget_cls and sizes said instance to fill the frame
    This method is utlized inside atc and probably should not be used otherwise
    
    Args:
        widget_cls: Widget class (presumably the TestWidget) that will be initialized within the generated frame object

    Returns:
        wx.Frame derived class to use for testing the widget.
    """
    # called when the test widget is not a frame.
    class BaseTestFrame(wx.Frame):
        """ A generated Frame class """
        def __init__(self):
            wx.Frame.__init__(self, None, wx.NewId(), "Generated Test Frame")

            sizer = wx.BoxSizer()
            self.widget = widget_cls(self)  # assumes need of parent.
            sizer.Add(self.widget, 1, wx.EXPAND)

            self.SetSizer(sizer)
            sizer.Layout()

    return BaseTestFrame

def __CreateTestMethod(app_cls, case):
    """
    Generates the test methods to assign to the ApplicationTestCase class.
    Generated methods initialize an instance of app_cls, assign the intended test case and 
        launch the app.
    Once the app has closed error conditions are checked and  the function returns

    This method is utilized inside atc and should not be used otherwise.

    returned method objects are not redecorated (as critical class data is not present)

    Args:
        app_cls: the wx.App derived class to instantiate
        case: str indicating which  test method to retrieve and  invoke.
    
    Returns:
        Method objects to launch an application for a given test case.
    """
    def test_func(obj):
        a = app_cls()
        a.case = case
        a.testcase = obj
        a.MainLoop()

        if hasattr(a, "exception"):
            raise a.exception

        elif hasattr(a, "errorcode"):
            sys.exit(a.errorcode)

    return test_func
