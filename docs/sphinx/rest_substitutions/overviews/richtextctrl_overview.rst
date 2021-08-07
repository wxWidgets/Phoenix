.. include:: headings.inc


.. _richtextctrl overview:

==========================================
|phoenix_title|  **RichTextCtrl Overview**
==========================================


Introduction
------------

:class:`~wx.richtext.RichTextCtrl` provides a generic implementation of a
rich text editor that can handle different character styles, paragraph
formatting, and images.

It's aimed at editing 'natural' language text - if you need an editor
that supports code editing, :class:`wx.stc.StyledTextCtrl` is a better choice.

Despite its name, it cannot currently read or write RTF (rich text
format) files. Instead, it uses its own XML format, and can also read
and write plain text. In future we expect to provide RTF or
OpenDocument file capabilities. Custom file formats can be supported
by creating additional file handlers and registering them with the
control.

:class:`~wx.richtext.RichTextCtrl` is largely compatible with the
:class:`wx.TextCtrl` API, but extends it where necessary. The control can
be used where the native rich text capabilities of :class:`wx.TextCtrl`
are not adequate (this is particularly true on Windows) and where more
direct access to the content representation is required. It is
difficult and inefficient to read the style information in a
:class:`wx.TextCtrl`, whereas this information is readily available in
:class:`~wx.richtext.RichTextCtrl`. Since it's written in pure wxWidgets,
any customizations you make to :class:`~wx.richtext.RichTextCtrl` will be
reflected on all platforms.

:class:`~wx.richtext.RichTextCtrl` supports basic printing via the
easy-to-use :class:`~wx.richtext.RichTextPrinting` class. Creating
applications with simple word processing features is simplified with
the inclusion of :class:`~wx.richtext.RichTextFormattingDialog`, a tabbed
dialog allowing interactive tailoring of paragraph and character
styling. Also provided is the multi-purpose dialog
:class:`~wx.richtext.RichTextStyleOrganiserDialog` that can be used for
managing style definitions, browsing styles and applying them, or
selecting list styles with a renumber option.

There are a few disadvantages to using
:class:`~wx.richtext.RichTextCtrl`. It is not native, so does not behave
exactly as a native :class:`wx.TextCtrl`, although common editing
conventions are followed. Users may miss the built-in spelling
correction on Mac OS X, or any special character input that may be
provided by the native control. It would also be a poor choice if
intended users rely on screen readers that would be not work well with
non-native text input implementation. You might mitigate this by
providing the choice between :class:`wx.TextCtrl` and
:class:`~wx.richtext.RichTextCtrl`, with fewer features in the former
case.

A good way to understand :class:`~wx.richtext.RichTextCtrl`\ 's
capabilities is to run the sample in the wxPython demo, and browse the
code.


Related Classes
===============

**Major classes:** :class:`~wx.richtext.RichTextCtrl`,
:class:`~wx.richtext.RichTextBuffer`, :class:`~wx.richtext.RichTextEvent`

**Helper classes:** :class:`wx.TextAttr`,
  :class:`~wx.richtext.RichTextRange`

**File handler classes:** :class:`~wx.richtext.RichTextFileHandler`,
:class:`~wx.richtext.RichTextHTMLHandler`,
:class:`~wx.richtext.RichTextXMLHandler`

**Style classes:**
:class:`~wx.richtext.RichTextCharacterStyleDefinition`,
:class:`~wx.richtext.RichTextParagraphStyleDefinition`,
:class:`~wx.richtext.RichTextListStyleDefinition`,
:class:`~wx.richtext.RichTextStyleSheet`

**Additional controls:** :class:`~wx.richtext.RichTextStyleComboCtrl`,
:class:`~wx.richtext.RichTextStyleListBox`,
:class:`~wx.richtext.RichTextStyleListCtrl`

**Printing classes:** :class:`~wx.richtext.RichTextPrinting`,
:class:`~wx.richtext.RichTextPrintout`,
:class:`~wx.richtext.RichTextHeaderFooterData`

**Dialog classes:** :class:`~wx.richtext.RichTextStyleOrganiserDialog`,
:class:`~wx.richtext.RichTextFormattingDialog`,
:class:`~wx.richtext.SymbolPickerDialog`


Code Example
============

