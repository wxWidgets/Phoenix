import unittest
import wx
import six
from unittests import wtc

#---------------------------------------------------------------------------



class String(unittest.TestCase):

    if hasattr(wx, 'testStringTypemap'):
        if not six.PY3:
            def test_StringTypemapsPy2(self):
                utf  = '\xc3\xa9l\xc3\xa9phant'     # utf-8 string
                uni  = utf.decode('utf-8')          # convert to unicode
                iso  = uni.encode('iso-8859-1')     # make a string with a different encoding


                # wx.testStringTypemap() will accept a parameter that
                # is a Unicode object or an 'ascii' or 'utf-8' string object,
                # which will then be converted to a wxString. The return
                # value is a Unicode object that has been converted from a
                # wxString that is a copy of the wxString created for the
                # parameter.

                # ascii
                result = wx.testStringTypemap('hello')
                self.assertTrue(type(result) == unicode)
                self.assertTrue(result == unicode('hello'))

                # unicode should pass through unmodified
                result = wx.testStringTypemap(uni)
                self.assertTrue(result == uni)

                # utf-8 is converted
                result = wx.testStringTypemap(utf)
                self.assertTrue(result == uni)

                # can't auto-convert this
                with self.assertRaises(UnicodeDecodeError):
                    result = wx.testStringTypemap(iso)

                # utf-16-be
                val = "\x00\xe9\x00l\x00\xe9\x00p\x00h\x00a\x00n\x00t"
                with self.assertRaises(UnicodeDecodeError):
                    result = wx.testStringTypemap(val)
                result = wx.testStringTypemap( val.decode('utf-16-be'))
                self.assertTrue(result == uni)

                # utf-32-be
                val = "\x00\x00\x00\xe9\x00\x00\x00l\x00\x00\x00\xe9\x00\x00\x00p\x00\x00\x00h\x00\x00\x00a\x00\x00\x00n\x00\x00\x00t"
                with self.assertRaises(UnicodeDecodeError):
                    result = wx.testStringTypemap(val)
                result = wx.testStringTypemap(val.decode('utf-32-be'))
                self.assertTrue(result == uni)

                # utf-8 with BOM
                #val = "\xef\xbb\xbfHello"
                #result = wx.testStringTypemap(val)
                #self.assertTrue(result == u'\ufeffHello')

        else:
            def test_StringTypemapsPy3(self):
                utf  = b'\xc3\xa9l\xc3\xa9phant'    # utf-8 bytes
                uni  = utf.decode('utf-8')          # convert to unicode
                iso  = uni.encode('iso-8859-1')     # make a string with a different encoding

                # ascii
                result = wx.testStringTypemap(b'hello')
                self.assertTrue(type(result) == str)
                self.assertTrue(result == 'hello')

                # unicode should pass through unmodified
                result = wx.testStringTypemap(uni)
                self.assertTrue(result == uni)

                # utf-8 is converted
                result = wx.testStringTypemap(utf)
                self.assertTrue(result == uni)

                # can't auto-convert this
                with self.assertRaises(UnicodeDecodeError):
                    result = wx.testStringTypemap(iso)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
