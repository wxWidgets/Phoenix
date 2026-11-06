import os
import pathlib
import tempfile
import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

pngFile = pathlib.Path(__file__).parent / 'toucan.png'


class FSPath:
    """An os.PathLike that is not a pathlib.Path"""
    def __init__(self, path):
        self.path = path

    def __fspath__(self):
        return self.path


class BadFSPath:
    def __fspath__(self):
        raise ValueError('bad path')


class pathlike_Tests(wtc.WidgetTestCase):

    def test_pathlikeFileDialog(self):
        # The native dialogs on GTK don't report these until they are shown
        dlg = wx.FileDialog(self.frame, defaultDir=pngFile.parent,
                            defaultFile=pathlib.Path(pngFile.name))
        dlg.SetDirectory(FSPath(str(pngFile.parent)))
        dlg.SetPath(pngFile)
        dlg.Destroy()

    def test_pathlikeDirDialog(self):
        dlg = wx.DirDialog(self.frame, defaultPath=pngFile.parent)
        dlg.SetPath(pngFile.parent)
        dlg.Destroy()

    def test_pathlikePickers(self):
        picker = wx.FilePickerCtrl(self.frame, path=pngFile)
        assert picker.GetPath() == str(pngFile)
        picker.SetPath(FSPath(str(pngFile)))
        assert picker.GetPath() == str(pngFile)
        picker = wx.DirPickerCtrl(self.frame, path=pngFile.parent)
        assert picker.GetPath() == str(pngFile.parent)

    def test_pathlikeImage(self):
        assert wx.Image(pngFile).IsOk()
        assert wx.Image(pngFile, wx.BITMAP_TYPE_PNG).IsOk()
        assert wx.Image(pngFile, 'image/png').IsOk()
        assert wx.Image().LoadFile(FSPath(str(pngFile)))
        assert wx.Image.CanRead(pngFile)

    def test_pathlikeImageSave(self):
        img = wx.Image(pngFile)
        with tempfile.TemporaryDirectory() as tmpdir:
            name = pathlib.Path(tmpdir) / 'saved.png'
            assert img.SaveFile(name, wx.BITMAP_TYPE_PNG)
            assert name.exists()

    def test_pathlikeBitmap(self):
        assert wx.Bitmap(pngFile).IsOk()
        assert wx.Bitmap().LoadFile(pngFile)

    def test_pathlikeBytes(self):
        assert wx.Image(FSPath(os.fsencode(pngFile))).IsOk()

    def test_pathlikeFileName(self):
        url = wx.FileSystem.FileNameToURL(str(pngFile))
        assert wx.FileSystem.FileNameToURL(pngFile) == url
        assert wx.FileSystem.FileNameToURL(FSPath(str(pngFile))) == url

    def test_pathlikeStillAcceptsStrings(self):
        picker = wx.FilePickerCtrl(self.frame, path=str(pngFile))
        assert picker.GetPath() == str(pngFile)

    def test_pathlikeErrors(self):
        with self.assertRaises(TypeError):
            wx.FileDialog(self.frame, defaultDir=123)
        with self.assertRaises(TypeError):
            wx.FileDialog(self.frame, defaultDir=FSPath(123))
        with self.assertRaises(ValueError):
            wx.FileDialog(self.frame, defaultDir=BadFSPath())

    def test_pathlikeOnlyForPaths(self):
        with self.assertRaises(TypeError):
            wx.StaticText(self.frame, label=pathlib.Path('label'))

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
