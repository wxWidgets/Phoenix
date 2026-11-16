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

import os
import xml.etree.ElementTree as ET

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "textctrl"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxTextProofOptions',
           'wxTextAttr',
           'wxTextCtrl',
           'wxTextUrlEvent',
           'wxTextSearch',
           'wxTextSearchResult',
           ]

#---------------------------------------------------------------------------

def parseAndTweakModule():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # wxGTK builds without gspell have no spell checking and no
    # wxTextProofOptions, so give them one that never enables any checks
    module.addHeaderCode("""\
        #include <wx/textctrl.h>
        #if !wxUSE_SPELLCHECK
        class wxTextProofOptions
        {
        public:
            static wxTextProofOptions Default() { return wxTextProofOptions().SpellCheck(true); }
            static wxTextProofOptions Disable() { return wxTextProofOptions(); }
            wxTextProofOptions& SpellCheck(bool enable = true) { m_EnableSpellCheck = enable; return *this; }
            wxTextProofOptions& GrammarCheck(bool enable = true) { m_EnableGrammarCheck = enable; return *this; }
            wxTextProofOptions& Language(const wxString& lang) { m_lang = lang; return *this; }
            bool IsSpellCheckEnabled() const { return m_EnableSpellCheck; }
            bool IsGrammarCheckEnabled() const { return m_EnableGrammarCheck; }
            const wxString& GetLang() const { return m_lang; }
            bool AnyChecksEnabled() const { return m_EnableSpellCheck || m_EnableGrammarCheck; }
        private:
            wxTextProofOptions() : m_EnableSpellCheck(false), m_EnableGrammarCheck(false) { }
            wxString m_lang;
            bool m_EnableSpellCheck;
            bool m_EnableGrammarCheck;
        };
        #endif
        """)

    # The interface header has no "public:" in this class, so Doxygen calls
    # all of its methods private and they weren't extracted
    c = module.find('wxTextProofOptions')
    c.noDefCtor = True
    xml = ET.parse(os.path.join(etgtools.XMLSRC, 'classwx_text_proof_options.xml'))
    for node in xml.getroot().findall('compounddef/sectiondef/memberdef[@kind="function"]'):
        node.set('prot', 'public')
        c.addItem(etgtools.MethodDef(node, c.name, klass=c))

    c = module.find('wxTextAttr')
    assert isinstance(c, etgtools.ClassDef)
    c.find('operator=').ignore()
    c.find('SetFont').pyArgsString = '(font, flags=TEXT_ATTR_FONT & ~TEXT_ATTR_FONT_PIXEL_SIZE)'
    c.find('SetFontUnderlined').renameOverload('wxTextAttrUnderlineType',
                                               'SetFontUnderlineType')


    c = module.find('wxTextCtrl')
    tools.fixTextClipboardMethods(c)

    # Not virtual, since there's nothing to override without spell checking
    m = c.find('EnableProofCheck')
    m.isVirtual = False
    m.setCppCode("""\
        #if wxUSE_SPELLCHECK
            return self->EnableProofCheck(*options);
        #else
            return false;
        #endif
        """)
    m = c.find('GetProofCheckOptions')
    m.isVirtual = False
    m.setCppCode_sip("""\
        #if wxUSE_SPELLCHECK
            sipRes = new wxTextProofOptions(sipCpp->GetProofCheckOptions());
        #else
            sipRes = new wxTextProofOptions(wxTextProofOptions::Disable());
        #endif
        """)
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

    c.find('GTKGetTextBuffer').ignore()
    c.find('GTKGetEditable').ignore()
    c.find('GTKSetPangoMarkup').ignore()

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

