import unittest
import wx
from unittests import wtc

#---------------------------------------------------------------------------



class String(unittest.TestCase):

    if hasattr(wx, 'testStringTypemap'):
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
