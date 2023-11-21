#---------------------------------------------------------------------------
# Name:        etg/textctrl.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     9-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "textctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxTextAttr',
           'wxTextCtrl',
           'wxTextUrlEvent',
           ]

#---------------------------------------------------------------------------

def parseAndTweakModule():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxTextAttr')
    assert isinstance(c, etgtools.ClassDef)
    c.find('operator=').ignore()
    c.find('SetFont').pyArgsString = '(font, flags=TEXT_ATTR_FONT & ~TEXT_ATTR_FONT_PIXEL_SIZE)'
    c.find('SetFontUnderlined').renameOverload('wxTextAttrUnderlineType',
                                               'SetFontUnderlineType')


    c = module.find('wxTextCtrl')
    module.addGlobalStr('wxTextCtrlNameStr', c)

    # Split the HitTest overloads into separately named methods since once
    # the output parameters are applied they will have the same function
    # signature.
    ht1 = c.find('HitTest')
    ht2 = ht1.overloads[0]
    ht1.overloads = []
    c.insertItemAfter(ht1, ht2)
    ht1.pyName = 'HitTestPos'
    ht1.find('pos').out = True
    ht2.find('row').out = True
    ht2.find('col').out = True

    c.find('PositionToXY.x').out = True
    c.find('PositionToXY.y').out = True

    for op in c.findAll('operator<<'):
        op.ignore()

    c.find('OnDropFiles').ignore()

    tools.fixWindowClass(c)

    c.addCppMethod('void', 'MacCheckSpelling', '(bool check)',
        doc="""\
            Turn on the native spell checking for the text widget on
            OSX.  Ignored on other platforms.
            """,
        body="""\
            #ifdef __WXMAC__
                self->MacCheckSpelling(check);
            #endif
            """)

    c.addCppMethod('bool', 'ShowNativeCaret', '(bool show = true)',
        doc="""\
            Turn on the widget's native caret on Windows.
            Ignored on other platforms.
            """,
        body="""\
            #ifdef __WXMSW__
                return self->ShowNativeCaret(show);
            #else
                return false;
            #endif
            """)
    c.addCppMethod('bool', 'HideNativeCaret', '()',
        doc="""\
            Turn off the widget's native caret on Windows.
            Ignored on other platforms.
            """,
        body="""\
            #ifdef __WXMSW__
                return self->HideNativeCaret();
            #else
                return false;
            #endif
            """)

    # Methods for "file-like" compatibility
    c.addCppMethod('void', 'write', '(const wxString* text)',
        doc="Append text to the textctrl, for file-like compatibility.",
        body="self->AppendText(*text);")
    c.addCppMethod('void', 'flush', '()',
        doc="NOP, for file-like compatibility.",
        body="")


    # OSX methods for controlling native features
    c.find('OSXEnableAutomaticQuoteSubstitution').setCppCode("""\
        #ifdef __WXMAC__
            self->OSXEnableAutomaticQuoteSubstitution(enable);
        #else
            wxPyRaiseNotImplemented();
        #endif
        """)

    c.find('OSXEnableAutomaticDashSubstitution').setCppCode("""\
        #ifdef __WXMAC__
            self->OSXEnableAutomaticDashSubstitution(enable);
        #else
            wxPyRaiseNotImplemented();
        #endif
        """)

    c.find('OSXDisableAllSmartSubstitutions').setCppCode("""\
        #ifdef __WXMAC__
            self->OSXDisableAllSmartSubstitutions();
        #else
            wxPyRaiseNotImplemented();
        #endif
        """)

    # TODO: add support for wxTextProofOptions (only supported on MSW/GTK3)
    # so will need stubs on other platforms.
    c.find('EnableProofCheck').ignore()
    c.find('GetProofCheckOptions').ignore()

    # This method exists only on OSX
    c.find('OSXEnableNewLineReplacement').setCppCode("""\
        #ifdef __WXMAC__
            self->OSXEnableNewLineReplacement(enable);
        #endif
        """)



    c = module.find('wxTextUrlEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_TEXT        = wx.PyEventBinder( wxEVT_TEXT, 1)
        EVT_TEXT_ENTER  = wx.PyEventBinder( wxEVT_TEXT_ENTER, 1)
        EVT_TEXT_URL    = wx.PyEventBinder( wxEVT_TEXT_URL, 1)
        EVT_TEXT_MAXLEN = wx.PyEventBinder( wxEVT_TEXT_MAXLEN, 1)
        EVT_TEXT_CUT    = wx.PyEventBinder( wxEVT_TEXT_CUT )
        EVT_TEXT_COPY   = wx.PyEventBinder( wxEVT_TEXT_COPY )
        EVT_TEXT_PASTE  = wx.PyEventBinder( wxEVT_TEXT_PASTE )

        # deprecated wxEVT aliases
        wxEVT_COMMAND_TEXT_UPDATED   = wxEVT_TEXT
        wxEVT_COMMAND_TEXT_ENTER     = wxEVT_TEXT_ENTER
        wxEVT_COMMAND_TEXT_URL       = wxEVT_TEXT_URL
        wxEVT_COMMAND_TEXT_MAXLEN    = wxEVT_TEXT_MAXLEN
        wxEVT_COMMAND_TEXT_CUT       = wxEVT_TEXT_CUT
        wxEVT_COMMAND_TEXT_COPY      = wxEVT_TEXT_COPY
        wxEVT_COMMAND_TEXT_PASTE     = wxEVT_TEXT_PASTE
        """)

    return module


#-----------------------------------------------------------------
def run():
    module = parseAndTweakModule()
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

