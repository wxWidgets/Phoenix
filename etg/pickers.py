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
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