This is taken from the wxPython demo::

    import wx
    import wx.richtext as rt
    import images

    #----------------------------------------------------------------------

    class RichTextFrame(wx.Frame):

        def __init__(self, *args, **kw):

            wx.Frame.__init__(self, *args, **kw)

            self.MakeMenuBar()
            self.MakeToolBar()
            self.CreateStatusBar()
            self.SetStatusText("Welcome to wx.richtext.RichTextCtrl!")

            self.rtc = rt.RichTextCtrl(self, style=wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER);
            wx.CallAfter(self.rtc.SetFocus)

            self.rtc.Freeze()
            self.rtc.BeginSuppressUndo()

            self.rtc.BeginParagraphSpacing(0, 20)

            self.rtc.BeginAlignment(rt.TEXT_ALIGNMENT_CENTRE)
            self.rtc.BeginBold()

            self.rtc.BeginFontSize(14)
            self.rtc.WriteText("Welcome to wxRichTextCtrl, a wxWidgets control for editing and presenting " \
                               "styled text and images")
            self.rtc.EndFontSize()
            self.rtc.Newline()

            self.rtc.BeginItalic()
            self.rtc.WriteText("by Julian Smart")
            self.rtc.EndItalic()

            self.rtc.EndBold()

            self.rtc.Newline()
            self.rtc.WriteImage(images._rt_zebra.GetImage())

            self.rtc.EndAlignment()

            self.rtc.Newline()
            self.rtc.Newline()

            self.rtc.WriteText("What can you do with this thing? ")
            self.rtc.WriteImage(images._rt_smiley.GetImage())
            self.rtc.WriteText(" Well, you can change text ")

            self.rtc.BeginTextColour((255, 0, 0))
            self.rtc.WriteText("colour, like this red bit.")
            self.rtc.EndTextColour()

            self.rtc.BeginTextColour((0, 0, 255))
            self.rtc.WriteText(" And this blue bit.")
            self.rtc.EndTextColour()

            self.rtc.WriteText(" Naturally you can make things ")
            self.rtc.BeginBold()
            self.rtc.WriteText("bold ")
            self.rtc.EndBold()
            self.rtc.BeginItalic()
            self.rtc.WriteText("or italic ")
            self.rtc.EndItalic()
            self.rtc.BeginUnderline()
            self.rtc.WriteText("or underlined.")
            self.rtc.EndUnderline()

            self.rtc.BeginFontSize(14)
            self.rtc.WriteText(" Different font sizes on the same line is allowed, too.")
            self.rtc.EndFontSize()

            self.rtc.WriteText(" Next we'll show an indented paragraph.")

            self.rtc.BeginLeftIndent(60)
            self.rtc.Newline()

            self.rtc.WriteText("It was in January, the most down-trodden month of an Edinburgh winter. " \
                               "An attractive woman came into the cafe, which is nothing remarkable.")
            self.rtc.EndLeftIndent()

            self.rtc.Newline()

            self.rtc.WriteText("Next, we'll show a first-line indent, achieved using BeginLeftIndent(100, -40).")

            self.rtc.BeginLeftIndent(100, -40)
            self.rtc.Newline()

            self.rtc.WriteText("It was in January, the most down-trodden month of an Edinburgh winter. " \
                               "An attractive woman came into the cafe, which is nothing remarkable.")
            self.rtc.EndLeftIndent()

            self.rtc.Newline()

            self.rtc.WriteText("Numbered bullets are possible, again using sub-indents:")

            self.rtc.BeginNumberedBullet(1, 100, 60)
            self.rtc.Newline()

            self.rtc.WriteText("This is my first item. Note that wxRichTextCtrl doesn't automatically do numbering, " \
                               "but this will be added later.")

            self.rtc.EndNumberedBullet()

            self.rtc.BeginNumberedBullet(2, 100, 60)
            self.rtc.Newline()

            self.rtc.WriteText("This is my second item.")
            self.rtc.EndNumberedBullet()

            self.rtc.Newline()

            self.rtc.WriteText("The following paragraph is right-indented:")

            self.rtc.BeginRightIndent(200)
            self.rtc.Newline()

            self.rtc.WriteText("It was in January, the most down-trodden month of an Edinburgh winter. " \
                               "An attractive woman came into the cafe, which is nothing remarkable.")
            self.rtc.EndRightIndent()

            self.rtc.Newline()

            self.rtc.WriteText("The following paragraph is right-aligned with 1.5 line spacing:")

            self.rtc.BeginAlignment(rt.TEXT_ALIGNMENT_RIGHT)
            self.rtc.BeginLineSpacing(rt.TEXT_ATTR_LINE_SPACING_HALF)
            self.rtc.Newline()

            self.rtc.WriteText("It was in January, the most down-trodden month of an Edinburgh winter. " \
                               "An attractive woman came into the cafe, which is nothing remarkable.")
            self.rtc.EndLineSpacing()
            self.rtc.EndAlignment()

            self.rtc.Newline()
            self.rtc.WriteText("Other notable features of wxRichTextCtrl include:")

            self.rtc.BeginSymbolBullet('*', 100, 60)
            self.rtc.Newline()
            self.rtc.WriteText("Compatibility with wxTextCtrl API")
            self.rtc.EndSymbolBullet()

            self.rtc.BeginSymbolBullet('*', 100, 60)
            self.rtc.Newline()
            self.rtc.WriteText("Easy stack-based BeginXXX()...EndXXX() style setting in addition to SetStyle()")
            self.rtc.EndSymbolBullet()

            self.rtc.BeginSymbolBullet('*', 100, 60)
            self.rtc.Newline()
            self.rtc.WriteText("XML loading and saving")
            self.rtc.EndSymbolBullet()

            self.rtc.BeginSymbolBullet('*', 100, 60)
            self.rtc.Newline()
            self.rtc.WriteText("Undo/Redo, with batching option and Undo suppressing")
            self.rtc.EndSymbolBullet()

            self.rtc.BeginSymbolBullet('*', 100, 60)
            self.rtc.Newline()
            self.rtc.WriteText("Clipboard copy and paste")
            self.rtc.EndSymbolBullet()

            self.rtc.BeginSymbolBullet('*', 100, 60)
            self.rtc.Newline()
            self.rtc.WriteText("wxRichTextStyleSheet with named character and paragraph styles, and control for " \
                               "applying named styles")
            self.rtc.EndSymbolBullet()

            self.rtc.BeginSymbolBullet('*', 100, 60)
            self.rtc.Newline()
            self.rtc.WriteText("A design that can easily be extended to other content types, ultimately with text " \
                               "boxes, tables, controls, and so on")
            self.rtc.EndSymbolBullet()

            self.rtc.BeginSymbolBullet('*', 100, 60)
            self.rtc.Newline()

            # Make a style suitable for showing a URL
            urlStyle = rt.TextAttrEx()
            urlStyle.SetTextColour(wx.BLUE)
            urlStyle.SetFontUnderlined(True)

            self.rtc.WriteText("RichTextCtrl can also display URLs, such as this one: ")
            self.rtc.BeginStyle(urlStyle)
            self.rtc.BeginURL("http://wxPython.org/")
            self.rtc.WriteText("The wxPython Web Site")
            self.rtc.EndURL();
            self.rtc.EndStyle();
            self.rtc.WriteText(". Click on the URL to generate an event.")

            self.rtc.Bind(wx.EVT_TEXT_URL, self.OnURL)

            self.rtc.Newline()
            self.rtc.WriteText("Note: this sample content was generated programmatically from within the " \
                               "MyFrame constructor " \
                               "in the demo. The images were loaded from inline XPMs. Enjoy wxRichTextCtrl!")

            self.rtc.EndParagraphSpacing()

            self.rtc.EndSuppressUndo()
            self.rtc.Thaw()


        def OnURL(self, evt):

            wx.MessageBox(evt.GetString(), "URL Clicked")


        def OnFileOpen(self, evt):

            # This gives us a string suitable for the file dialog based on
            # the file handlers that are loaded
            wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=False)
            dlg = wx.FileDialog(self, "Choose a filename",
                                wildcard=wildcard,
                                style=wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if path:
                    fileType = types[dlg.GetFilterIndex()]
                    self.rtc.LoadFile(path, fileType)
            dlg.Destroy()


        def OnFileSave(self, evt):

            if not self.rtc.GetFilename():
                self.OnFileSaveAs(evt)
                return

            self.rtc.SaveFile()


        def OnFileSaveAs(self, evt):

            wildcard, types = rt.RichTextBuffer.GetExtWildcard(save=True)

            dlg = wx.FileDialog(self, "Choose a filename",
                                wildcard=wildcard,
                                style=wx.SAVE)

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if path:
                    fileType = types[dlg.GetFilterIndex()]
                    ext = rt.RichTextBuffer.FindHandlerByType(fileType).GetExtension()
                    if not path.endswith(ext):
                        path += '.' + ext
                    self.rtc.SaveFile(path, fileType)

            dlg.Destroy()


        def OnFileViewHTML(self, evt):

            # Get an instance of the html file handler, use it to save the
            # document to a StringIO stream, and then display the
            # resulting html text in a dialog with a HtmlWindow.
            handler = rt.RichTextHTMLHandler()
            handler.SetFlags(rt.RICHTEXT_HANDLER_SAVE_IMAGES_TO_MEMORY)
            handler.SetFontSizeMapping([7,9,11,12,14,22,100])

            import cStringIO
            stream = cStringIO.StringIO()
            if not handler.SaveStream(self.rtc.GetBuffer(), stream):
                return

            import wx.html
            dlg = wx.Dialog(self, title="HTML", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
            html = wx.html.HtmlWindow(dlg, size=(500,400), style=wx.BORDER_SUNKEN)
            html.SetPage(stream.getvalue())
            btn = wx.Button(dlg, wx.ID_CANCEL)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(html, 1, wx.ALL|wx.EXPAND, 5)
            sizer.Add(btn, 0, wx.ALL|wx.CENTER, 10)
            dlg.SetSizer(sizer)
            sizer.Fit(dlg)

            dlg.ShowModal()

            handler.DeleteTemporaryImages()


        def OnFileExit(self, evt):

            self.Close(True)


        def OnBold(self, evt):

            self.rtc.ApplyBoldToSelection()


        def OnItalic(self, evt):

            self.rtc.ApplyItalicToSelection()


        def OnUnderline(self, evt):

            self.rtc.ApplyUnderlineToSelection()


        def OnAlignLeft(self, evt):

            self.rtc.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_LEFT)


        def OnAlignRight(self, evt):

            self.rtc.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_RIGHT)


        def OnAlignCenter(self, evt):

            self.rtc.ApplyAlignmentToSelection(rt.TEXT_ALIGNMENT_CENTRE)


        def OnIndentMore(self, evt):

            attr = rt.TextAttrEx()
            attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
            ip = self.rtc.GetInsertionPoint()
            if self.rtc.GetStyle(ip, attr):
                r = rt.RichTextRange(ip, ip)
                if self.rtc.HasSelection():
                    r = self.rtc.GetSelectionRange()

                attr.SetLeftIndent(attr.GetLeftIndent() + 100)
                attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
                self.rtc.SetStyle(r, attr)


        def OnIndentLess(self, evt):

            attr = rt.TextAttrEx()
            attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
            ip = self.rtc.GetInsertionPoint()
            if self.rtc.GetStyle(ip, attr):
                r = rt.RichTextRange(ip, ip)
                if self.rtc.HasSelection():
                    r = self.rtc.GetSelectionRange()

            if attr.GetLeftIndent() >= 100:
                attr.SetLeftIndent(attr.GetLeftIndent() - 100)
                attr.SetFlags(rt.TEXT_ATTR_LEFT_INDENT)
                self.rtc.SetStyle(r, attr)


        def OnParagraphSpacingMore(self, evt):

            attr = rt.TextAttrEx()
            attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
            ip = self.rtc.GetInsertionPoint()
            if self.rtc.GetStyle(ip, attr):
                r = rt.RichTextRange(ip, ip)
                if self.rtc.HasSelection():
                    r = self.rtc.GetSelectionRange()

                attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() + 20);
                attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
                self.rtc.SetStyle(r, attr)


        def OnParagraphSpacingLess(self, evt):

            attr = rt.TextAttrEx()
            attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
            ip = self.rtc.GetInsertionPoint()
            if self.rtc.GetStyle(ip, attr):
                r = rt.RichTextRange(ip, ip)
                if self.rtc.HasSelection():
                    r = self.rtc.GetSelectionRange()

                if attr.GetParagraphSpacingAfter() >= 20:
                    attr.SetParagraphSpacingAfter(attr.GetParagraphSpacingAfter() - 20);
                    attr.SetFlags(rt.TEXT_ATTR_PARA_SPACING_AFTER)
                    self.rtc.SetStyle(r, attr)


        def OnLineSpacingSingle(self, evt):

            attr = rt.TextAttrEx()
            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            ip = self.rtc.GetInsertionPoint()
            if self.rtc.GetStyle(ip, attr):
                r = rt.RichTextRange(ip, ip)
                if self.rtc.HasSelection():
                    r = self.rtc.GetSelectionRange()

                attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
                attr.SetLineSpacing(10)
                self.rtc.SetStyle(r, attr)


        def OnLineSpacingHalf(self, evt):

            attr = rt.TextAttrEx()
            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            ip = self.rtc.GetInsertionPoint()
            if self.rtc.GetStyle(ip, attr):
                r = rt.RichTextRange(ip, ip)
                if self.rtc.HasSelection():
                    r = self.rtc.GetSelectionRange()

                attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
                attr.SetLineSpacing(15)
                self.rtc.SetStyle(r, attr)


        def OnLineSpacingDouble(self, evt):

            attr = rt.TextAttrEx()
            attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
            ip = self.rtc.GetInsertionPoint()
            if self.rtc.GetStyle(ip, attr):
                r = rt.RichTextRange(ip, ip)
                if self.rtc.HasSelection():
                    r = self.rtc.GetSelectionRange()

                attr.SetFlags(rt.TEXT_ATTR_LINE_SPACING)
                attr.SetLineSpacing(20)
                self.rtc.SetStyle(r, attr)


        def OnFont(self, evt):

            if not self.rtc.HasSelection():
                return

            r = self.rtc.GetSelectionRange()
            fontData = wx.FontData()
            fontData.EnableEffects(False)
            attr = rt.TextAttrEx()
            attr.SetFlags(rt.TEXT_ATTR_FONT)
            if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
                fontData.SetInitialFont(attr.GetFont())

            dlg = wx.FontDialog(self, fontData)
            if dlg.ShowModal() == wx.ID_OK:
                fontData = dlg.GetFontData()
                font = fontData.GetChosenFont()
                if font:
                    attr.SetFlags(rt.TEXT_ATTR_FONT)
                    attr.SetFont(font)
                    self.rtc.SetStyle(r, attr)
            dlg.Destroy()


        def OnColour(self, evt):

            colourData = wx.ColourData()
            attr = rt.TextAttrEx()
            attr.SetFlags(rt.TEXT_ATTR_TEXT_COLOUR)
            if self.rtc.GetStyle(self.rtc.GetInsertionPoint(), attr):
                colourData.SetColour(attr.GetTextColour())

            dlg = wx.ColourDialog(self, colourData)
            if dlg.ShowModal() == wx.ID_OK:
                colourData = dlg.GetColourData()
                colour = colourData.GetColour()
                if colour:
                    if not self.rtc.HasSelection():
                        self.rtc.BeginTextColour(colour)
                    else:
                        r = self.rtc.GetSelectionRange()
                        attr.SetFlags(rt.TEXT_ATTR_TEXT_COLOUR)
                        attr.SetTextColour(colour)
                        self.rtc.SetStyle(r, attr)
            dlg.Destroy()



        def OnUpdateBold(self, evt):

            evt.Check(self.rtc.IsSelectionBold())


        def OnUpdateItalic(self, evt):

            evt.Check(self.rtc.IsSelectionItalics())


        def OnUpdateUnderline(self, evt):

            evt.Check(self.rtc.IsSelectionUnderlined())


        def OnUpdateAlignLeft(self, evt):

            evt.Check(self.rtc.IsSelectionAligned(rt.TEXT_ALIGNMENT_LEFT))


        def OnUpdateAlignCenter(self, evt):

            evt.Check(self.rtc.IsSelectionAligned(rt.TEXT_ALIGNMENT_CENTRE))


        def OnUpdateAlignRight(self, evt):

            evt.Check(self.rtc.IsSelectionAligned(rt.TEXT_ALIGNMENT_RIGHT))


        def ForwardEvent(self, evt):

            # The RichTextCtrl can handle menu and update events for undo,
            # redo, cut, copy, paste, delete, and select all, so just
            # forward the event to it.
            self.rtc.ProcessEvent(evt)


        def MakeMenuBar(self):

            def doBind(item, handler, updateUI=None):

                self.Bind(wx.EVT_MENU, handler, item)
                if updateUI is not None:
                    self.Bind(wx.EVT_UPDATE_UI, updateUI, item)

            fileMenu = wx.Menu()
            doBind( fileMenu.Append(-1, "&Open\tCtrl+O", "Open a file"),
                    self.OnFileOpen )
            doBind( fileMenu.Append(-1, "&Save\tCtrl+S", "Save a file"),
                    self.OnFileSave )
            doBind( fileMenu.Append(-1, "&Save As...\tF12", "Save to a new file"),
                    self.OnFileSaveAs )
            fileMenu.AppendSeparator()
            doBind( fileMenu.Append(-1, "&View as HTML", "View HTML"),
                    self.OnFileViewHTML)
            fileMenu.AppendSeparator()
            doBind( fileMenu.Append(-1, "E&xit\tCtrl+Q", "Quit this program"),
                    self.OnFileExit )

            editMenu = wx.Menu()
            doBind( editMenu.Append(wx.ID_UNDO, "&Undo\tCtrl+Z"),
                    self.ForwardEvent, self.ForwardEvent)
            doBind( editMenu.Append(wx.ID_REDO, "&Redo\tCtrl+Y"),
                    self.ForwardEvent, self.ForwardEvent )
            editMenu.AppendSeparator()
            doBind( editMenu.Append(wx.ID_CUT, "Cu&t\tCtrl+X"),
                    self.ForwardEvent, self.ForwardEvent )
            doBind( editMenu.Append(wx.ID_COPY, "&Copy\tCtrl+C"),
                    self.ForwardEvent, self.ForwardEvent)
            doBind( editMenu.Append(wx.ID_PASTE, "&Paste\tCtrl+V"),
                    self.ForwardEvent, self.ForwardEvent)
            doBind( editMenu.Append(wx.ID_CLEAR, "&Delete\tDel"),
                    self.ForwardEvent, self.ForwardEvent)
            editMenu.AppendSeparator()
            doBind( editMenu.Append(wx.ID_SELECTALL, "Select A&ll\tCtrl+A"),
                    self.ForwardEvent, self.ForwardEvent )

            formatMenu = wx.Menu()
            doBind( formatMenu.AppendCheckItem(-1, "&Bold\tCtrl+B"),
                    self.OnBold, self.OnUpdateBold)
            doBind( formatMenu.AppendCheckItem(-1, "&Italic\tCtrl+I"),
                    self.OnItalic, self.OnUpdateItalic)
            doBind( formatMenu.AppendCheckItem(-1, "&Underline\tCtrl+U"),
                    self.OnUnderline, self.OnUpdateUnderline)
            formatMenu.AppendSeparator()
            doBind( formatMenu.AppendCheckItem(-1, "L&eft Align"),
                    self.OnAlignLeft, self.OnUpdateAlignLeft)
            doBind( formatMenu.AppendCheckItem(-1, "&Centre"),
                    self.OnAlignCenter, self.OnUpdateAlignCenter)
            doBind( formatMenu.AppendCheckItem(-1, "&Right Align"),
                    self.OnAlignRight, self.OnUpdateAlignRight)
            formatMenu.AppendSeparator()
            doBind( formatMenu.Append(-1, "Indent &More"), self.OnIndentMore)
            doBind( formatMenu.Append(-1, "Indent &Less"), self.OnIndentLess)
            formatMenu.AppendSeparator()
            doBind( formatMenu.Append(-1, "Increase Paragraph &Spacing"), self.OnParagraphSpacingMore)
            doBind( formatMenu.Append(-1, "Decrease &Paragraph Spacing"), self.OnParagraphSpacingLess)
            formatMenu.AppendSeparator()
            doBind( formatMenu.Append(-1, "Normal Line Spacing"), self.OnLineSpacingSingle)
            doBind( formatMenu.Append(-1, "1.5 Line Spacing"), self.OnLineSpacingHalf)
            doBind( formatMenu.Append(-1, "Double Line Spacing"), self.OnLineSpacingDouble)
            formatMenu.AppendSeparator()
            doBind( formatMenu.Append(-1, "&Font..."), self.OnFont)

            mb = wx.MenuBar()
            mb.Append(fileMenu, "&File")
            mb.Append(editMenu, "&Edit")
            mb.Append(formatMenu, "F&ormat")
            self.SetMenuBar(mb)


        def MakeToolBar(self):

            def doBind(item, handler, updateUI=None):

                self.Bind(wx.EVT_TOOL, handler, item)
                if updateUI is not None:
                    self.Bind(wx.EVT_UPDATE_UI, updateUI, item)

            tbar = self.CreateToolBar()
            doBind( tbar.AddTool(-1, images._rt_open.GetBitmap(),
                                shortHelpString="Open"), self.OnFileOpen)
            doBind( tbar.AddTool(-1, images._rt_save.GetBitmap(),
                                shortHelpString="Save"), self.OnFileSave)
            tbar.AddSeparator()
            doBind( tbar.AddTool(wx.ID_CUT, images._rt_cut.GetBitmap(),
                                shortHelpString="Cut"), self.ForwardEvent, self.ForwardEvent)
            doBind( tbar.AddTool(wx.ID_COPY, images._rt_copy.GetBitmap(),
                                shortHelpString="Copy"), self.ForwardEvent, self.ForwardEvent)
            doBind( tbar.AddTool(wx.ID_PASTE, images._rt_paste.GetBitmap(),
                                shortHelpString="Paste"), self.ForwardEvent, self.ForwardEvent)
            tbar.AddSeparator()
            doBind( tbar.AddTool(wx.ID_UNDO, images._rt_undo.GetBitmap(),
                                shortHelpString="Undo"), self.ForwardEvent, self.ForwardEvent)
            doBind( tbar.AddTool(wx.ID_REDO, images._rt_redo.GetBitmap(),
                                shortHelpString="Redo"), self.ForwardEvent, self.ForwardEvent)
            tbar.AddSeparator()
            doBind( tbar.AddTool(-1, images._rt_bold.GetBitmap(), isToggle=True,
                                shortHelpString="Bold"), self.OnBold, self.OnUpdateBold)
            doBind( tbar.AddTool(-1, images._rt_italic.GetBitmap(), isToggle=True,
                                shortHelpString="Italic"), self.OnItalic, self.OnUpdateItalic)
            doBind( tbar.AddTool(-1, images._rt_underline.GetBitmap(), isToggle=True,
                                shortHelpString="Underline"), self.OnUnderline, self.OnUpdateUnderline)
            tbar.AddSeparator()
            doBind( tbar.AddTool(-1, images._rt_alignleft.GetBitmap(), isToggle=True,
                                shortHelpString="Align Left"), self.OnAlignLeft, self.OnUpdateAlignLeft)
            doBind( tbar.AddTool(-1, images._rt_centre.GetBitmap(), isToggle=True,
                                shortHelpString="Center"), self.OnAlignCenter, self.OnUpdateAlignCenter)
            doBind( tbar.AddTool(-1, images._rt_alignright.GetBitmap(), isToggle=True,
                                shortHelpString="Align Right"), self.OnAlignRight, self.OnUpdateAlignRight)
            tbar.AddSeparator()
            doBind( tbar.AddTool(-1, images._rt_indentless.GetBitmap(),
                                shortHelpString="Indent Less"), self.OnIndentLess)
            doBind( tbar.AddTool(-1, images._rt_indentmore.GetBitmap(),
                                shortHelpString="Indent More"), self.OnIndentMore)
            tbar.AddSeparator()
            doBind( tbar.AddTool(-1, images._rt_font.GetBitmap(),
                                shortHelpString="Font"), self.OnFont)
            doBind( tbar.AddTool(-1, images._rt_colour.GetBitmap(),
                                shortHelpString="Font Colour"), self.OnColour)

            tbar.Realize()


    #----------------------------------------------------------------------

    class TestPanel(wx.Panel):

        def __init__(self, parent):

            wx.Panel.__init__(self, parent, -1)

            b = wx.Button(self, -1, "Show the RichTextCtrl sample", (50,50))
            self.Bind(wx.EVT_BUTTON, self.OnButton, b)

            self.AddRTCHandlers()


        def AddRTCHandlers(self):

            # make sure we haven't already added them.
            if rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) is not None:
                return

            # This would normally go in your app's OnInit method.  I'm
            # not sure why these file handlers are not loaded by
            # default by the C++ richtext code, I guess it's so you
            # can change the name or extension if you wanted...
            rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
            rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

            # ...like this
            rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler(name="Other XML",
                                                               ext="ox",
                                                               type=99))

            # This is needed for the view as HTML option since we tell it
            # to store the images in the memory file system.
            wx.FileSystem.AddHandler(wx.MemoryFSHandler())


        def OnButton(self, evt):

            win = RichTextFrame(self, -1, "wx.richtext.RichTextCtrl",
                                size=(700, 500),
                                style = wx.DEFAULT_FRAME_STYLE)
            win.Show(True)

            # give easy access to the demo's PyShell if it's running
            self.rtfrm = win
            self.rtc = win.rtc


    app = wx.App(0)

    frame = wx.Frame(None)
    panel = TestPanel(frame)
    frame.Show()

    app.MainLoop()



