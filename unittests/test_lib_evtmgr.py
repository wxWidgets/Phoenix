import os
import subprocess
import sys
import unittest
from unittests import wtc
import wx

from wx.lib.evtmgr import eventManager

#---------------------------------------------------------------------------

class lib_evtmgr_Tests(wtc.WidgetTestCase):

    def test_lib_evtmgrNoDeprecationWarning(self):
        # Use a new interpreter since wx.lib.pubsub has already been imported
        # in this one
        code = ("import warnings, wx\n"
                "warnings.simplefilter('error', wx.wxPyDeprecationWarning)\n"
                "import wx.lib.evtmgr\n")
        env = dict(os.environ)
        paths = [os.path.dirname(os.path.dirname(wx.__file__)),
                 env.get('PYTHONPATH')]
        env['PYTHONPATH'] = os.pathsep.join(p for p in paths if p)
        result = subprocess.run([sys.executable, '-c', code], env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_lib_evtmgrRegister(self):
        btn = wx.Button(self.frame)
        received = []
        def listener(evt):
            received.append(evt.GetEventObject())

        eventManager.Register(listener, wx.EVT_BUTTON, btn)
        evt = wx.CommandEvent(wx.wxEVT_BUTTON, btn.GetId())
        evt.SetEventObject(btn)
        btn.GetEventHandler().ProcessEvent(evt)
        eventManager.DeregisterListener(listener)
        self.assertEqual(received, [btn])

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
