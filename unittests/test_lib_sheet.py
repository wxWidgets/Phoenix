import unittest
from unittests import wtc
import wx

import wx.lib.sheet as sheet

#---------------------------------------------------------------------------

class lib_sheet_Tests(wtc.WidgetTestCase):

    def test_lib_sheet_Ctor(self):
        sheet.CSheet(self.frame)

    def test_lib_sheet_EditCell(self):
        s = sheet.CSheet(self.frame)
        s.SetGridCursor(1, 1)
        s.EnableCellEditControl()
        controls = [w for w in s.GetGridWindow().GetChildren() if isinstance(w, wx.TextCtrl)]
        controls[0].SetValue('hello')
        s.DisableCellEditControl()
        self.assertEqual(s.GetCellValue(1, 1), 'hello')


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
