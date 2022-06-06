#---------------------------------------------------------------------------
# Name:        etg/pickers.py
# Author:      Robin Dunn
#
# Created:     10-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "pickers"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxPickerBase",
           "wxColourPickerCtrl",
           "wxColourPickerEvent",
           "wxFilePickerCtrl",
           "wxDirPickerCtrl",
           "wxFileDirPickerEvent",
           "wxFontPickerCtrl",
           "wxFontPickerEvent"
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxPickerBase')
    assert isinstance(c, etgtools.ClassDef)
    c.find('CreateBase.id').default = 'wxID_ANY'
    c.find('GetTextCtrlStyle').ignore(False)
    c.find('GetPickerStyle').ignore(False)
    c.find('PostCreation').ignore(False)

    #-----------------------------------------------------------------

    module.addHeaderCode('#include <wx/clrpicker.h>')

    c = module.find('wxColourPickerCtrl')
    tools.fixWindowClass(c)
    module.addGlobalStr('wxColourPickerWidgetNameStr', c)
    module.addGlobalStr('wxColourPickerCtrlNameStr', c)

    c.addItem(etgtools.WigCode("""\
        virtual void UpdatePickerFromTextCtrl();
        virtual void UpdateTextCtrlFromPicker();
        """))

    c = module.find('wxColourPickerEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_COLOURPICKER_CHANGED = wx.PyEventBinder( wxEVT_COLOURPICKER_CHANGED, 1 )
        EVT_COLOURPICKER_CURRENT_CHANGED = wx.PyEventBinder( wxEVT_COLOURPICKER_CURRENT_CHANGED, 1 )
        EVT_COLOURPICKER_DIALOG_CANCELLED = wx.PyEventBinder( wxEVT_COLOURPICKER_DIALOG_CANCELLED, 1 )

        # deprecated wxEVT alias
        wxEVT_COMMAND_COLOURPICKER_CHANGED  = wxEVT_COLOURPICKER_CHANGED
        """)


    #-----------------------------------------------------------------

    module.addHeaderCode('#include <wx/filepicker.h>')

    c = module.find('wxFilePickerCtrl')
    tools.fixWindowClass(c)
    module.addGlobalStr('wxFilePickerWidgetLabel', c)
    module.addGlobalStr('wxFilePickerWidgetNameStr', c)
    module.addGlobalStr('wxFilePickerCtrlNameStr', c)
    module.addGlobalStr('wxFileSelectorPromptStr', c)
    module.addGlobalStr('wxFileSelectorDefaultWildcardStr', c)

    c.addItem(etgtools.WigCode("""\
        virtual void UpdatePickerFromTextCtrl();
        virtual void UpdateTextCtrlFromPicker();
        """))

    # we'll use the [G|S]etPath methods instead so we don't have to mess with wxFileName
    c.find('GetFileName').ignore()
    c.find('SetFileName').ignore()

    c = module.find('wxDirPickerCtrl')
    tools.fixWindowClass(c)
    module.addGlobalStr('wxDirPickerWidgetLabel', c)
    module.addGlobalStr('wxDirPickerWidgetNameStr', c)
    module.addGlobalStr('wxDirPickerCtrlNameStr', c)
    module.addGlobalStr('wxDirSelectorPromptStr', c)

    c.addItem(etgtools.WigCode("""\
        virtual void UpdatePickerFromTextCtrl();
        virtual void UpdateTextCtrlFromPicker();
        """))

    # we'll use the [G|S]etPath methods instead so we don't have to mess with wxFileName
    c.find('GetDirName').ignore()
    c.find('SetDirName').ignore()

    c = module.find('wxFileDirPickerEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_FILEPICKER_CHANGED = wx.PyEventBinder( wxEVT_FILEPICKER_CHANGED, 1 )
        EVT_DIRPICKER_CHANGED = wx.PyEventBinder( wxEVT_DIRPICKER_CHANGED, 1 )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_FILEPICKER_CHANGED   = wxEVT_FILEPICKER_CHANGED
        wxEVT_COMMAND_DIRPICKER_CHANGED    = wxEVT_DIRPICKER_CHANGED
        """)

    #-----------------------------------------------------------------

    module.addHeaderCode('#include <wx/fontpicker.h>')

    c = module.find('wxFontPickerCtrl')
    tools.fixWindowClass(c)
    module.addGlobalStr('wxFontPickerWidgetNameStr', c)
    module.addGlobalStr('wxFontPickerCtrlNameStr', c)

    c.addItem(etgtools.WigCode("""\
        virtual void UpdatePickerFromTextCtrl();
        virtual void UpdateTextCtrlFromPicker();
        """))

    c = module.find('wxFontPickerEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_FONTPICKER_CHANGED = wx.PyEventBinder( wxEVT_FONTPICKER_CHANGED, 1 )

        # deprecated wxEVT alias
        wxEVT_COMMAND_FONTPICKER_CHANGED  = wxEVT_FONTPICKER_CHANGED
        """)

    #-----------------------------------------------------------------
    # The C++ wxColourPickerCtrl uses a wx.Button for the implementation,
    # but that looks and works very badly on Mac because the native
    # button can't change color.  So for the Mac we'll implement our own
    # picker using a wx.BitmapButton instead.
    module.addPyCode("""\
    if 'wxMac' in wx.PlatformInfo:
        class ColourPickerCtrl(PickerBase):
            '''
            This control allows the user to select a colour. The
            implementation varies by platform but is usually a button which
            brings up a `wx.ColourDialog` when clicked.


            Window Styles
            -------------

                ======================  ============================================
                wx.CLRP_DEFAULT         Default style.
                wx.CLRP_USE_TEXTCTRL    Creates a text control to the left of the
                                        picker button which is completely managed
                                        by the `wx.ColourPickerCtrl` and which can
                                        be used by the user to specify a colour.
                                        The text control is automatically synchronized
                                        with the button's value. Use functions defined in
                                        `wx.PickerBase` to modify the text control.
                wx.CLRP_SHOW_LABEL      Shows the colour in HTML form (AABBCC) as the
                                        colour button label (instead of no label at all).
                ======================  ============================================

            Events
            ------

                ========================  ==========================================
                EVT_COLOURPICKER_CHANGED  The user changed the colour selected in the
                                          control either using the button or using the
                                          text control (see wx.CLRP_USE_TEXTCTRL; note
                                          that in this case the event is fired only if
                                          the user's input is valid, i.e. recognizable).
                ========================  ==========================================
            '''

            # ColourData object to be shared by all colour pickers, so they can
            # share the custom colours
            _colourData = None

            #--------------------------------------------------
            class ColourPickerButton(BitmapButton):
                def __init__(self, parent, id=-1, colour=wx.BLACK,
                             pos=wx.DefaultPosition, size=wx.DefaultSize,
                             style = CLRP_DEFAULT_STYLE,
                             validator = wx.DefaultValidator,
                             name = "colourpickerwidget"):

                    wx.BitmapButton.__init__(self, parent, id, wx.Bitmap(1,1),
                                             pos, size, style, validator, name)
                    self.SetColour(colour)
                    self.InvalidateBestSize()
                    self.SetInitialSize(size)
                    self.Bind(wx.EVT_BUTTON, self.OnButtonClick)

                    if ColourPickerCtrl._colourData is None:
                        ColourPickerCtrl._colourData = wx.ColourData()
                        ColourPickerCtrl._colourData.SetChooseFull(True)
                        grey = 0
                        for i in range(16):
                            c = wx.Colour(grey, grey, grey)
                            ColourPickerCtrl._colourData.SetCustomColour(i, c)
                            grey += 16

                def SetColour(self, colour):
                    # force a copy, in case the _colorData is shared
                    self.colour = wx.Colour(colour)
                    bmp = self._makeBitmap()
                    self.SetBitmapLabel(wx.BitmapBundle(bmp))

                def GetColour(self):
                    return self.colour

                def OnButtonClick(self, evt):
                    ColourPickerCtrl._colourData.SetColour(self.colour)
                    dlg = wx.ColourDialog(self, ColourPickerCtrl._colourData)
                    if dlg.ShowModal() == wx.ID_OK:
                        ColourPickerCtrl._colourData = dlg.GetColourData()
                        self.SetColour(ColourPickerCtrl._colourData.GetColour())
                        evt = wx.ColourPickerEvent(self, self.GetId(), self.GetColour())
                        self.GetEventHandler().ProcessEvent(evt)

                def _makeBitmap(self):
                    width = height = 24
                    bg = self.GetColour()
                    if self.HasFlag(CLRP_SHOW_LABEL):
                        w, h = self.GetTextExtent(bg.GetAsString(wx.C2S_HTML_SYNTAX))
                        width += w
                    bmp = wx.Bitmap(width, height)
                    dc = wx.MemoryDC(bmp)
                    dc.SetBackground(wx.Brush(self.colour))
                    dc.Clear()
                    if self.HasFlag(CLRP_SHOW_LABEL):
                        from wx.lib.colourutils import BestLabelColour
                        fg = BestLabelColour(bg)
                        dc.SetTextForeground(fg)
                        dc.DrawText(bg.GetAsString(wx.C2S_HTML_SYNTAX),
                                    (width - w)/2, (height - h)/2)
                    return bmp

            #--------------------------------------------------

            def __init__(self, parent, id=-1, colour=wx.BLACK,
                         pos=wx.DefaultPosition, size=wx.DefaultSize,
                         style = CLRP_DEFAULT_STYLE,
                         validator = wx.DefaultValidator,
                         name = "colourpicker"):
                if type(colour) != wx.Colour:
                    colour = wx.Colour(colour)
                wx.PickerBase.__init__(self)
                self.CreateBase(parent, id, colour.GetAsString(),
                                pos, size, style, validator, name)
                widget = ColourPickerCtrl.ColourPickerButton(
                    self, -1, colour, style=self.GetPickerStyle(style))
                self.SetPickerCtrl(widget)
                widget.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnColourChange)
                self.PostCreation()


            def GetColour(self):
                '''Set the displayed colour.'''
                return self.GetPickerCtrl().GetColour()

            def SetColour(self, colour):
                '''Returns the currently selected colour.'''
                self.GetPickerCtrl().SetColour(colour)
                self.UpdateTextCtrlFromPicker()
            Colour = property(GetColour, SetColour)


            def UpdatePickerFromTextCtrl(self):
                col = wx.Colour(self.GetTextCtrl().GetValue())
                if not col.IsOk():
                    return
                if self.GetColour() != col:
                    self.GetPickerCtrl().SetColour(col)
                    evt = wx.ColourPickerEvent(self, self.GetId(), self.GetColour())
                    self.GetEventHandler().ProcessEvent(evt)

            def UpdateTextCtrlFromPicker(self):
                if not self.GetTextCtrl():
                    return
                self.GetTextCtrl().SetValue(self.GetColour().GetAsString())

            def GetPickerStyle(self, style):
                return style & CLRP_SHOW_LABEL

            def OnColourChange(self, evt):
                self.UpdateTextCtrlFromPicker()
                evt = wx.ColourPickerEvent(self, self.GetId(), self.GetColour())
                self.GetEventHandler().ProcessEvent(evt)
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

