import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class mimetype_Tests(wtc.WidgetTestCase):

    def test_mimetype1(self):
        ft = wx.TheMimeTypesManager.GetFileTypeFromExtension('*.pdf')
        if ft:
            ft.GetExtensions()
            ft.GetMimeType()
            ft.GetIcon()

    def test_mimetype2(self):
        ft = wx.TheMimeTypesManager.GetFileTypeFromMimeType('image/png')
        if ft:
            ft.GetExtensions()
            ft.GetMimeType()
            ft.GetIcon()

    def test_mimetype3(self):
        fti = wx.FileTypeInfo('mime', 'open', 'print', 'desc', 'ext1')
        fti.AddExtension('ext2')
        fti.AddExtension('ext3')
        self.assertEqual(fti.GetMimeType(), 'mime')
        self.assertEqual(fti.GetOpenCommand(), 'open')
        self.assertEqual(fti.GetPrintCommand(), 'print')
        self.assertEqual(fti.GetDescription(), 'desc')
        self.assertEqual(fti.GetExtensions(), ['ext1', 'ext2', 'ext3'])
        self.assertEqual(fti.GetExtensionsCount(), 3)

    def test_mimetype4(self):
        fti = wx.FileTypeInfo(['mime', 'open', 'print', 'desc', 'ext1', 'ext2', 'ext3'])
        self.assertEqual(fti.GetMimeType(), 'mime')
        self.assertEqual(fti.GetOpenCommand(), 'open')
        self.assertEqual(fti.GetPrintCommand(), 'print')
        self.assertEqual(fti.GetDescription(), 'desc')
        self.assertEqual(fti.GetExtensions(), ['ext1', 'ext2', 'ext3'])
        self.assertEqual(fti.GetExtensionsCount(), 3)

    def test_mimetype5(self):
        ft = wx.TheMimeTypesManager.GetFileTypeFromMimeType('image/png')
        if ft:
            info = ft.GetIconInfo()
            if info is not None:
                self.assertTrue(isinstance(info, tuple))
                self.assertTrue(len(info) == 3)
                self.assertTrue(isinstance(info[0], wx.Icon))


#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
