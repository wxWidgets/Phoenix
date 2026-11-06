"""
A small text editor showing how to build an application with
wx.lib.pydocview, which adds services, tabbed MDI and default frames on top of
the wx.lib.docview document/view framework.

The document interface (one window per document, tabs, or on Windows MDI child
windows) can be changed in Tools/Options and takes effect after a restart.
"""

import wx
import wx.lib.docview as docview
import wx.lib.pydocview as pydocview

_ = wx.GetTranslation


class TextEditDocument(docview.Document):

    def SaveObject(self, fileObject):
        fileObject.write(self.GetFirstView().GetText())
        return True

    def LoadObject(self, fileObject):
        self.GetFirstView().SetText(fileObject.read())
        return True


class TextEditView(docview.View):

    # Events can arrive while the frame is being created, before the text control exists
    _text = None

    def OnCreate(self, doc, flags):
        frame = wx.GetApp().CreateDocumentFrame(self, doc, flags)
        self._text = wx.TextCtrl(frame, style=wx.TE_MULTILINE)
        self._text.Bind(wx.EVT_TEXT, self.OnText)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._text, 1, wx.EXPAND)
        frame.SetSizer(sizer)
        frame.Layout()
        self.Activate()
        return True

    def GetText(self):
        return self._text.GetValue()

    def SetText(self, text):
        self._text.ChangeValue(text)

    def OnText(self, event):
        if not self.GetDocument().IsModified():
            self.GetDocument().Modify(True)

    def OnActivateView(self, activate, activeView, deactiveView):
        if activate and self._text:
            self._text.SetFocus()

    def OnClose(self, deleteWindow=True):
        if not docview.View.OnClose(self, deleteWindow):
            return False
        self.Activate(False)
        if deleteWindow and self.GetFrame():
            self.GetFrame().Destroy()
        return True

    def ProcessEvent(self, event):
        if not self._text:
            return docview.View.ProcessEvent(self, event)
        actions = {
            wx.ID_CUT: self._text.Cut,
            wx.ID_COPY: self._text.Copy,
            wx.ID_PASTE: self._text.Paste,
            wx.ID_CLEAR: lambda: self._text.Remove(*self._text.GetSelection()),
            wx.ID_SELECTALL: self._text.SelectAll,
        }
        action = actions.get(event.GetId())
        if action:
            action()
            return True
        return docview.View.ProcessEvent(self, event)

    def ProcessUpdateUIEvent(self, event):
        if not self._text:
            return docview.View.ProcessUpdateUIEvent(self, event)
        id = event.GetId()
        if id in (wx.ID_CUT, wx.ID_CLEAR):
            event.Enable(self._text.CanCut())
        elif id == wx.ID_COPY:
            event.Enable(self._text.CanCopy())
        elif id == wx.ID_PASTE:
            event.Enable(self._text.CanPaste())
        elif id == wx.ID_SELECTALL:
            event.Enable(self._text.GetLastPosition() > 0)
        else:
            return docview.View.ProcessUpdateUIEvent(self, event)
        return True


class PyDocViewSampleApp(pydocview.DocApp):

    def OnInit(self):
        self.SetAppName("PyDocView Sample")
        if not pydocview.DocApp.OnInit(self):
            # Another instance is running and has been asked to open our files
            return False

        config = wx.Config(self.GetAppName(), style=wx.CONFIG_USE_LOCAL_FILE)
        wx.ConfigBase.Set(config)

        docManager = docview.DocManager(flags=self.GetDefaultDocManagerFlags())
        self.SetDocumentManager(docManager)

        template = docview.DocTemplate(docManager, _("Text"), "*.txt", "", "txt",
                                       _("Text Document"), _("Text View"),
                                       TextEditDocument, TextEditView)
        docManager.AssociateTemplate(template)

        self.InstallService(pydocview.DocOptionsService())
        self.InstallService(pydocview.WindowMenuService())
        self.InstallService(pydocview.FilePropertiesService())
        self.InstallService(pydocview.AboutService())

        self.OpenMainFrame()
        self.OpenCommandLineArgs()
        if not docManager.GetDocuments() and docManager.GetFlags() & docview.DOC_SDI:
            template.CreateDocument('', docview.DOC_NEW).OnNewDocument()
        return True


def main():
    app = PyDocViewSampleApp(redirect=False)
    app.MainLoop()


if __name__ == '__main__':
    main()
