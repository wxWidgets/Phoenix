import unittest
import ast
import os
import wx

#---------------------------------------------------------------------------

PI_MODULES = [
    'adv', 'aui', 'core', 'dataview', 'glcanvas', 'grid', 'html', 'html2',
    'media', 'propgrid', 'ribbon', 'richtext', 'stc', 'xml', 'xrc',
]

if 'wxMSW' in wx.PlatformInfo:
    PI_MODULES.append('msw')


class PIImportTest(unittest.TestCase):
    """
    The *.pyi files generated are used with some IDE's to create things like
    autocomplete lists and call tips. They are PEP 484 stub files: code meant
    to be read by static analysis tools such as mypy or pyright, not to be
    executed. Stub syntax intentionally allows things that aren't valid at
    runtime (e.g. a class referring to itself in a default argument value),
    so this test just checks that each expected .pyi file was generated and
    is parseable as Python, which is all that's required for it to be usable
    by IDEs and type checkers.
    """

    def test_pi_files(self):
        wx_dir = os.path.dirname(wx.__file__)

        for modname in PI_MODULES:
            filename = os.path.join(wx_dir, modname + '.pyi')
            with self.subTest(filename=modname + '.pyi'):
                self.assertTrue(os.path.isfile(filename),
                                 '%s was not generated' % filename)
                with open(filename, encoding='utf-8') as f:
                    source = f.read()
                try:
                    ast.parse(source, filename=filename)
                except SyntaxError as e:
                    self.fail('%s: %s' % (filename, e))


#---------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()
