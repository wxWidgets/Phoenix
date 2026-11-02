import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.py.frame as pyframe
import wx.py.sliceshell as sliceshell

#---------------------------------------------------------------------------

class py_slices_Tests(wtc.WidgetTestCase):

    def test_py_sliceshellExecute(self):
        shell = sliceshell.SlicesShell(self.frame)
        shell.Execute('testPySlicesValue = 1')
        self.assertIn('testPySlicesValue', shell.interp.locals)

    def test_py_sliceshellCompletionHistory(self):
        shell = sliceshell.SlicesShell(self.frame)
        shell.history = ['bbb AAA ccc']
        shell.OnShowCompHistory()

    def test_py_frameBufferSave(self):
        with mock.patch.object(wx, 'FileSelector', return_value='') as selector:
            pyframe.ShellFrameMixin.bufferSave(mock.Mock())
        self.assertEqual(selector.call_args.kwargs['flags'],
                         wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