Text Styles
===========

Styling attributes are represented by :class:`wx.TextAttr`, or for more
control over attributes such as margins and size, the derived class
:class:`~wx.richtext.RichTextAttr`.

When setting a style, the flags of the attribute object determine
which attributes are applied. When querying a style, the passed flags
are ignored except (optionally) to determine whether attributes should
be retrieved from character content or from the paragraph object.

:class:`~wx.richtext.RichTextCtrl` takes a layered approach to styles, so that
different parts of the content may be responsible for contributing
different attributes to the final style you see on the screen.

There are four main notions of style within a control:


+ **Basic style**: The fundamental style of a control, onto which any
  other styles are layered. It provides default attributes, and
  changing the basic style may immediately change the look of the
  content depending on what other styles the content uses. Calling
  :meth:`~wx.richtext.RichTextCtrl.SetFont` changes the font for the
  basic style. The basic style is set with
  :meth:`~wx.richtext.RichTextCtrl.SetBasicStyle`.

+ **Paragraph style**: Each paragraph has attributes that are set
  independently from other paragraphs and independently from the
  content within the paragraph. Normally, these attributes are
  paragraph- related, such as alignment and indentation, but it is
  possible to set character attributes too. The paragraph style can be
  set independently of its content by passing
  ``RICHTEXT_SETSTYLE_PARAGRAPHS_ONLY`` to
  :meth:`~wx.richtext.RichTextCtrl.SetStyleEx`.

