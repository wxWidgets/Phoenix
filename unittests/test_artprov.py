import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class artprov_Tests(wtc.WidgetTestCase):

    def test_artprovConstants(self):
        wx.ART_TOOLBAR
        wx.ART_MENU
        wx.ART_FRAME_ICON
        wx.ART_CMN_DIALOG
        wx.ART_HELP_BROWSER
        wx.ART_MESSAGE_BOX
        wx.ART_BUTTON
        wx.ART_LIST
        wx.ART_OTHER
        wx.ART_ADD_BOOKMARK
        wx.ART_DEL_BOOKMARK
        wx.ART_HELP_SIDE_PANEL
        wx.ART_HELP_SETTINGS
        wx.ART_HELP_BOOK
        wx.ART_HELP_FOLDER
        wx.ART_HELP_PAGE
        wx.ART_GO_BACK
        wx.ART_GO_FORWARD
        wx.ART_GO_UP
        wx.ART_GO_DOWN
        wx.ART_GO_TO_PARENT
        wx.ART_GO_HOME
        wx.ART_GOTO_FIRST
        wx.ART_GOTO_LAST
        wx.ART_FILE_OPEN
        wx.ART_FILE_SAVE
        wx.ART_FILE_SAVE_AS
        wx.ART_PRINT
        wx.ART_HELP
        wx.ART_TIP
        wx.ART_REPORT_VIEW
        wx.ART_LIST_VIEW
        wx.ART_NEW_DIR
        wx.ART_HARDDISK
        wx.ART_FLOPPY
        wx.ART_CDROM
        wx.ART_REMOVABLE
        wx.ART_FOLDER
        wx.ART_FOLDER_OPEN
        wx.ART_GO_DIR_UP
        wx.ART_EXECUTABLE_FILE
        wx.ART_NORMAL_FILE
        wx.ART_TICK_MARK
        wx.ART_CROSS_MARK
        wx.ART_ERROR
        wx.ART_QUESTION
        wx.ART_WARNING
        wx.ART_INFORMATION
        wx.ART_MISSING_IMAGE
        wx.ART_COPY
        wx.ART_CUT
        wx.ART_PASTE
        wx.ART_DELETE
        wx.ART_NEW
        wx.ART_UNDO
        wx.ART_REDO
        wx.ART_PLUS
        wx.ART_MINUS
        wx.ART_CLOSE
        wx.ART_QUIT
        wx.ART_FIND
        wx.ART_FIND_AND_REPLACE


    def test_artprovGetBitmap(self):
        bmp = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_TOOLBAR)
        self.assertTrue(isinstance(bmp, wx.Bitmap))


    def test_artprovConstantsAreStr(self):
        self.assertEqual(wx.ART_MENU, 'wxART_MENU_C')
        self.assertEqual(wx.ART_FILE_OPEN, 'wxART_FILE_OPEN')
        for name in dir(wx):
            if name.startswith('ART_'):
                self.assertIsInstance(getattr(wx, name), str, name)


    def test_artprovCustomProvider(self):
        # The IDs passed to a Python provider should compare equal to the
        # wx.ART_* constants used to request the art.
        calls = []
        class MyProvider(wx.ArtProvider):
            def CreateBitmap(self, artid, client, size):
                calls.append((artid, client))
                if artid == wx.ART_GO_BACK and client == wx.ART_MENU:
                    return wx.Bitmap(16, 16)
                return wx.NullBitmap

        provider = MyProvider()
        wx.ArtProvider.Push(provider)
        try:
            bmp = wx.ArtProvider.GetBitmap(wx.ART_GO_BACK, wx.ART_MENU)
        finally:
            wx.ArtProvider.Remove(provider)
        self.assertIn((wx.ART_GO_BACK, wx.ART_MENU), calls)
        self.assertTrue(bmp.IsOk())
        self.assertEqual(bmp.GetSize(), (16, 16))


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
