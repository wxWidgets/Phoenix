import unittest
from unittests import wtc
import wx
import signal, sys, os

testscript = os.path.join(os.path.dirname(__file__), 'process_script.py')

#---------------------------------------------------------------------------

def tearDownModule():
    # wx.Execute() installs a process-wide SIGCHLD handler that outlives
    # this module's wx.App, and can crash a later test's app (wxWidgets
    # bug). Reset it so it doesn't leak into other tests in this worker.
    if hasattr(signal, 'SIGCHLD'):
        signal.signal(signal.SIGCHLD, signal.SIG_DFL)

#---------------------------------------------------------------------------

class process_Tests(wtc.WidgetTestCase):

    def test_process1(self):
        # wx.Execute and wx.Process can only launch app bundles on OSX!! It's
        # a good thing we have the subprocess module that can be used instead.
        if 'wxMac' not in wx.PlatformInfo:
            p = wx.Process.Open('%s %s' % (sys.executable, testscript))
            pid = p.GetPid()


    def test_process2(self):
        self.flag = False
        def onEndProcess(evt):
            self.flag = True

        if 'wxMac' not in wx.PlatformInfo:
            p = wx.Process(self.frame)
            self.frame.Bind(wx.EVT_END_PROCESS, onEndProcess)
            wx.Execute('%s %s' % (sys.executable, testscript), callback=p)
            self.waitFor(1000)
            self.assertTrue(self.flag)

    def test_processExecuteEnv(self):
        env = wx.ExecuteEnv()
        self.assertEqual(env.cwd, '')
        self.assertEqual(env.env, {})
        with self.assertRaises(TypeError):
            env.env = {'FOO': 1}
        with self.assertRaises(TypeError):
            env.env = 5

        if 'wxMac' not in wx.PlatformInfo:
            import tempfile
            cwd = os.path.realpath(tempfile.mkdtemp())
            env.cwd = cwd
            env.env = dict(os.environ, WXPY_TEST_VAR='hello')
            p = wx.Process()
            p.Redirect()
            cmd = '"%s" -c "import os; print(os.getcwd()); print(os.environ[\'WXPY_TEST_VAR\'])"'
            rv = wx.Execute(cmd % sys.executable, wx.EXEC_SYNC | wx.EXEC_NODISABLE, p, env)
            self.assertEqual(rv, 0)
            out = p.GetInputStream().read().decode().split()
            self.assertEqual([os.path.realpath(out[0]), out[1]], [cwd, 'hello'])
            os.rmdir(cwd)

    # TODO: When the stream classes are wrapped add tests for writing to and
    # reading from the process

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
