#---------------------------------------------------------------------------
# Name:        etg/_stc.py
# Author:      Robin Dunn
#
# Created:     24-Oct-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_stc"
NAME      = "_stc"   # Base name of the file to generate to for this script
DOCSTRING = """\
The :ref:`wx.stc.StyledTextCrtl` class provided by this module is a text widget
primarily intended for use as a syntax highlighting source code editor.  It is
based on the popular Scintilla widget.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxStyledTextCtrl',
           'wxStyledTextEvent',
          ]


# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "stc" library in a multi-lib build.
INCLUDES = [ ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from the build scripts to get a list of
# sources and/or additional dependencies when building this extension module.
ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
DEPENDS = tools.getNonEtgFiles(INCLUDES)
OTHERDEPS = [  ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    module.check4unittest = False

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wxPython/wxpy_api.h>')
    module.addImport('_core')
    module.addPyCode('''\
    import wx
    ID_ANY = wx.ID_ANY  # Needed for some parameter defaults in this module
    ''', order=10)
    module.addInclude(INCLUDES)


    #-----------------------------------------------------------------

    module.addHeaderCode('#include <wx/stc/stc.h>')
    module.addHeaderCode('#include "wxpybuffer.h"')


    c = module.find('wxStyledTextCtrl')
    assert isinstance(c, etgtools.ClassDef)
    c.bases = ['wxControl']  # wxTextCtrlIface is also a base...
    c.piBases = ['wx.Control', 'wx.TextEntry']
    tools.fixWindowClass(c, False)
    module.addGlobalStr('wxSTCNameStr', c)


    c.find('GetCurLine.linePos').out = True
    c.find('GetCurLineRaw.linePos').out = True
    for name in ['Remove', 'Replace', 'SetSelection', 'GetSelection']:
        m = c.find(name)
        m.find('from').name = 'from_'
        m.find('to').name = 'to_'

    c.find('GetSelection.from_').out = True
    c.find('GetSelection.to_').out = True
    c.find('PositionToXY.x').out = True
    c.find('PositionToXY.y').out = True

    c.find('FindText.findEnd').out = True

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


    # Replace the *Pointer methods with ones that return a memoryview object instead.
    c.find('GetCharacterPointer').ignore()
    c.addCppMethod('PyObject*', 'GetCharacterPointer', '()',
        doc="""\
            Compact the document buffer and return a read-only memoryview
            object of the characters in the document.""",
        body="""
            const char* ptr = self->GetCharacterPointer();
            Py_ssize_t len = self->GetLength();
            PyObject* rv;
            wxPyBLOCK_THREADS( rv = wxPyMakeBuffer((void*)ptr, len, true) );
            return rv;
            """)

    c.find('GetRangePointer').ignore()
    c.addCppMethod('PyObject*', 'GetRangePointer', '(int position, int rangeLength)',
        doc="""\
            Return a read-only pointer to a range of characters in the
            document. May move the gap so that the range is contiguous,
            but will only move up to rangeLength bytes.""",
        body="""
            const char* ptr = self->GetRangePointer(position, rangeLength);
            Py_ssize_t len = rangeLength;
            PyObject* rv;
            wxPyBLOCK_THREADS( rv = wxPyMakeBuffer((void*)ptr, len, true) );
            return rv;
            """)


    # Generate the code for this differently because it needs to be
    # forcibly mashed into an int in the C code
    module.find('wxSTC_MASK_FOLDERS').forcedInt = True


    # Make sure that all the methods from wxTextEntry and wxTextCtrl are
    # included. This is needed because we are pretending that this class only
    # derives from wxControl but the real C++ class also derives from
    # wxTextCtrlIface which derives from wxTextEntryBase.
    import textentry
    mod = textentry.parseAndTweakModule()
    klass = mod.find('wxTextEntry')
    items = [item for item in klass.items if isinstance(item, etgtools.MethodDef) and
                                             not item.isCtor and
                                             not item.isDtor and
                                             not c.findItem(item.name)]
    c.items.extend(items)

    tc_excludes = ['OSXEnableAutomaticQuoteSubstitution',
                   'OSXEnableAutomaticDashSubstitution',
                   'OSXDisableAllSmartSubstitutions',
                   'OSXEnableNewLineReplacement',
                   ]
    import textctrl
    mod = textctrl.parseAndTweakModule()
    klass = mod.find('wxTextCtrl')
    items = [item for item in klass.items if isinstance(item, etgtools.MethodDef) and
                                             not item.isCtor and
                                             not item.isDtor and
                                             not c.findItem(item.name) and
                                             not item.name in tc_excludes]
    c.items.extend(items)

    c.find('EmulateKeyPress').ignore()
    c.find('IsMultiLine').ignore()
    c.find('IsSingleLine').ignore()
    c.find('MacCheckSpelling').ignore()
    c.find('ShowNativeCaret').ignore()
    c.find('HideNativeCaret').ignore()

    # Change the *RGBAImage methods to accept any buffer object
    c.find('MarkerDefineRGBAImage').ignore()
    c.addCppMethod('void', 'MarkerDefineRGBAImage', '(int markerNumber, wxPyBuffer* pixels)',
        doc="""\
            Define a marker from RGBA data.\n
            It has the width and height from RGBAImageSetWidth/Height. You must
            ensure that the buffer is at least width*height*4 bytes long.
            """,
        body="""\
            self->MarkerDefineRGBAImage(markerNumber, (unsigned char*)pixels->m_ptr);
            """)

    c.find('RegisterRGBAImage').ignore()
    c.addCppMethod('void', 'RegisterRGBAImage', '(int type, wxPyBuffer* pixels)',
        doc="""\
            Register an RGBA image for use in autocompletion lists.\n
            It has the width and height from RGBAImageSetWidth/Height. You must
            ensure that the buffer is at least width*height*4 bytes long.
            """,
        body="""\
            self->RegisterRGBAImage(type, (unsigned char*)pixels->m_ptr);
            """)

    c.find('MarkerDefinePixmap').ignore()
    c.find('RegisterImage').findOverload('xpmData').ignore()

    # TODO:  Add the UTF8 PyMethods from classic (see _stc_utf8_methods.py)


    #-----------------------------------------------------------------
    c = module.find('wxStyledTextEvent')
    tools.fixEventClass(c)

    module.addPyCode("""\
        EVT_STC_CHANGE = wx.PyEventBinder( wxEVT_STC_CHANGE, 1 )
        EVT_STC_STYLENEEDED = wx.PyEventBinder( wxEVT_STC_STYLENEEDED, 1 )
        EVT_STC_CHARADDED = wx.PyEventBinder( wxEVT_STC_CHARADDED, 1 )
        EVT_STC_SAVEPOINTREACHED = wx.PyEventBinder( wxEVT_STC_SAVEPOINTREACHED, 1 )
        EVT_STC_SAVEPOINTLEFT = wx.PyEventBinder( wxEVT_STC_SAVEPOINTLEFT, 1 )
        EVT_STC_ROMODIFYATTEMPT = wx.PyEventBinder( wxEVT_STC_ROMODIFYATTEMPT, 1 )
        EVT_STC_KEY = wx.PyEventBinder( wxEVT_STC_KEY, 1 )
        EVT_STC_DOUBLECLICK = wx.PyEventBinder( wxEVT_STC_DOUBLECLICK, 1 )
        EVT_STC_UPDATEUI = wx.PyEventBinder( wxEVT_STC_UPDATEUI, 1 )
        EVT_STC_MODIFIED = wx.PyEventBinder( wxEVT_STC_MODIFIED, 1 )
        EVT_STC_MACRORECORD = wx.PyEventBinder( wxEVT_STC_MACRORECORD, 1 )
        EVT_STC_MARGINCLICK = wx.PyEventBinder( wxEVT_STC_MARGINCLICK, 1 )
        EVT_STC_NEEDSHOWN = wx.PyEventBinder( wxEVT_STC_NEEDSHOWN, 1 )
        EVT_STC_PAINTED = wx.PyEventBinder( wxEVT_STC_PAINTED, 1 )
        EVT_STC_USERLISTSELECTION = wx.PyEventBinder( wxEVT_STC_USERLISTSELECTION, 1 )
        EVT_STC_URIDROPPED = wx.PyEventBinder( wxEVT_STC_URIDROPPED, 1 )
        EVT_STC_DWELLSTART = wx.PyEventBinder( wxEVT_STC_DWELLSTART, 1 )
        EVT_STC_DWELLEND = wx.PyEventBinder( wxEVT_STC_DWELLEND, 1 )
        EVT_STC_START_DRAG = wx.PyEventBinder( wxEVT_STC_START_DRAG, 1 )
        EVT_STC_DRAG_OVER = wx.PyEventBinder( wxEVT_STC_DRAG_OVER, 1 )
        EVT_STC_DO_DROP = wx.PyEventBinder( wxEVT_STC_DO_DROP, 1 )
        EVT_STC_ZOOM = wx.PyEventBinder( wxEVT_STC_ZOOM, 1 )
        EVT_STC_HOTSPOT_CLICK = wx.PyEventBinder( wxEVT_STC_HOTSPOT_CLICK, 1 )
        EVT_STC_HOTSPOT_DCLICK = wx.PyEventBinder( wxEVT_STC_HOTSPOT_DCLICK, 1 )
        EVT_STC_HOTSPOT_RELEASE_CLICK = wx.PyEventBinder( wxEVT_STC_HOTSPOT_RELEASE_CLICK, 1 )
        EVT_STC_CALLTIP_CLICK = wx.PyEventBinder( wxEVT_STC_CALLTIP_CLICK, 1 )
        EVT_STC_AUTOCOMP_SELECTION = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_SELECTION, 1 )
        EVT_STC_INDICATOR_CLICK = wx.PyEventBinder( wxEVT_STC_INDICATOR_CLICK, 1 )
        EVT_STC_INDICATOR_RELEASE = wx.PyEventBinder( wxEVT_STC_INDICATOR_RELEASE, 1 )
        EVT_STC_AUTOCOMP_CANCELLED = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_CANCELLED, 1 )
        EVT_STC_AUTOCOMP_CHAR_DELETED = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_CHAR_DELETED, 1 )
        EVT_STC_CLIPBOARD_COPY = wx.PyEventBinder( wxEVT_STC_CLIPBOARD_COPY, 1)
        EVT_STC_CLIPBOARD_PASTE = wx.PyEventBinder( wxEVT_STC_CLIPBOARD_PASTE, 1)
        EVT_STC_AUTOCOMP_COMPLETED = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_COMPLETED, 1)
        EVT_STC_MARGIN_RIGHT_CLICK = wx.PyEventBinder( wxEVT_STC_MARGIN_RIGHT_CLICK, 1)
        EVT_STC_AUTOCOMP_SELECTION_CHANGE = wx.PyEventBinder( wxEVT_STC_AUTOCOMP_SELECTION_CHANGE, 1)
        """)

    #-----------------------------------------------------------------

    # Keep some of the old names
    module.addPyCode("""\
        # compatibility aliases
        STC_SCMOD_NORM = STC_KEYMOD_NORM
        STC_SCMOD_SHIFT = STC_KEYMOD_SHIFT
        STC_SCMOD_CTRL = STC_KEYMOD_CTRL
        STC_SCMOD_ALT = STC_KEYMOD_ALT
        STC_SCMOD_SUPER = STC_KEYMOD_SUPER
        STC_SCMOD_META = STC_KEYMOD_META
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
