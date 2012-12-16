#---------------------------------------------------------------------------
# Name:        unittests/do-runtests.py
# Author:      Robin Dunn
#
# Created:     6-Aug-2012
# Copyright:   (c) 2012 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Run the unittests given on the command line while using a custom TestResults
class, and output the results in a format that can be integrated into another
TestResults (in the calling process.) See runtests.py for more information
and also for the code that calls this script via subprocess.
"""

import sys
import os
import unittest
import unittest.runner
from wx.lib.six import PY3, BytesIO
import pickle
    
g_testResult = None

# make sure the phoenix dir is on the path
if os.path.dirname(__file__):
    phoenixDir = os.path.abspath(os.path.dirname(__file__)+'/..')
else:  # run as main?
    d = os.path.dirname(sys.argv[0])
    if not d: d = '.'
    phoenixDir = os.path.abspath(d+'/..')
sys.path.insert(0, phoenixDir)


class MyTestResult(unittest.TextTestResult):
    def stopTestRun(self):
        self.output = self.stream.getvalue()
        
    def getResultsMsg(self):
        def fixList(src):
            return [(self.getDescription(test), err) for test, err in src]
        msg = dict()
        msg['output'] = self.output
        msg['testsRun'] = self.testsRun
        msg['failures'] = fixList(self.failures)
        msg['errors'] = fixList(self.errors)
        msg['skipped'] = fixList(self.skipped)
        msg['expectedFailures'] = fixList(self.expectedFailures)
        msg['unexpectedSuccesses'] = fixList(self.unexpectedSuccesses)
        return msg


class MyTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        global g_testResult
        if g_testResult is None:
            self.stream = unittest.runner._WritelnDecorator(BytesIO())
            g_testResult = MyTestResult(self.stream, self.descriptions, self.verbosity)
        return g_testResult
    

if __name__ == '__main__':
    unittest.main(module=None, exit=False, testRunner=MyTestRunner)
    msg = g_testResult.getResultsMsg()
    text = pickle.dumps(msg)
    if PY3:
        sys.stdout.buffer.write(text)
    else:
        sys.stdout.write(text)
    