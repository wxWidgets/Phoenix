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

class TestApplication(wx.App):
    def OnInit(self):
        f = ApplicationTestCase._frame()
        f.Show(True)
        return True

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

class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.NewId(), "Phoenix Application Test")
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

    def OnCommence(self, evt):
        assert wx.GetApp().IsMainLoopRunning(), "Timer ended before mainloop started" # see above comment regarding
                                                                                    # commencing with the timer.

        # ensure the test schedule is set up, create it if it does not exist
        if not hasattr(self, "schedule"):
            self.schedule = [member[5:] for member in dir(self) if member.startswith("test_")]

        self.__results = []

        # start test sequence
        evt = TestEvent()
        wx.PostEvent(self, evt)

    def OnTest(self, evt):
        # find test case and try it
        try:
            testname = self.schedule[TestEvent.caseiter]
            TestEvent.caseiter += 1
        except IndexError:
            # well either some one made schedule some funky object
            # or the end of the schedule has been reached.
            # for now pretend its a good thing:
            print("Reached end of schedule")
            self.WrapUp()
            return

        try:
            testfunc = getattr(self, "test_%s" % testname)
        except AttributeError:
            print("Missing test method for: %s" % testname, file = sys.stderr)
            sys.exit(1)

        try:
            print("Testing: %s" % testname)
            testfunc()
        except Exception as e:
            import traceback
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)
            tb_info = traceback.extract_tb(tb)

            filename, line, func, text = tb_info[-1]
            print("Additional Info:\nFile: %s\nLine: %s\nFunc: %s\nText: %s" % (filename, line, func, text), file = sys.stderr)
            sys.exit(1)

    def TestDone(self, passed = True):
        # record test status and invoke next test
        if passed:
            self.__results.append(".")
        else:
            self.__results.append("F")

        evt = TestEvent()
        wx.PostEvent(self, evt)


    def Assert(self, expr, message = "An Assertion occurred"):
        # well, misnomer. Is a psuedo assert
        # use this method when ensuring the test can continue
        # in most test-failure scenarios you should use TestDone(False)
        if not expr:
            print(message, file = sys.stderr)
            sys.exit(1)

    def WrapUp(self):
        print("Results: %s" % "".join(self.__results))
        
        if "F" in self.__results:
            print("Test(s) have failed", file = sys.stderr)
            sys.exit(1)
        else:
            # close peacefully
            self.Close()

class ApplicationTestCase(unittest.TestCase):
    _app = TestApplication
    _frame = TestFrame

    def test_application(self):
        app = self._app()
        app.MainLoop()

def main():
    unittest.main()

if __name__ == "__main__":
    main()
