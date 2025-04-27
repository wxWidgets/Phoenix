#!/usr/bin/env python

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"

import unittest

from wx.py import pseudo


"""
These unittest methods are preferred:
-------------------------------------
self.assertTrue(expr, msg=None)
self.assertEqual(first, second, msg=None)
self.assertRaises(excClass, callableObj, *args, **kwargs)
self.fail(msg=None)
self.failIf(expr, msg=None)
"""


class ModuleTestCase(unittest.TestCase):

    def test_module(self):
        module = pseudo
        self.assertTrue(module.__author__)
        self.assertTrue(module.PseudoFile)
        self.assertTrue(module.PseudoFileErr)
        self.assertTrue(module.PseudoFileIn)
        self.assertTrue(module.PseudoFileOut)
        self.assertTrue(module.PseudoKeyword)


class PseudoTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class PseudoFileTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


class PseudoFileOutTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _write(self):
        pass

    def test_PseudoFileOut_goodInit(self):
        self.assertTrue(pseudo.PseudoFileOut(write=self._write))

    def test_PseudoFileOut_badInit(self):
        self.assertRaises(ValueError, pseudo.PseudoFileOut, write='bad')


if __name__ == '__main__':
    unittest.main()
