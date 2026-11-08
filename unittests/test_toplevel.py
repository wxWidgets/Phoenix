import unittest
from unittests import wtc
import wx

#---------------------------------------------------------------------------

class GeometryStore(wx.TopLevelWindow.GeometryStore):
    def __init__(self):
        super().__init__()
        self.values = {}

    def SaveValue(self, name, value):
        self.values[name] = value
        return True

    def RestoreValue(self, name):
        return self.values.get(name)


class toplevel_Tests(wtc.WidgetTestCase):

    def test_toplevelGeometryStore(self):
        store = GeometryStore()
        self.assertTrue(self.frame.SaveGeometry(store))
        self.assertEqual(store.values['w'], self.frame.GetSize().width)
        self.assertEqual(store.RestoreValue('w'), self.frame.GetSize().width)
        self.assertIsNone(store.RestoreValue('missing'))
        self.assertIsNone(store.RestoreString('missing'))

        store.values['w'] = 345
        store.values['h'] = 234
        frame = wx.Frame(None)
        self.assertTrue(frame.RestoreToGeometry(store))
        self.assertEqual(frame.GetSize(), (345, 234))
        frame.Destroy()

    def test_toplevelGeometryStoreEmpty(self):
        self.assertFalse(self.frame.RestoreToGeometry(GeometryStore()))

    def test_toplevelGeometryStoreAbstract(self):
        with self.assertRaises(TypeError):
            wx.TopLevelWindow.GeometryStore()

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
