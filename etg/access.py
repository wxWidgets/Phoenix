#---------------------------------------------------------------------------
# Name:        etg/access.py
# Author:      Robin Dunn
#
# Created:     08-Oct-2018
# Copyright:   (c) 2018 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "access"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxAccessible',

           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    #module.addHeaderCode('#include <wx/some_header_file.h>')

    module.addHeaderCode("""\
    #if !wxUSE_ACCESSIBILITY
        typedef enum
        {
            wxACC_FAIL,
            wxACC_FALSE,
            wxACC_OK,
            wxACC_NOT_IMPLEMENTED,
            wxACC_NOT_SUPPORTED
        } wxAccStatus;
        typedef enum
        {
            wxNAVDIR_DOWN,
            wxNAVDIR_FIRSTCHILD,
            wxNAVDIR_LASTCHILD,
            wxNAVDIR_LEFT,
            wxNAVDIR_NEXT,
            wxNAVDIR_PREVIOUS,
            wxNAVDIR_RIGHT,
            wxNAVDIR_UP
        } wxNavDir;
        typedef enum {
            wxROLE_NONE,
            wxROLE_SYSTEM_ALERT,
            wxROLE_SYSTEM_ANIMATION,
            wxROLE_SYSTEM_APPLICATION,
            wxROLE_SYSTEM_BORDER,
            wxROLE_SYSTEM_BUTTONDROPDOWN,
            wxROLE_SYSTEM_BUTTONDROPDOWNGRID,
            wxROLE_SYSTEM_BUTTONMENU,
            wxROLE_SYSTEM_CARET,
            wxROLE_SYSTEM_CELL,
            wxROLE_SYSTEM_CHARACTER,
            wxROLE_SYSTEM_CHART,
            wxROLE_SYSTEM_CHECKBUTTON,
            wxROLE_SYSTEM_CLIENT,
            wxROLE_SYSTEM_CLOCK,
            wxROLE_SYSTEM_COLUMN,
            wxROLE_SYSTEM_COLUMNHEADER,
            wxROLE_SYSTEM_COMBOBOX,
            wxROLE_SYSTEM_CURSOR,
            wxROLE_SYSTEM_DIAGRAM,
            wxROLE_SYSTEM_DIAL,
            wxROLE_SYSTEM_DIALOG,
            wxROLE_SYSTEM_DOCUMENT,
            wxROLE_SYSTEM_DROPLIST,
            wxROLE_SYSTEM_EQUATION,
            wxROLE_SYSTEM_GRAPHIC,
            wxROLE_SYSTEM_GRIP,
            wxROLE_SYSTEM_GROUPING,
            wxROLE_SYSTEM_HELPBALLOON,
            wxROLE_SYSTEM_HOTKEYFIELD,
            wxROLE_SYSTEM_INDICATOR,
            wxROLE_SYSTEM_LINK,
            wxROLE_SYSTEM_LIST,
            wxROLE_SYSTEM_LISTITEM,
            wxROLE_SYSTEM_MENUBAR,
            wxROLE_SYSTEM_MENUITEM,
            wxROLE_SYSTEM_MENUPOPUP,
            wxROLE_SYSTEM_OUTLINE,
            wxROLE_SYSTEM_OUTLINEITEM,
            wxROLE_SYSTEM_PAGETAB,
            wxROLE_SYSTEM_PAGETABLIST,
            wxROLE_SYSTEM_PANE,
            wxROLE_SYSTEM_PROGRESSBAR,
            wxROLE_SYSTEM_PROPERTYPAGE,
            wxROLE_SYSTEM_PUSHBUTTON,
            wxROLE_SYSTEM_RADIOBUTTON,
            wxROLE_SYSTEM_ROW,
            wxROLE_SYSTEM_ROWHEADER,
            wxROLE_SYSTEM_SCROLLBAR,
            wxROLE_SYSTEM_SEPARATOR,
            wxROLE_SYSTEM_SLIDER,
            wxROLE_SYSTEM_SOUND,
            wxROLE_SYSTEM_SPINBUTTON,
            wxROLE_SYSTEM_STATICTEXT,
            wxROLE_SYSTEM_STATUSBAR,
            wxROLE_SYSTEM_TABLE,
            wxROLE_SYSTEM_TEXT,
            wxROLE_SYSTEM_TITLEBAR,
            wxROLE_SYSTEM_TOOLBAR,
            wxROLE_SYSTEM_TOOLTIP,
            wxROLE_SYSTEM_WHITESPACE,
            wxROLE_SYSTEM_WINDOW
        } wxAccRole;
        typedef enum {
            wxOBJID_WINDOW,
            wxOBJID_SYSMENU,
            wxOBJID_TITLEBAR,
            wxOBJID_MENU,
            wxOBJID_CLIENT,
            wxOBJID_VSCROLL,
            wxOBJID_HSCROLL,
            wxOBJID_SIZEGRIP,
            wxOBJID_CARET,
            wxOBJID_CURSOR,
            wxOBJID_ALERT,
            wxOBJID_SOUND,
        } wxAccObject;
        typedef enum
        {
            wxACC_SEL_NONE,
            wxACC_SEL_TAKEFOCUS,
            wxACC_SEL_TAKESELECTION,
            wxACC_SEL_EXTENDSELECTION,
            wxACC_SEL_ADDSELECTION,
            wxACC_SEL_REMOVESELECTION,
        } wxAccSelectionFlags;
        #define wxACC_STATE_SYSTEM_ALERT_HIGH       0
        #define wxACC_STATE_SYSTEM_ALERT_MEDIUM     0
        #define wxACC_STATE_SYSTEM_ALERT_LOW        0
        #define wxACC_STATE_SYSTEM_ANIMATED         0
        #define wxACC_STATE_SYSTEM_BUSY             0
        #define wxACC_STATE_SYSTEM_CHECKED          0
        #define wxACC_STATE_SYSTEM_COLLAPSED        0
        #define wxACC_STATE_SYSTEM_DEFAULT          0
        #define wxACC_STATE_SYSTEM_EXPANDED         0
        #define wxACC_STATE_SYSTEM_EXTSELECTABLE    0
        #define wxACC_STATE_SYSTEM_FLOATING         0
        #define wxACC_STATE_SYSTEM_FOCUSABLE        0
        #define wxACC_STATE_SYSTEM_FOCUSED          0
        #define wxACC_STATE_SYSTEM_HOTTRACKED       0
        #define wxACC_STATE_SYSTEM_INVISIBLE        0
        #define wxACC_STATE_SYSTEM_MARQUEED         0
        #define wxACC_STATE_SYSTEM_MIXED            0
        #define wxACC_STATE_SYSTEM_MULTISELECTABLE  0
        #define wxACC_STATE_SYSTEM_OFFSCREEN        0
        #define wxACC_STATE_SYSTEM_PRESSED          0
        #define wxACC_STATE_SYSTEM_PROTECTED        0
        #define wxACC_STATE_SYSTEM_READONLY         0
        #define wxACC_STATE_SYSTEM_SELECTABLE       0
        #define wxACC_STATE_SYSTEM_SELECTED         0
        #define wxACC_STATE_SYSTEM_SELFVOICING      0
        #define wxACC_STATE_SYSTEM_UNAVAILABLE      0
        #define wxACC_EVENT_SYSTEM_SOUND              0
        #define wxACC_EVENT_SYSTEM_ALERT              0
        #define wxACC_EVENT_SYSTEM_FOREGROUND         0
        #define wxACC_EVENT_SYSTEM_MENUSTART          0
        #define wxACC_EVENT_SYSTEM_MENUEND            0
        #define wxACC_EVENT_SYSTEM_MENUPOPUPSTART     0
        #define wxACC_EVENT_SYSTEM_MENUPOPUPEND       0
        #define wxACC_EVENT_SYSTEM_CAPTURESTART       0
        #define wxACC_EVENT_SYSTEM_CAPTUREEND         0
        #define wxACC_EVENT_SYSTEM_MOVESIZESTART      0
        #define wxACC_EVENT_SYSTEM_MOVESIZEEND        0
        #define wxACC_EVENT_SYSTEM_CONTEXTHELPSTART   0
        #define wxACC_EVENT_SYSTEM_CONTEXTHELPEND     0
        #define wxACC_EVENT_SYSTEM_DRAGDROPSTART      0
        #define wxACC_EVENT_SYSTEM_DRAGDROPEND        0
        #define wxACC_EVENT_SYSTEM_DIALOGSTART        0
        #define wxACC_EVENT_SYSTEM_DIALOGEND          0
        #define wxACC_EVENT_SYSTEM_SCROLLINGSTART     0
        #define wxACC_EVENT_SYSTEM_SCROLLINGEND       0
        #define wxACC_EVENT_SYSTEM_SWITCHSTART        0
        #define wxACC_EVENT_SYSTEM_SWITCHEND          0
        #define wxACC_EVENT_SYSTEM_MINIMIZESTART      0
        #define wxACC_EVENT_SYSTEM_MINIMIZEEND        0
        #define wxACC_EVENT_OBJECT_CREATE                 0
        #define wxACC_EVENT_OBJECT_DESTROY                0
        #define wxACC_EVENT_OBJECT_SHOW                   0
        #define wxACC_EVENT_OBJECT_HIDE                   0
        #define wxACC_EVENT_OBJECT_REORDER                0
        #define wxACC_EVENT_OBJECT_FOCUS                  0
        #define wxACC_EVENT_OBJECT_SELECTION              0
        #define wxACC_EVENT_OBJECT_SELECTIONADD           0
        #define wxACC_EVENT_OBJECT_SELECTIONREMOVE        0
        #define wxACC_EVENT_OBJECT_SELECTIONWITHIN        0
        #define wxACC_EVENT_OBJECT_STATECHANGE            0
        #define wxACC_EVENT_OBJECT_LOCATIONCHANGE         0
        #define wxACC_EVENT_OBJECT_NAMECHANGE             0
        #define wxACC_EVENT_OBJECT_DESCRIPTIONCHANGE      0
        #define wxACC_EVENT_OBJECT_VALUECHANGE            0
        #define wxACC_EVENT_OBJECT_PARENTCHANGE           0
        #define wxACC_EVENT_OBJECT_HELPCHANGE             0
        #define wxACC_EVENT_OBJECT_DEFACTIONCHANGE        0
        #define wxACC_EVENT_OBJECT_ACCELERATORCHANGE      0

    class wxAccessible : public wxObject
    {
    public:
        wxAccessible(wxWindow* win = NULL) { wxPyRaiseNotImplemented(); }
        ~wxAccessible() {}

        virtual wxAccStatus DoDefaultAction(int childId) { return wxACC_OK; }
        virtual wxAccStatus GetChild(int childId, wxAccessible** child) { return wxACC_OK; }
        virtual wxAccStatus GetChildCount(int* childCount) { return wxACC_OK; }
        virtual wxAccStatus GetDefaultAction(int childId,
                                            wxString* actionName) { return wxACC_OK; }
        virtual wxAccStatus GetDescription(int childId,
                                        wxString* description) { return wxACC_OK; }
        virtual wxAccStatus GetFocus(int* childId, wxAccessible** child) { return wxACC_OK; }
        virtual wxAccStatus GetHelpText(int childId, wxString* helpText) { return wxACC_OK; }
        virtual wxAccStatus GetKeyboardShortcut(int childId,
                                                wxString* shortcut) { return wxACC_OK; }
        virtual wxAccStatus GetLocation(wxRect& rect, int elementId) { return wxACC_OK; }
        virtual wxAccStatus GetName(int childId, wxString* name) { return wxACC_OK; }
        virtual wxAccStatus GetParent(wxAccessible** parent) { return wxACC_OK; }
        virtual wxAccStatus GetRole(int childId, wxAccRole* role) { return wxACC_OK; }
        virtual wxAccStatus GetSelections(wxVariant* selections) { return wxACC_OK; }
        virtual wxAccStatus GetState(int childId, long* state) { return wxACC_OK; }
        virtual wxAccStatus GetValue(int childId, wxString* strValue) { return wxACC_OK; }
        wxWindow* GetWindow() { return NULL; }
        virtual wxAccStatus HitTest(const wxPoint& pt, int* childId,
                                    wxAccessible** childObject) { return wxACC_OK; }
        virtual wxAccStatus Navigate(wxNavDir navDir, int fromId,
                                    int* toId,
                                    wxAccessible** toObject) { return wxACC_OK; }
        static void NotifyEvent(int eventType, wxWindow* window,
                                wxAccObject objectType,
                                int objectId) { wxPyRaiseNotImplemented(); }
        virtual wxAccStatus Select(int childId,
                                wxAccSelectionFlags selectFlags) { return wxACC_OK; }
        void SetWindow(wxWindow* window) {}
    };
    #endif
    """)

    c = module.find('wxAccessible')
    assert isinstance(c, etgtools.ClassDef)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

