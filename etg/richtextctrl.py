#---------------------------------------------------------------------------
# Name:        etg/richtextctrl.py
# Author:      Robin Dunn
#
# Created:     13-May-2013
# Copyright:   (c) 2013-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_richtext"
NAME      = "richtextctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "interface_2wx_2richtext_2richtextctrl_8h.xml",
           "wxRichTextContextMenuPropertiesInfo",
           "wxRichTextCtrl",
           "wxRichTextEvent",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.


    #-----------------------------------------------------------------
    # ignore some macros since most of this set are not simple numbers
    for item in module.items:
        if item.name.startswith('wxRICHTEXT_DEFAULT'):
            item.ignore()


    #-----------------------------------------------------------------
    c = module.find('wxRichTextContextMenuPropertiesInfo')
    assert isinstance(c, etgtools.ClassDef)
    tools.ignoreConstOverloads(c)



    #-----------------------------------------------------------------
    c = module.find('wxRichTextCtrl')
    tools.fixWindowClass(c)
    c.bases = ['wxControl']  # wxTextCtrlIface, wxScrollHelper are also bases...
    c.find('GetSelection').findOverload('from').ignore()
    tools.ignoreConstOverloads(c)

    c.find('PositionToXY.x').out = True
    c.find('PositionToXY.y').out = True

    c.find('HitTest.pos').out = True
    c.find('HitTest.col').out = True
    c.find('HitTest.row').out = True
    c.find('HitTest').renameOverload('row', 'HitTestXY')

    c.find('GetRange.from').name = 'from_'
    c.find('GetRange.to').name = 'to_'
    c.find('Remove.from').name = 'from_'
    c.find('Remove.to').name = 'to_'
    c.find('Replace.from').name = 'from_'
    c.find('Replace.to').name = 'to_'
    c.find('SetSelection.from').name = 'from_'
    c.find('SetSelection.to').name = 'to_'

    c.find('SetListStyle.def').name = 'styleDef'
    c.find('ApplyStyle.def').name = 'styleDef'

    tools.fixTextClipboardMethods(c)

    c.addPyMethod('GetDefaultStyle', '(self)', 'return self.GetDefaultStyleEx()',
                  deprecated='Use GetDefaultStyleEx instead')


    # Make sure that all the methods from wxTextEntry are included. This is
    # needed because we are pretending that this class only derives from
    # wxControl but the real C++ class also derives from wxTextCtrlIface
    # which derives from wxTextEntryBase.
    import textentry
    mod = textentry.parseAndTweakModule()
    klass = mod.find('wxTextEntry')
    items = [item for item in klass.items if isinstance(item, etgtools.MethodDef) and
                                             not item.isCtor and
                                             not item.isDtor and
                                             not c.findItem(item.name)]
    c.items.extend(items)

    # TODO: What about the wxScrollHelper base class


    #-----------------------------------------------------------------
    c = module.find('wxRichTextEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_RICHTEXT_LEFT_CLICK = wx.PyEventBinder(wxEVT_RICHTEXT_LEFT_CLICK)
        EVT_RICHTEXT_RIGHT_CLICK = wx.PyEventBinder(wxEVT_RICHTEXT_RIGHT_CLICK)
        EVT_RICHTEXT_MIDDLE_CLICK = wx.PyEventBinder(wxEVT_RICHTEXT_MIDDLE_CLICK)
        EVT_RICHTEXT_LEFT_DCLICK = wx.PyEventBinder(wxEVT_RICHTEXT_LEFT_DCLICK)
        EVT_RICHTEXT_RETURN = wx.PyEventBinder(wxEVT_RICHTEXT_RETURN)
        EVT_RICHTEXT_CHARACTER = wx.PyEventBinder(wxEVT_RICHTEXT_CHARACTER)
        EVT_RICHTEXT_DELETE = wx.PyEventBinder(wxEVT_RICHTEXT_DELETE)

        EVT_RICHTEXT_STYLESHEET_CHANGING = wx.PyEventBinder(wxEVT_RICHTEXT_STYLESHEET_CHANGING)
        EVT_RICHTEXT_STYLESHEET_CHANGED = wx.PyEventBinder(wxEVT_RICHTEXT_STYLESHEET_CHANGED)
        EVT_RICHTEXT_STYLESHEET_REPLACING = wx.PyEventBinder(wxEVT_RICHTEXT_STYLESHEET_REPLACING)
        EVT_RICHTEXT_STYLESHEET_REPLACED = wx.PyEventBinder(wxEVT_RICHTEXT_STYLESHEET_REPLACED)

        EVT_RICHTEXT_CONTENT_INSERTED = wx.PyEventBinder(wxEVT_RICHTEXT_CONTENT_INSERTED)
        EVT_RICHTEXT_CONTENT_DELETED = wx.PyEventBinder(wxEVT_RICHTEXT_CONTENT_DELETED)
        EVT_RICHTEXT_STYLE_CHANGED = wx.PyEventBinder(wxEVT_RICHTEXT_STYLE_CHANGED)
        EVT_RICHTEXT_STYLE_CHANGED = wx.PyEventBinder(wxEVT_RICHTEXT_PROPERTIES_CHANGED)
        EVT_RICHTEXT_SELECTION_CHANGED = wx.PyEventBinder(wxEVT_RICHTEXT_SELECTION_CHANGED)
        EVT_RICHTEXT_BUFFER_RESET = wx.PyEventBinder(wxEVT_RICHTEXT_BUFFER_RESET)
        EVT_RICHTEXT_FOCUS_OBJECT_CHANGED = wx.PyEventBinder(wxEVT_RICHTEXT_FOCUS_OBJECT_CHANGED)
        """);

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

