import unittest
from unittests import wtc
import wx
import sys

#---------------------------------------------------------------------------

class fontenum_Tests(wtc.WidgetTestCase):

    @unittest.skipIf(sys.platform == 'darwin', 'EnumerateEncodings not implemented on Mac')
    def test_fontenum1(self):
        enc = wx.FontEnumerator.GetEncodings()
        self.assertTrue(isinstance(enc, list))
        self.assertTrue(len(enc) > 0)

    def test_fontenum2(self):
        faces = wx.FontEnumerator.GetFacenames()
        self.assertTrue(isinstance(faces, list))
        self.assertTrue(len(faces) > 0)

        fw_faces = wx.FontEnumerator.GetFacenames(fixedWidthOnly=True)
        self.assertTrue(len(fw_faces) < len(faces))


    def test_fontenum3(self):
        class MyFontEnumerator(wx.FontEnumerator):
            def __init__(self):
                wx.FontEnumerator.__init__(self)
                self.my_faces = list()
                self.my_enc = list()

            def OnFacename(self, name):
                self.my_faces.append(name)
                return len(self.my_faces) < 5  # quit when we've got 5
            def OnFontEncoding(self, facename, encoding):
                self.my_enc.append( (facename, encoding) )
                return len(self.my_enc) < 5  # quit when we've got 5

        mfe = MyFontEnumerator()
        mfe.EnumerateFacenames()
        self.assertTrue(len(mfe.my_faces) > 0 and len(mfe.my_faces) <= 5)

        if sys.platform != 'darwin':
            mfe.EnumerateEncodings()
            self.assertTrue(len(mfe.my_enc) > 0 and len(mfe.my_enc) <= 5)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