+ **Character style**: Characters within each paragraph can have
  attributes. A single character, or a run of characters, can have a
  particular set of attributes. The character style can be with
  :meth:`~wx.richtext.RichTextCtrl.SetStyle` or
  :meth:`~wx.richtext.RichTextCtrl.SetStyleEx`.

+ **Default style**: This is the 'current' style that determines the
  style of content that is subsequently typed, pasted or
  programmatically inserted. The default style is set with
  :meth:`~wx.richtext.RichTextCtrl.SetDefaultStyle`.


What you see on the screen is the dynamically *combined* style, found
by merging the first three of the above style types (the fourth is
only a guide for future content insertion and therefore does not
affect the currently displayed content).

To make all this more concrete, here are examples of where you might
set these different styles:


+ You might set the *basic style* to have a Times Roman font in 12
  point, left-aligned, with two millimetres of spacing after each
  paragraph.

+ You might set the *paragraph style* (for one particular paragraph)
  to be centred.

+ You might set the *character style* of one particular word to bold.

+ You might set the *default style* to be underlined, for subsequent
  inserted text.


Naturally you can do any of these things either using your own UI, or
programmatically.

The basic :class:`wx.TextCtrl` doesn't make the same distinctions as
:class:`~wx.richtext.RichTextCtrl` regarding attribute storage. So we need finer
control when setting and retrieving attributes.
:meth:`~wx.richtext.RichTextCtrl.SetStyleEx` takes a *flags* parameter:


