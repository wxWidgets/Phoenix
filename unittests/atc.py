# Samuel Dunn
# Application Test Case
# Allows testing wx features within the context of an application

"""
Application Test Case allows python's unittest framework to run full wx 
applications within a test case with out any need to manually drive the main 
eventloop. This reduces buginess within tested features that require a running
mainloop, such as event-based behavior.

ATC accomplishes this by receiving a widget class and constructing a test case class
from the widget. When unittest invokes a test within this testcase the application
will be started and the test sequence will begin. 

The widget given to ATC will look like it is a test case itself, aside from a few 
nuances. Which are as follows:
1) The widget MUST derive from the given class: TestWidget
    This class provides the code necessary to automate tests and convey results.
    Furthermore, anything that derives TestWidget must also derive from at least wx.EventHandler
2) Some methods will need to be decorated with 'testCritical' to perform as expected.
    More on this later.
3) The ATC testcase class must be created and assigned to the global scope so unittest can detect it.
    This is performed with createATC(test_widget_derivation)

ATC requires some additional code in order to perform correctly. It needs:
1) to know which methods are critical. That is which ones are not allowed to have
  an exception escape their frame.
2) When a test fails or passes

First, a decorator method 'testCritical' is provided. this decorator will automatically fail 
the current test if an an unhandled exception occurs within the decorated function.
Secondly, TestWidget provides the methods TestWidget.testPassed and TestWidget.TestFailed
to specify a test result. When these methods are called the application will exit and 
results will be delivered to unittest

Important notes:
The TestCase class can be accessed using TestWidget.getTestCase(), this is usefull for 
utilizing standard testcase methods such as failUnless, assert____() and so on.
These TestCase methods will only work within testCritical methods. Otherwise 
the exceptions raised by them will pass silently into the Python/wx sandwhich. 


The following files contain ATC examples:
unittests/test_frame.py
unittest/test_atc.py

~~ Samuel Dunn
"""

# TODO:
#   Ensure full TestCase API is available within the app
#   automatically apply TestCritical decorator to test_ methods in widget
#   Explore option of having the same application instance runn all test sequences.


__version__ = "0.0.3"

import functools
import os
import six
import sys
import unittest
import traceback
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
            six.print_("Unbound exception caught in test procedure:\n%s\n%s" % (e.__class__, str(e)), file = sys.stderr)
            
            # print the traceback for this exception
            traceback.print_tb(sys.exc_info()[-1])

            # close  the app.
            wx.GetApp().exception = e
            for window in wx.GetTopLevelWindows():
                window.Close()

    return method

def createATC(widget_cls, autoshow = True):
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
        autoshow: (True) boolean value that indicates whether or not the top level window should be automatically shown
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
    
    tlw = None
    if not issubclass(widget_cls, wx.Frame):
        # need to stick this widget in a frame
        tlw = __CreateFrame(widget_cls)
    else:
        tlw = widget_cls

    app = __CreateApp(tlw, autoshow)

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

        # print stacktrace info (as no exception was raised at this point
        # a stacktrace is used, not a traceback.)
        self.__print_stacktrace()

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
        six.print_("Test Timeout!!!")
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
        testfunc()
    
    def __print_stacktrace(self):
        """
        Called during testFailed to print stack trace information.
        """
        six.print_("Providing most recent stack trace information:\n", file = sys.stderr)
        stacktrace = traceback.extract_stack()
        # find "test_func" or whatever the generated test function is called
        # within stacktrace and exclude all rows before it.
        for x in range(len(stacktrace)):
            if "test_func" in str(stacktrace[x]):
                stacktrace = stacktrace[x:-2]   # cut off call to this method
                break                           # and call to extract_stack

        six.print_("".join(traceback.format_list(stacktrace)), file = sys.stderr)
        six.print_("TestWidget.testFailed() called.", file = sys.stderr)
        

def __CreateApp(frame_cls, autoshow):
    """
    Generates an app class that will create an instance of frame_cls on launch.
    This method is utilized inside atc and probably should not be used otherwise

    Args:
        frame_cls: Class that derives from wx.Frame
        autoshow: boolean value that indicates whether or not the top level window should be automatically shown
    Returns:
        wx.App derived class
    """
    class TestApp(wx.App):
        """ a generated App class """
        def OnInit(self):
            self.frame = frame_cls()
            if autoshow:
                self.frame.Show()
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
            wx.Frame.__init__(self, None, wx.NewId(), "ATC: " + widget_cls.__name__)

            if issubclass(widget_cls, wx.Dialog):
                dlg = widget_cls(self)
                self.Show() # show first, so the dialog is on top
                dlg.Show()  # modeless

            else:
                sizer = wx.BoxSizer()
                self.widget = widget_cls(self)  # assumes need of parent.
                sizer.Add(self.widget, 1, wx.EXPAND)

                self.SetSizer(sizer)
                sizer.Layout()

                self.Show()

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

        if hasattr(a, "tb"):
            traceback.print_tb(a.tb)

        if hasattr(a, "exception"):
            raise a.exception

        elif hasattr(a, "errorcode"):
            sys.exit(a.errorcode)

    return test_func
