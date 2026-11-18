import unittest
from unittests import wtc
import wx

import wx.py.filling as filling

#---------------------------------------------------------------------------

class Inner:
    evaluated = 0

    @property
    def value(self):
        Inner.evaluated += 1
        return 42


class Outer:
    def __init__(self):
        self.inner = Inner()


class py_filling_Tests(wtc.WidgetTestCase):

    def findChild(self, tree, parent, text):
        child, cookie = tree.GetFirstChild(parent)
        while child.IsOk():
            if tree.GetItemText(child) == text:
                return child
            child, cookie = tree.GetNextChild(parent, cookie)
        self.fail('no child %r' % text)

    def test_py_fillingExpandDoesNotEvaluateGrandchildren(self):
        # Expanding an item used to get the attribute values of each of its
        # children too, running property getters nobody asked for
        Inner.evaluated = 0
        tree = filling.FillingTree(self.frame, rootObject={'outer': Outer()},
                                   rootIsNamespace=True)
        tree.Expand(tree.root)
        outer = self.findChild(tree, tree.root, 'outer')
        self.assertTrue(tree.ItemHasChildren(outer))
        tree.Expand(outer)
        inner = self.findChild(tree, outer, 'inner')
        self.assertTrue(tree.ItemHasChildren(inner))
        self.assertEqual(Inner.evaluated, 0)

        tree.Expand(inner)
        self.assertEqual(tree.GetItemData(self.findChild(tree, inner, 'value')), 42)
        self.assertEqual(Inner.evaluated, 1)

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
