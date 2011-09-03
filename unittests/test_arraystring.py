import unittest2
import wx


#---------------------------------------------------------------------------

class ArrayString(unittest2.TestCase):
        
    if hasattr(wx, 'testArrayStringTypemap'):
        def test_ArrayStringTypemaps(self):
            # basic conversion of list or tuples of strings
            seqList = ['a', u'b', 'hello world']
            self.assertEqual(wx.testArrayStringTypemap(seqList), seqList)
            seqTuple = ('a', u'b', 'hello world')
            self.assertEqual(wx.testArrayStringTypemap(seqTuple), list(seqTuple))
            
        def test_ArrayStringTypemapErrors(self):
            # test error conditions
            with self.assertRaises(TypeError):
                wx.testArrayStringTypemap("STRING sequence")
            with self.assertRaises(TypeError):
                wx.testArrayStringTypemap(u"UNICODE sequence")
            with self.assertRaises(TypeError):
                wx.testArrayStringTypemap(["list", "with", "non-string", "items", 123])
            

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest2.main()
