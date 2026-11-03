import os
import tempfile
import unittest
from unittest import mock
from unittests import wtc
import wx

import wx.lib.docview as docview

#---------------------------------------------------------------------------

class TextDocument(docview.Document):
    text = ''

    def SaveObject(self, fileObject):
        fileObject.write(self.text)
        return True

    def LoadObject(self, fileObject):
        self.text = fileObject.read()
        return True


class lib_docview_Tests(wtc.WidgetTestCase):

    def test_lib_docviewSaveAndOpen(self):
        with tempfile.TemporaryDirectory() as tempDir:
            filename = os.path.join(tempDir, 'doc.txt')
            doc = TextDocument()
            doc.text = 'contents'
            self.assertTrue(doc.OnSaveDocument(filename))

            doc = TextDocument()
            self.assertTrue(doc.OnOpenDocument(filename))
            self.assertEqual(doc.text, 'contents')

    def test_lib_docviewTemplateSetIcon(self):
        manager = docview.DocManager(initialize=False)
        template = docview.DocTemplate(manager, 'Text', '*.txt', '', 'txt', 'Text', 'Text',
                                       TextDocument, docview.View)
        icon = wx.Icon(wx.Bitmap(16, 16))
        template.SetIcon(icon)
        self.assertIs(template.GetIcon(), icon)

    def test_lib_docviewMakeFrameTitle(self):
        manager = docview.DocManager(initialize=False)
        doc = TextDocument()
        doc.SetTitle('Title')
        appName = wx.GetApp().GetAppName()
        self.assertEqual(manager.MakeFrameTitle(), appName)
        self.assertEqual(manager.MakeFrameTitle(doc), 'Title - ' + appName)

    def test_lib_docviewSelectSortedTemplates(self):
        manager = docview.DocManager(initialize=False)
        templates = [docview.DocTemplate(manager, name, '*.txt', '', 'txt', name, name,
                                         TextDocument, docview.View, flags=docview.TEMPLATE_VISIBLE)
                     for name in ('b', 'a')]
        with mock.patch.object(wx, 'SingleChoiceDialog') as dialog:
            dialog.return_value.ShowModal.return_value = wx.ID_OK
            dialog.return_value.GetSelection.return_value = 0
            self.assertIs(manager.SelectDocumentType(templates, sort=True), templates[1])
            self.assertIs(manager.SelectViewType(templates, sort=True), templates[1])

#---------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
