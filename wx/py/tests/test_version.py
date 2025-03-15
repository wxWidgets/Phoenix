#!/usr/bin/env python

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"

import unittest

from wx.py import version


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
        module = version
        self.assertTrue(module.__author__)
        self.assertTrue(module.VERSION)


class VersionTestCase(unittest.TestCase):

    def test_VERSION(self):
        self.assertTrue(isinstance(version.VERSION, str))


if __name__ == '__main__':
    unittest.main()