+ ``RICHTEXT_SETSTYLE_OPTIMIZE`` specifies that the style should be
  changed only if the combined attributes are different from the
  attributes for the current object. This is important when applying
  styling that has been edited by the user, because he has just edited
  the *combined* (visible) style, and :class:`~wx.richtext.RichTextCtrl` wants to leave
  unchanged attributes associated with their original objects instead of
  applying them to both paragraph and content objects.
+ ``RICHTEXT_SETSTYLE_PARAGRAPHS_ONLY`` specifies that only paragraph
  objects within the given range should take on the attributes.
+ ``RICHTEXT_SETSTYLE_CHARACTERS_ONLY`` specifies that only content
  objects (text or images) within the given range should take on the
  attributes.
+ ``RICHTEXT_SETSTYLE_WITH_UNDO`` specifies that the operation should be
  undoable.


It's great to be able to change arbitrary attributes in a
:class:`~wx.richtext.RichTextCtrl`, but it can be unwieldy for the
user or programmer to set attributes separately. Word processors have
collections of styles that you can tailor or use as-is, and this means
that you can set a heading with one click instead of marking text in
bold, specifying a large font size, and applying a certain paragraph
spacing and alignment for every such heading. Similarly, wxPython
provides a class called :class:`~wx.richtext.RichTextStyleSheet` which
manages style definitions
(:class:`~wx.richtext.RichTextParagraphStyleDefinition`,
:class:`~wx.richtext.RichTextListStyleDefinition` and
:class:`~wx.richtext.RichTextCharacterStyleDefinition`). Once you have
added definitions to a style sheet and associated it with a
:class:`~wx.richtext.RichTextCtrl`, you can apply a named definition
to a range of text. The classes
:class:`~wx.richtext.RichTextStyleComboCtrl` and
:class:`~wx.richtext.RichTextStyleListBox` can be used to present the
user with a list of styles in a sheet, and apply them to the selected
text.

