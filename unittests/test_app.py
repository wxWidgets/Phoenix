import os
import subprocess
import sys
import unittest
import wx
##import os; print 'PID:', os.getpid(); raw_input('Ready to start, press enter...')

import warnings

#---------------------------------------------------------------------------

class App(unittest.TestCase):

    def test_App(self):
        app = wx.App()

    def test_App_OnInit(self):
        class MyApp(wx.App):
            def OnInit(self):
                self.onInit_called = True
                return True
        app = MyApp()
        self.assertTrue(app.onInit_called)

    if 0:
        def test_App_OnExit(self):
            class MyApp(wx.App):
                def OnInit(self):
                    self.onExit_called = False
                    self.f = wx.Frame(None)
                    self.f.Bind(wx.EVT_IDLE, self.OnIdle)
                    self.f.Show()
                    return True
                def OnIdle(self, evt):
                    self.f.Close()
                def OnExit(self):
                    self.onExit_called = True
                    return 0
            app = MyApp()
            app.MainLoop()
            self.assertTrue(app.onExit_called)

    def test_version(self):
        v = wx.version()
        wx.VERSION
        wx.VERSION_STRING
        wx.__version__

    def test_PySimpleApp(self):
        # wx.PySimpleApp is supposed to be deprecated, make sure it is.
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            with self.assertRaises(wx.wxPyDeprecationWarning):
                app = wx.PySimpleApp()


    def test_CallAfter(self):
        class MyApp(wx.App):
            def OnInit(self):
                self.callAfter_called = False
                self.frame = wx.Frame(None, title="testing CallAfter")
                self.frame.Show()
                wx.CallAfter(self.doAfter, 1, 2, 3)
                return True
            def doAfter(self, a, b, c):
                self.callAfter_called = True
                self.frame.Close()

        app = MyApp()
        app.MainLoop()
        self.assertTrue(app.callAfter_called)

    @unittest.skipIf(sys.platform != 'win32', 'activation contexts are Windows-only')
    def test_importInHostActivationContext(self):
        # Like an MFC host calling into Python: it activates a context around
        # the call and deactivates it afterwards, which fails if importing wx
        # left its own context on top
        code = """if 1:
            import ctypes
            from ctypes import wintypes
            k32 = ctypes.WinDLL('kernel32', use_last_error=True)
            k32.GetCurrentActCtx.argtypes = [ctypes.POINTER(wintypes.HANDLE)]
            k32.ActivateActCtx.argtypes = [wintypes.HANDLE, ctypes.POINTER(ctypes.c_size_t)]
            k32.DeactivateActCtx.argtypes = [wintypes.DWORD, ctypes.c_size_t]
            ctx = wintypes.HANDLE()
            k32.GetCurrentActCtx(ctypes.byref(ctx))
            cookie = ctypes.c_size_t()
            assert k32.ActivateActCtx(ctx, ctypes.byref(cookie))
            import wx
            assert k32.DeactivateActCtx(0, cookie.value)
            """
        env = dict(os.environ)
        env['PYTHONPATH'] = os.pathsep.join(
            [os.path.dirname(os.path.dirname(wx.__file__))] +
            ([env['PYTHONPATH']] if env.get('PYTHONPATH') else []))
        result = subprocess.run([sys.executable, '-c', code], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
