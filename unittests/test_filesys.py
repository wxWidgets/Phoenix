import imp_unittest, unittest
import wtc
import wx
import os


#---------------------------------------------------------------------------

class filesys_Tests(wtc.WidgetTestCase):

    def test_filesysClasses(self):
        # For now just test that the expected classes exist.  
        wx.FileSystem
        wx.FSFile
        wx.FileSystemHandler
        wx.MemoryFSHandler
        wx.ArchiveFSHandler
        wx.FilterFSHandler
        wx.InternetFSHandler
        wx.ZipFSHandler

    # TODO: Add more tests.
        
#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
