
import unittest2
import wxPhoenix as wx

#---------------------------------------------------------------------------

class String(unittest2.TestCase):
        
    if hasattr(wx, 'testStringTypemap'):
        def test_StringTypemaps(self):
            utf  = '\xc3\xa9l\xc3\xa9phant'    # utf-8 string
            uni  = utf.decode('utf-8')         # convert to unicode
            iso  = uni.encode('iso-8859-1')    # make a string with a different encoding

            
            # wx.testStringTypemap() will accept a parameter that is a Unicode object 
            # or an 'ascii' or 'utf-8' string object, which will then be converted to 
            # a wxString.  The return value is a Unicode object that has been 
            # converted from a wxString that is a copy of the wxString created for 
            # the parameter.
            
            # ascii
            result = wx.testStringTypemap('hello')
            self.assertTrue(type(result) == unicode)
            self.assertTrue(result == u'hello')
                   
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
            val = "\xef\xbb\xbfHello"
            result = wx.testStringTypemap(val)
            self.assertTrue(result == u'\ufeffHello')

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest2.main()
