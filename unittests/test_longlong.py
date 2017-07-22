
import unittest
import wx

#---------------------------------------------------------------------------

class longlong_Tests(unittest.TestCase):

    def test_longlong(self):
        val1 = 2**50  # make a big value

        # setting the timespan's seconds property will use the mapped type
        # code to convert to a wxLongLong...
        ts = wx.TimeSpan(hours=0, min=0, sec=val1)

        # ...and fetching it from the timespan will use the mapped type to
        # convert back from a wxLongLong to a Python object...
        val2 = ts.GetSeconds()

        # ...which we can compare with the original.
        self.assertTrue(val1 == val2)


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
