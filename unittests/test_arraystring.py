import unittest
import wx
import six

#---------------------------------------------------------------------------

if not six.PY3:
    alt = unicode
else:
    def alt(s):
        return bytes(s, 'utf-8')


class ArrayString(unittest.TestCase):

    if hasattr(wx, 'testArrayStringTypemap'):
        def test_ArrayStringTypemaps(self):
            # basic conversion of list or tuples of strings
            seqList = ['a', alt('b'), 'hello world']
            self.assertEqual(wx.testArrayStringTypemap(seqList), ['a', 'b', 'hello world'])
            seqTuple = ('a', alt('b'), 'hello world')
            self.assertEqual(wx.testArrayStringTypemap(seqTuple), ['a', 'b', 'hello world'])

        def test_ArrayStringTypemapErrors(self):
            # test error conditions
            with self.assertRaises(TypeError):
                wx.testArrayStringTypemap("STRING sequence")
            with self.assertRaises(TypeError):
                wx.testArrayStringTypemap(alt("ALT sequence"))
            with self.assertRaises(TypeError):
                wx.testArrayStringTypemap(["list", "with", "non-string", "items", 123])


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