You can reapply a style sheet to the contents of the control, by
calling :meth:`~wx.richtext.RichTextCtrl.ApplyStyleSheet`. This is
useful if the style definitions have changed, and you want the content
to reflect this. It relies on the fact that when you apply a named
style, the style definition name is recorded in the content. So
ApplyStyleSheet works by finding the paragraph attributes with style
names and re- applying the definition's attributes to the
paragraph. Currently, this works with paragraph and list style
definitions only.


Included Dialogs
================

:class:`~wx.richtext.RichTextCtrl` comes with standard dialogs to make
it easier to implement text editing functionality.

:class:`~wx.richtext.RichTextFormattingDialog` can be used for
character or paragraph formatting, or a combination of both. It's a
`PropertySheetDialog` with the following available tabs: Font, Indents
& Spacing, Tabs, Bullets, Style, Borders, Margins, Background, Size,
and List Style.  You can select which pages will be shown by supplying
flags to the dialog constructor. In a character formatting dialog,
typically only the Font page will be shown. In a paragraph formatting
dialog, you'll show the Indents & Spacing, Tabs and Bullets pages. The
Style tab is useful when editing a style definition.

You can customize this dialog by providing your own
:class:`~wx.richtext.RichTextFormattingDialogFactory` object, which
tells the formatting dialog how many pages are supported, what their
identifiers are, and how to creates the pages.

