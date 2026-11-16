import os
import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.py.shell as pyshell

#---------------------------------------------------------------------------

class py_shell_Tests(wtc.WidgetTestCase):

    def test_py_shellHelpOutput(self):
        shell = pyshell.Shell(self.frame)
        # pydoc would pipe the text through this pager instead if the
        # shell's streams claimed to be terminals
        with mock.patch.dict(os.environ, {'PAGER': 'cat'}):
            shell.push('help(len)')
        self.assertIn('Return the number of items', shell.GetText())

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
