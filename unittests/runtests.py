#---------------------------------------------------------------------------
# Name:        unittests/runtests.py
# Author:      Robin Dunn
#
# Created:     3-Dec-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
This script will find and run all of the Phoenix test cases. We use a custom
TestSuite and other customized unittest classes so we can run each test
module in a separate process. This helps to isolate the test cases from each
other so they don't stomp on each other too much. 

Currently the process granularity is the TestSuite created when the tests in
a single module are loaded, which makes it essentially the same as when
running that module standalone. More granularity is possible by using
separate processes for each TestCase.testMethod, but I haven't seen the need
for that yet.

See do-runtests.py for the script that is run in the child processes.
"""


import sys
import os
import glob
import subprocess
import imp_unittest, unittest

# make sure the phoenix dir is on the path
if os.path.dirname(__file__):
    phoenixDir = os.path.abspath(os.path.dirname(__file__)+'/..')
else:  # run as main?
    d = os.path.dirname(sys.argv[0])
    if not d: d = '.'
    phoenixDir = os.path.abspath(d+'/..')
sys.path.insert(0, phoenixDir)

import wx
import wx.lib.six as six
print("wx.version: " + wx.version())
print("pid: " + str(os.getpid()))
#print("executable: " + sys.executable); raw_input("Press Enter...")

import wtc

#---------------------------------------------------------------------------

def getTestName(test):
    cls = test.__class__
    return "%s.%s.%s" % (cls.__module__, cls.__name__, test._testMethodName)


class MyTestSuite(unittest.TestSuite):
    """
    Override run() to run the TestCases in a new process.
    """
    def run(self, result, debug=False):
        if self._tests and isinstance(self._tests[0], unittest.TestSuite):
            # self is a suite of suites, recurse down another level
            return unittest.TestSuite.run(self, result, debug)
        elif self._tests and not isinstance(self._tests[0], wtc.WidgetTestCase):
            # we can run normal test cases in this process
            return unittest.TestSuite.run(self, result, debug)
        else:
            # Otherwise we want to run these tests in a new process,
            # get the names of all the test cases in this test suite
            testNames = list()
            for test in self:
                name = getTestName(test)
                testNames.append(name)
                
            # build the command to be run
            PYTHON = os.environ.get('PYTHON', sys.executable)
            runner = os.path.join(phoenixDir, 'unittests', 'do-runtests.py')
            cmd = [PYTHON, '-u', runner] 
            if result.verbosity > 1:
                cmd.append('--verbose')
            elif result.verbosity < 1:
                cmd.append('--quiet')
            cmd += testNames
            
            # run it
            sp = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE)#, stderr=subprocess.STDOUT)
            output = sp.stdout.read()
            #if sys.version_info > (3,):
            #    output = output.decode('ascii') 
            output = output.rstrip()
            rval = sp.wait()
            if rval:
                print("Command '%s' failed with exit code %d." % (cmd, rval))
                sys.exit(rval)
                        
            # Unpickle the output and copy it to result. It should be a
            # dictionary with info from the TestResult class used in the
            # child process.
            import pickle
            msg = pickle.loads(output)
            result.stream.write(msg['output'])
            result.stream.flush()
            result.testsRun += msg['testsRun']
            result.failures += msg['failures']
            result.errors += msg['errors']
            result.skipped += msg['skipped']
            result.expectedFailures += msg['expectedFailures']
            result.unexpectedSuccesses += msg['unexpectedSuccesses']
            
            return result
                
            

class MyTestResult(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity):
        super(MyTestResult, self).__init__(stream, descriptions, verbosity)
        self.verbosity = verbosity
    
    def getDescription(self, test):
        """
        Override getDescription() to be able to deal with the test already
        being converted to a string.
        """
        if isinstance(test, six.string_types):
            return test
        return super(MyTestResult, self).getDescription(test)
    
    
    
class MyTestLoader(unittest.TestLoader):
    suiteClass = MyTestSuite

class MyTestRunner(unittest.TextTestRunner):
    resultclass = MyTestResult

#---------------------------------------------------------------------------

if __name__ == '__main__':
    if '--single-process' in sys.argv:
        sys.argv.remove('--single-process')
        args = sys.argv[:1] + 'discover -p test_*.py -s unittests -t .'.split() + sys.argv[1:]
        unittest.main(argv=args)

    else:
        # The discover option doesn't use my my custom loader or suite
        # classes, so we'll do the finding of the test files in this case.
        #names = ['test_gdicmn', 'test_panel', 'test_msgdlg', 'test_uiaction']
        names = glob.glob(os.path.join('unittests', 'test_*.py'))
        names = [os.path.splitext(os.path.basename(n))[0] for n in names]
        args = sys.argv + names
        unittest.main(argv=args, module=None, 
                      testRunner=MyTestRunner, testLoader=MyTestLoader())


        
    #loader = MyTestLoader()
    #suite = unittest.TestSuite()
    #for name in ['test_panel', 'test_msgdlg']:
    #    suite.addTests(loader.loadTestsFromName(name))
    #runner = MyTestRunner()
    #runner.run(suite)
    
