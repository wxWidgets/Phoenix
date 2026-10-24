import os
import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.lib.filebrowsebutton as fbb

#---------------------------------------------------------------------------

class FakeDialog:
    """
    Stands in for the dialogs so the tests can check how they would be
    created without showing them.
    """
    created = []

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        FakeDialog.created.append(self)

    def ShowModal(self):
        return wx.ID_CANCEL

    def Destroy(self):
        pass


class lib_filebrowsebutton_Tests(wtc.WidgetTestCase):

    def setUp(self):
        super().setUp()
        FakeDialog.created = []

    def test_lib_filebrowsebuttonCtor(self):
        fbb.FileBrowseButton(self.frame)
        fbb.FileBrowseButtonWithHistory(self.frame)
        fbb.DirBrowseButton(self.frame)

    def test_lib_filebrowsebuttonStartDirectoryIsAbsolute(self):
        btn = fbb.FileBrowseButton(self.frame)
        with mock.patch.object(wx, 'FileDialog', FakeDialog):
            btn.OnBrowse()
        self.assertEqual(FakeDialog.created[0].args[2], os.path.abspath('.'))

    def test_lib_filebrowsebuttonDirStartDirectoryIsAbsolute(self):
        btn = fbb.DirBrowseButton(self.frame, dialogClass=FakeDialog)
        btn.OnBrowse()
        self.assertEqual(FakeDialog.created[0].kwargs['defaultPath'],
                         os.path.abspath('.'))

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
