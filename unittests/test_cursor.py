import unittest
from unittests import wtc
import wx
import six
import os

pngFile = os.path.join(os.path.dirname(__file__), 'pointy.png')
curFile = os.path.join(os.path.dirname(__file__), 'horse.cur')

#---------------------------------------------------------------------------

class CursorTests(wtc.WidgetTestCase):

    def test_CursorCtors(self):
        # stock
        c = wx.Cursor(wx.CURSOR_HAND)
        self.assertTrue(c.IsOk())

        # from file
        c = wx.Cursor(curFile, wx.BITMAP_TYPE_CUR)
        self.assertTrue(c.IsOk())

        # from image
        img = wx.Image(pngFile)
        img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_X, 1)
        img.SetOption(wx.IMAGE_OPTION_CUR_HOTSPOT_Y, 1)
        c = wx.Cursor(img)
        self.assertTrue(c.IsOk())

        # copy
        c2 = wx.Cursor(c)
        self.assertTrue(c2.IsOk())


    def test_CursorStockIDsExist(self):
        wx.CURSOR_ARROW
        wx.CURSOR_RIGHT_ARROW
        wx.CURSOR_BULLSEYE
        wx.CURSOR_CHAR
        wx.CURSOR_CROSS
        wx.CURSOR_HAND
        wx.CURSOR_IBEAM
        wx.CURSOR_LEFT_BUTTON
        wx.CURSOR_MAGNIFIER
        wx.CURSOR_MIDDLE_BUTTON
        wx.CURSOR_NO_ENTRY
        wx.CURSOR_PAINT_BRUSH
        wx.CURSOR_PENCIL
        wx.CURSOR_POINT_LEFT
        wx.CURSOR_POINT_RIGHT
        wx.CURSOR_QUESTION_ARROW
        wx.CURSOR_RIGHT_BUTTON
        wx.CURSOR_SIZENESW
        wx.CURSOR_SIZENS
        wx.CURSOR_SIZENWSE
        wx.CURSOR_SIZEWE
        wx.CURSOR_SIZING
        wx.CURSOR_SPRAYCAN
        wx.CURSOR_WAIT
        wx.CURSOR_WATCH
        wx.CURSOR_BLANK
        wx.CURSOR_DEFAULT
        wx.CURSOR_COPY_ARROW
        wx.CURSOR_ARROWWAIT


    def test_Cursor__nonzero__(self):
        c1 = wx.Cursor()
        self.assertTrue( not c1.IsOk() )

        c2 = wx.Cursor(wx.CURSOR_ARROW)
        self.assertTrue( c2.IsOk() )
        if six.PY3:
            self.assertTrue( c2.__bool__() == c2.IsOk() )
        else:
            self.assertTrue( c2.__nonzero__() == c2.IsOk() )

        # check that the __nonzero__ method can be used with if statements
        nzcheck = False
        if c2:
            nzcheck = True
        self.assertTrue(nzcheck)
        nzcheck = False
        if not c1:
            nzcheck = True
        self.assertTrue(nzcheck)


    def test_NullCursor(self):
        # just make sure this one exists
        wx.NullCursor
        self.assertTrue(not wx.NullCursor.IsOk())


    def test_StockCursorsExist(self):
        wx.STANDARD_CURSOR
        wx.HOURGLASS_CURSOR
        wx.CROSS_CURSOR

    def test_StockCursorsInitialized(self):
        self.assertTrue(wx.STANDARD_CURSOR.IsOk())
        self.assertTrue(wx.HOURGLASS_CURSOR.IsOk())
        self.assertTrue(wx.CROSS_CURSOR.IsOk())


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
