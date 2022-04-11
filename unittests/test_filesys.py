import unittest
from unittests import wtc
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

    def test_filesys02(self):
        wx.FileSystem.AddHandler(wx.ArchiveFSHandler())

    def test_filesys03(self):
        wx.FileSystem.AddHandler(wx.InternetFSHandler())

    def test_filesys04(self):
        wx.FileSystem.AddHandler(wx.MemoryFSHandler())

    def test_filesysMemoryFSHandler(self):
        memoryFS = wx.MemoryFSHandler()
        memoryFS.AddFile('test.txt', 'This is a test')
        self.assertTrue(memoryFS.FindFirst('test.txt') == 'test.txt')

    # TODO: Add more tests.

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
