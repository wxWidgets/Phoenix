import unittest


class sphinxtools_utilities_Tests(unittest.TestCase):

    def setUp(self):
        # etgtools has to be imported first to avoid a circular import
        import etgtools
        from sphinxtools import utilities
        self.utilities = utilities

    def test_pythonizeTypeCharPointer(self):
        pythonizeType = self.utilities.pythonizeType
        self.assertEqual(pythonizeType('const char *', True), 'string')
        self.assertEqual(pythonizeType('char *', True), 'string')
        self.assertEqual(pythonizeType('unsigned char *', True), 'int')

    def test_pythonizeTypeHint(self):
        pythonizeTypeHint = self.utilities.pythonizeTypeHint
        self.assertEqual(pythonizeTypeHint('int'), 'int')
        self.assertEqual(pythonizeTypeHint('str'), 'string')
        self.assertEqual(pythonizeTypeHint('Buffer'), 'Buffer')
        self.assertEqual(pythonizeTypeHint('Union[Size, _TwoInts]'), 'wx.Size')
        self.assertEqual(pythonizeTypeHint('Optional[Union[Rect, _FourInts]]'), 'wx.Rect')
        self.assertEqual(pythonizeTypeHint('Union[DataObject.Direction, int]'),
                         'wx.DataObject.Direction')
        self.assertEqual(pythonizeTypeHint('Union[Colour, _ThreeInts, _FourInts, str, None]'),
                         'wx.Colour or string')
        self.assertEqual(pythonizeTypeHint('wx.grid.Grid'), 'wx.grid.Grid')

    def test_replaceCppItemsKeepsProducts(self):
        replaceCppItems = self.utilities.replaceCppItems
        self.assertEqual(replaceCppItems('at least width*height*4 bytes'),
                         'at least width*height*4 bytes')
        self.assertEqual(replaceCppItems('Pass a wxWindow* here'), 'Pass a wxWindow here')


if __name__ == '__main__':
    unittest.main()
