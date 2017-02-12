# Samuel Dunn
# Application Test Case
# allows testing wx features within the context of an application

# Drawbacks: Current revision doesn't play into unittest's framework very well
#               mimicking it more than anything
#            Current revision only supports handling test events through a top level Frame
#               derived from TestFrame, alternatives are being considered
#            Only one TestCase class per module

# Benefits: Allows unittesting features that suffer from only synthesizing an active event loop.

# TODO:
#   Create a decorator method to identify methods that are fully self sufficient tests, so TestDone
#       can be called implicitly
#       On The other hand, its only truly useful to know if the test completes as part of the method
#   A decorator for describing methods that are a part of a test sequence, but not the entire sequence
#       could be useful
#   Explore TestWidget possibilty
#   Explore commencing test schedule various ways (depending on OS)
#   Change ApplicationTestCase to be a TestCase class generator, allowing plural testcase classes per module
#   explore potential for a meta-class that decorates test related methods to ensure test failure on unhandled
#       exception (related to first couple TODOs)

__version__ = "0.0.1"

import os
import sys
import unittest
import wx
import wx.lib.newevent

TestEvent, EVT_TEST = wx.lib.newevent.NewEvent()

TestEvent.caseiter = 0

"""
class TestWidget:
    # provides some useful methods for use within test widgets.
    # it is recommended to derive test objects from this class in addtion to the
    # relevate wx class

    # provide methods for: ensuring application closes (with and without an error code)
    # standardized assertion
    # etc.

    # should this class provide methods for event handling (forcing derivation from wx.EventHandler)?
"""

class TestWidget:
    def __init__(self):
        assert isinstance(self, wx.EvtHandler), "Test widget needs to be an event handler"

        self.__timer = wx.Timer(self, wx.NewId())

        self.Bind(wx.EVT_TIMER, self.OnCommence, self.__timer)
        self.Bind(EVT_TEST, self.OnTest)

        self.__timer.StartOnce(500) # Wait for the application mainloop to start and commence testing.
                                    # while 500 milliseconds should be more than plenty, this is still
                                    # clumsy and I don't like it.
                                    # Initially I had an initial TestEvent posted to be processed when
                                    # the mainloop was running, but this caused issues on some linux
                                    # distributions.
                                    # Ultimately I'd like to minimize as much waiting as feasibly possible
    
    # this  only gets invoked if the test arget is a frame object, in which case the app can post events directly
    # to the test target
    def GetTestTarget(self):
        return self

    def OnCommence(self, evt):
        assert wx.GetApp().IsMainLoopRunning(), "Timer ended before mainloop started" # see above comment regarding
                                                                                    # commencing with the timer.

        # ensure the test schedule is set up, create it if it does not exist
        if not hasattr(self, "schedule"):
            self.schedule = [member[5:] for member in dir(self) if member.startswith("test_")]

        self.__results = []

        # start test sequence
        evt = TestEvent()
        evt.case = wx.GetApp().case
        wx.PostEvent(self, evt)


    def OnTest(self, evt):
        testfunc = getattr(self, evt.case)

        print("Testing: %s" % evt.case)
        testfunc()

    def TestDone(self, passed = True):
        # record test status and invoke next test
        if passed:
            for window in wx.GetTopLevelWindows():
                window.Close()
        else:
            wx.GetApp().GetMainLoop().Exit(30)


def CreateApp(frame):
    class TestApp(wx.App):
        def OnInit(self):
            self.frame = frame()
            self.frame.Show(True)
            return True

    return TestApp

def CreateFrame(widget):
    # called when the test widget is not a frame.
    class BaseTestFrame(wx.Frame):
        def __init__(self):
            wx.Frame.__init__(self, None, wx.NewId(), "%s Test Frame" % str(type(widget)))

            sizer = wx.BoxSizer()
            self.widget = widget(self)  # assumes need of parent.
            sizer.Add(self.widget, 1, wx.EXPAND)

            self.SetSizer(sizer)
            sizer.Layout()

        # this will only be invoked if the test widget is not a frame.
        def GetTestTarget(self):
            return self.widget

    return BaseTestFrame

def CreateTestMethod(app, case):
    def test_func(obj):
        a = app()
        a.case = case
        a.MainLoop()

    return test_func

def CreateATC(widget):
    # if widget is not instance of TestFrame, generate a quick frame
    # to house the widget
    assert issubclass(widget, TestWidget), "Testing requires the tested widget to derive from TestWidget for now"

    tlw = None
    if not issubclass(widget, wx.Frame):
        # need to stick this widget in a frame
        tlw = CreateFrame(widget)

    else:
        tlw = widget

    app = CreateApp(tlw)

    class ApplicationTestCase(unittest.TestCase):
        pass

    methods = [meth for meth in dir(widget) if (meth.startswith("test_") and callable(getattr(widget, meth)))]
    print(methods)
    for meth in methods:
        test_func = CreateTestMethod(app, meth)
        setattr(ApplicationTestCase, meth, test_func)

    return ApplicationTestCase

if __name__ == "__main__":
    pass