:class:`~wx.richtext.RichTextStyleOrganiserDialog` is a multi-purpose
dialog that can be used for managing style definitions, browsing
styles and applying them, or selecting list styles with a renumber
option. See the sample for usage - it is used for the "Manage Styles"
and "Bullets and Numbering" menu commands.

:class:`~wx.richtext.SymbolPickerDialog` lets the user insert a symbol
from a specified font. It has no :class:`~wx.richtext.RichTextCtrl`
dependencies besides being included in the rich text library.


How RichTextCtrl is Implemented
===============================

Data representation is handled by
:class:`~wx.richtext.RichTextBuffer`, and a
:class:`~wx.richtext.RichTextCtrl` always has one such buffer.

The content is represented by a hierarchy of objects, all derived from
:class:`~wx.richtext.RichTextObject`. An object might be an image, a
fragment of text, a paragraph, or a further composite object. Objects
store a :class:`~wx.richtext.RichTextAttr` containing style
information; a paragraph object can contain both paragraph and
character information, but content objects such as text can only store
character information. The final style displayed in the control or in
a printout is a combination of base style, paragraph style and content
(character) style.

The top of the hierarchy is the buffer, a kind of
:class:`~wx.richtext.RichTextParagraphLayoutBox`, containing further
:class:`~wx.richtext.RichTextParagraph` objects, each of which can
include text, images and potentially other types of object.

