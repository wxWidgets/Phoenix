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

    def test_py_sliceshellTutorialMarkers(self):
        shell = sliceshell.SlicesShell(self.frame, introText='PySlices\nPython\nType "help"',
                                       showPySlicesTutorial=True)
        lines = [shell.GetLine(i).rstrip('\r\n') for i in range(shell.GetLineCount())]

        def hasMarker(text, marker):
            return bool(shell.MarkerGet(lines.index(text)) & (1 << marker))

        self.assertTrue(hasMarker('a=1', sliceshell.INPUT_START))
        self.assertTrue(hasMarker('print(a+b)', sliceshell.INPUT_END))
        self.assertTrue(hasMarker('will all run in sequence, much like a script.',
                                  sliceshell.OUTPUT_START))

    def test_py_frameBufferSave(self):
        with mock.patch.object(wx, 'FileSelector', return_value='') as selector:
            pyframe.ShellFrameMixin.bufferSave(mock.Mock())
        self.assertEqual(selector.call_args.kwargs['flags'],
                         wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
