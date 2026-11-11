import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.lib.printout as printout

#---------------------------------------------------------------------------

class FakePrinter:
    calls = []

    def __init__(self, pdd):
        self.pdd = pdd

    def Print(self, parent, printout, prompt=True):
        self.calls.append(prompt)
        return True

    def GetPrintDialogData(self):
        return self.pdd


class lib_printout_Tests(wtc.WidgetTestCase):

    def test_lib_printout_PrintTablePrompt(self):
        table = printout.PrintTable(self.frame)
        table.data = [['a', 'b'], ['c', 'd']]
        FakePrinter.calls = []
        with mock.patch('wx.Printer', FakePrinter):
            table.Print()
            table.Print(prompt=False)
        self.assertEqual(FakePrinter.calls, [True, False])


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