Each object maintains a range (start and end position) measured from
the start of the main parent object.

When Layout is called on an object, it is given a size which the
object must limit itself to, or one or more flexible directions
(vertical or horizontal). So, for example, a centred paragraph is
given the page width to play with (minus any margins), but can extend
indefinitely in the vertical direction. The implementation of Layout
caches the calculated size and position.

When the buffer is modified, a range is invalidated (marked as
requiring layout), so that only the minimum amount of layout is
performed.

A paragraph of pure text with the same style contains just one further
object, a :class:`~wx.richtext.RichTextPlainText` object. When styling
is applied to part of this object, the object is decomposed into
separate objects, one object for each different character style. So
each object within a paragraph always has just one :class:`wx.TextAttr`
object to denote its character style. Of course, this can lead to
fragmentation after a lot of edit operations, potentially leading to
several objects with the same style where just one would do. So a
Defragment function is called when updating the control's display, to
ensure that the minimum number of objects is used.


Nested Objects
==============

:class:`~wx.richtext.RichTextCtrl` supports nested objects such as
text boxes and tables. To achieve compatibility with the existing API,
there is the concept of *object* *focus*. When the user clicks on a
nested text box, the object focus is set to that container object so
all keyboard input and API functions apply to that container. The
application can change the focus using
:meth:`~wx.richtext.RichTextCtrl.SetObjectFocus`. Call this function
with a ``None`` parameter to set the focus back to the top-level
object.

An event will be sent to the control when the focus changes.

When the user clicks on the control,
:class:`~wx.richtext.RichTextCtrl` determines which container to set
as the current object focus by calling the found container's overridden
:meth:`~wx.richtext.RichTextObject.AcceptsFocus` function. For
example, although a table is a container, it must not itself be the
object focus because there is no text editing at the table
level. Instead, a cell within the table must accept the focus.

Since with nested objects it is not possible to represent a section
with merely a start position and an end position, the class
:class:`~wx.richtext.RichTextSelection` is provided which stores
multiple ranges (for non-contiguous selections such as table cells)
and a pointer to the container object in question. You can pass
:class:`~wx.richtext.RichTextSelection` to
:meth:`~wx.richtext.RichTextCtrl.SetSelection` or get an instance of
it from :meth:`~wx.richtext.RichTextCtrl.GetSelection`.

When selecting multiple objects, such as cell tables, the
:class:`~wx.richtext.RichTextCtrl` dragging handler code calls the
function :meth:`~wx.richtext.RichTextObject.HandlesChildSelections` to
determine whether the children can be individual selections. Currently
only table cells can be multiply-selected in this way.


Context Menus and Property Dialogs
==================================

There are three ways you can make use of context menus: you can let
:class:`~wx.richtext.RichTextCtrl` handle everything and provide a basic
menu; you can set your own context menu using
:meth:`~wx.richtext.RichTextCtrl.SetContextMenu` but let
:class:`~wx.richtext.RichTextCtrl` handle showing it and adding property
items; or you can override the default context menu behaviour by
adding a context menu event handler to your class in the normal way.

If you right-click over a text box in cell in a table, you may want to
edit the properties of one of these objects - but which properties
will you be editing?

Well, the default behaviour allows up to three property-editing menu
items simultaneously - for the object clicked on, the container of
that object, and the container's parent (depending on whether any of
these objects return true from their
:meth:`~wx.richtext.RichTextObject.CanEditProperties` functions). If
you supply a context menu, add a property command item using the
``ID_RICHTEXT_PROPERTIES1`` identifier, so that
:class:`~wx.richtext.RichTextCtrl` can find the position to add
command items. The object should tell the control what label to use by
returning a string from
:meth:`~wx.richtext.RichTextObject.GetPropertiesMenuLabel`.

Since there may be several property-editing commands showing, it is
recommended that you don't include the word Properties - just the name
of the object, such as Text Box or Table.


Development Roadmap
===================


Bugs
----

This is an incomplete list of bugs.


+ Moving the caret up at the beginning of a line sometimes incorrectly
  positions the caret.
+ As the selection is expanded, the text jumps slightly due to kerning
  differences between drawing a single text string versus drawing
  several fragments separately. This could be improved by using
  :meth:`wx.DC.GetPartialTextExtents` to calculate exactly where the separate
  fragments should be drawn. Note that this problem also applies to
  separation of text fragments due to difference in their attributes.



Features
--------

This is a list of some of the features that have yet to be
implemented. Help with them will be appreciated.


+ Support for composite objects in some functions where it's not yet
  implemented, for example ApplyStyleSheet

+ Table API enhancements and dialogs; improved table layout especially
  row spans and fitting

+ Conversion from HTML, and a rewrite of the HTML output handler that
  includes CSS, tables, text boxes, and floating images, in addition to
  a simplified-HTML mode for wxHTML compatibility

+ Open Office input and output

+ RTF input and output

+ A ruler control

+ Standard editing toolbars

+ Bitmap bullets

+ Justified text, in print/preview at least

+ Scaling: either everything scaled, or rendering using a custom
  reference point size and an optional dimension scale


There are also things that could be done to take advantage of the
underlying text capabilities of the platform; higher-level text
formatting APIs are available on some platforms, such as Mac OS X, and
some of translation from high level to low level :class:`wx.DC` API is
unnecessary. However this would require additions to the wxPython API.


