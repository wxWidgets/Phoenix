#---------------------------------------------------------------------------
# Name:        etg/window.py
# Author:      Robin Dunn
#
# Created:     27-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "window"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxVisualAttributes',
           'wxWindow' ]    
    
OTHERDEPS = [ 'src/window_ex.cpp',   # some helper C++ code
              ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.    

    c = module.find('wxWindow')
    assert isinstance(c, etgtools.ClassDef)
    
    # First we need to let the wrapper generator know about wxWindowBase since
    # AddChild and RemoveChild need to use that type in order to be virtualized.
    wc = etgtools.WigCode("""\
    class wxWindowBase : wxEvtHandler  /Abstract/
    {
    public:
        virtual void AddChild( wxWindowBase* child );
        virtual void RemoveChild( wxWindowBase* child );
    };
    """)
    module.insertItemBefore(c, wc)

    # Now change the base class of wxWindow
    c.bases = ['wxWindowBase']
    
    # And fix the arg types we get from Doxy
    c.find('AddChild.child').type = 'wxWindowBase*'
    c.find('RemoveChild.child').type = 'wxWindowBase*'
    
    
    # We now return you to our regularly scheduled programming...
    tools.fixWindowClass(c)

    c.includeCppCode('src/window_ex.cpp')

    # ignore some overloads that will be ambiguous afer wrapping
    c.find('GetChildren').overloads = []
    c.find('GetClientSize').findOverload('int *').ignore()
    c.find('GetSize').findOverload('int *').ignore()
    c.find('GetVirtualSize').findOverload('int *').ignore()
    c.find('GetPosition').findOverload('int *').ignore()
    c.find('GetScreenPosition').findOverload('int *').ignore()
    c.find('ClientToScreen').findOverload('int *').ignore()
    c.find('ScreenToClient').findOverload('int *').ignore()
    
    # Rename these overloads for symmetry with the getters of the same name
    c.find('SetSize').findOverload('wxRect').pyName = 'SetRect'
    c.find('SetClientSize').findOverload('wxRect').pyName = 'SetClientRect'
    
    m = c.find('GetTextExtent').findOverload('int *')
    m.pyName = 'GetFullTextExtent'
    m.find('w').out = True
    m.find('h').out = True
    m.find('descent').out = True
    m.find('externalLeading').out = True
    
    c.find('GetHandle').type = 'void*'
    c.find('GetHandle').setCppCode("sipRes = wxPyGetWinHandle(sipCpp);")
    
    c.addCppMethod('void*', 'GetGtkWidget', '()', """\
    #ifdef __WXGTK__
        return (void*)self->GetHandle();
    #else
        return NULL;
    #endif
    """)
    
    # Add some new methods
    c.addCppMethod('wxWindow*', 'GetTopLevelParent', '()',
                   'return wxGetTopLevelParent(self);')
    #c.addCppMethod('wxWindow*', 'FindWindowByLabel', '(const wxString& label)', 
    #               'return wxWindow::FindWindowByLabel(label, self);')
    
    c.addCppMethod('bool', 'MacIsWindowScrollbar', '(const wxWindow* sb)', """\
    #ifdef __WXMAC__
        return self->MacIsWindowScrollbar(sb); 
    #else
        return false;
    #endif
    """)
    
    # Make the Register/UnregisterHotKey functions be available on Windows,
    # and empty stubs otherwise
    c.find('RegisterHotKey').setCppCode("""\
    #ifdef __WXMSW__
        sipRes = sipCpp->RegisterHotKey(hotkeyId, modifiers, virtualKeyCode);
    #else
        sipRes = false;
    #endif
    """)
    c.find('UnregisterHotKey').setCppCode("""\
    #ifdef __WXMSW__
        sipRes = sipCpp->UnregisterHotKey(hotkeyId);
    #else
        sipRes = false;
    #endif
    """)    
    c.find('RegisterHotKey').isVirtual = False
    c.find('UnregisterHotKey').isVirtual = False

    
    c.find('SetDoubleBuffered').setCppCode("""\
    #if defined(__WXGTK20__) || defined(__WXMSW__)
        sipCpp->SetDoubleBuffered(on);
    #endif
    """)

    #%Rename(ConvertDialogPointToPixels, wxPoint, ConvertDialogToPixels(const wxPoint& pt));
    #%Rename(ConvertDialogSizeToPixels,  wxSize,  ConvertDialogToPixels(const wxSize& sz));
    #%Rename(ConvertPixelPointToDialog, wxPoint, ConvertPixelsToDialog(const wxPoint& pt));
    #%Rename(ConvertPixelSizeToDialog,  wxSize,  ConvertPixelsToDialog(const wxSize& sz));
    
    # MSW only.  Do we want them wrapped?
    c.find('GetAccessible').ignore()
    c.find('SetAccessible').ignore()
   
    # Make some of the protected methods visible and overridable from Python
    c.find('SendDestroyEvent').ignore(False)

    c.find('Destroy').transferThis=True
    c.addPyMethod('PostCreate', '(self, pre)', 'pass')
    
    # transfer ownership of these parameters to the C++ object
    c.find('SetCaret.caret').transfer = True
    c.find('SetToolTip.tip').transfer = True
    c.find('SetDropTarget.target').transfer = True
    c.find('SetConstraints.constraints').transfer = True
    c.find('SetSizer.sizer').transfer = True
    c.find('SetSizerAndFit.sizer').transfer = True
    
    # Define some properties using the getter and setter methods
    c.addProperty('AcceleratorTable GetAcceleratorTable SetAcceleratorTable')
    c.addProperty('AutoLayout GetAutoLayout SetAutoLayout')
    c.addProperty('BackgroundColour GetBackgroundColour SetBackgroundColour')
    c.addProperty('BackgroundStyle GetBackgroundStyle SetBackgroundStyle')
    c.addProperty('EffectiveMinSize GetEffectiveMinSize')
    c.addProperty('BestSize GetBestSize')
    c.addProperty('BestVirtualSize GetBestVirtualSize')
    c.addProperty('Border GetBorder')
    c.addProperty('Caret GetCaret SetCaret')
    c.addProperty('CharHeight GetCharHeight')
    c.addProperty('CharWidth GetCharWidth')
    c.addProperty('Children GetChildren')
    c.addProperty('ClientAreaOrigin GetClientAreaOrigin')
    c.addProperty('ClientRect GetClientRect SetClientRect')
    c.addProperty('ClientSize GetClientSize SetClientSize')
    c.addProperty('Constraints GetConstraints SetConstraints')
    c.addProperty('ContainingSizer GetContainingSizer SetContainingSizer')
    c.addProperty('Cursor GetCursor SetCursor')
    c.addProperty('DefaultAttributes GetDefaultAttributes')
    c.addProperty('DropTarget GetDropTarget SetDropTarget')
    c.addProperty('EventHandler GetEventHandler SetEventHandler')
    c.addProperty('ExtraStyle GetExtraStyle SetExtraStyle')
    c.addProperty('Font GetFont SetFont')
    c.addProperty('ForegroundColour GetForegroundColour SetForegroundColour')
    c.addProperty('GrandParent GetGrandParent')
    c.addProperty('TopLevelParent GetTopLevelParent')
    c.addProperty('Handle GetHandle')
    c.addProperty('HelpText GetHelpText SetHelpText')
    c.addProperty('Id GetId SetId')
    c.addProperty('Label GetLabel SetLabel')
    c.addProperty('LayoutDirection GetLayoutDirection SetLayoutDirection')
    c.addProperty('MaxHeight GetMaxHeight')
    c.addProperty('MaxSize GetMaxSize SetMaxSize')
    c.addProperty('MaxWidth GetMaxWidth')
    c.addProperty('MinHeight GetMinHeight')
    c.addProperty('MinSize GetMinSize SetMinSize')
    c.addProperty('MinWidth GetMinWidth')
    c.addProperty('Name GetName SetName')
    c.addProperty('Parent GetParent')
    c.addProperty('Position GetPosition SetPosition')
    c.addProperty('Rect GetRect SetRect')
    c.addProperty('ScreenPosition GetScreenPosition')
    c.addProperty('ScreenRect GetScreenRect')
    c.addProperty('Size GetSize SetSize')
    c.addProperty('Sizer GetSizer SetSizer')
    c.addProperty('ThemeEnabled GetThemeEnabled SetThemeEnabled')
    c.addProperty('ToolTip GetToolTip SetToolTip')
    c.addProperty('UpdateClientRect GetUpdateClientRect')
    c.addProperty('UpdateRegion GetUpdateRegion')
    c.addProperty('Validator GetValidator SetValidator')
    c.addProperty('VirtualSize GetVirtualSize SetVirtualSize')
    c.addProperty('WindowStyle GetWindowStyle SetWindowStyle')
    c.addProperty('WindowStyleFlag GetWindowStyleFlag SetWindowStyleFlag')
    c.addProperty('WindowVariant GetWindowVariant SetWindowVariant')
    c.addProperty('Shown IsShown Show')
    c.addProperty('Enabled IsEnabled Enable')
    c.addProperty('TopLevel IsTopLevel')
    c.addProperty('MinClientSize GetMinClientSize SetMinClientSize')
    c.addProperty('MaxClientSize GetMaxClientSize SetMaxClientSize')
    ##c.addProperty('GtkWidget GetGtkWidget')



    # We probably won't ever need most of the wxWindow virtuals to be
    # overridable in Python, so we'll clear all the virtual flags here and add
    # back those that we want to keep in the next step.
    tools.removeVirtuals(c)
    tools.addWindowVirtuals(c)

    
    
    module.addPyCode('''\
    class FrozenWindow(object):
        """
        A context manager to be used with Python 'with' statements
        that will freeze the given window for the duration of the
        with block.
        """
        def __init__(self, window):
            self._win = window
        def __enter__(self):
            self._win.Freeze()
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            self._win.Thaw()
    ''')
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

