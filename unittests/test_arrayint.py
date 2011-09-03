import unittest2
import wx


#---------------------------------------------------------------------------

class ArrayInt(unittest2.TestCase):
        
    if hasattr(wx, 'testArrayIntTypemap'):
        def test_ArrayStringTypemaps(self):
            # basic conversion of list or tuples of numbers
            seqList = [1,2,3,4.5,6.7]
            self.assertEqual(wx.testArrayIntTypemap(seqList), [1,2,3,4,6]) #floats are truncated to int
            seqTuple = (1,2,3,4.5,6.7)
            self.assertEqual(wx.testArrayIntTypemap(seqTuple), [1,2,3,4,6])
            
        def test_ArrayIntTypemapErrors(self):
            # test error conditions
            with self.assertRaises(TypeError):
                wx.testArrayIntTypemap([1,2,3, "baditem", ["listitem"]])
            

#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest2.main()
