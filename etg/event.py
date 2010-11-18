#---------------------------------------------------------------------------
# Name:        etg/event.py
# Author:      Robin Dunn
#
# Created:     15-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "event"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 
    'wxEvtHandler',
    'wxEventBlocker',

    'wxEvent',
    'wxCommandEvent',

    'wxActivateEvent',
    'wxChildFocusEvent',
    'wxClipboardTextEvent',
    'wxCloseEvent',
    'wxContextMenuEvent',
    'wxDisplayChangedEvent',
    'wxDropFilesEvent',
    'wxEraseEvent',
    'wxFocusEvent',
    'wxHelpEvent',
    'wxIconizeEvent',
    'wxIdleEvent',
    'wxInitDialogEvent',
    'wxJoystickEvent',
    'wxKeyEvent',
    'wxMaximizeEvent',
    'wxMenuEvent',
    'wxMouseCaptureChangedEvent',
    'wxMouseCaptureLostEvent',
    'wxMouseEvent',
    'wxMoveEvent',
    'wxNavigationKeyEvent',
    'wxNotifyEvent',
    'wxPaintEvent',
    'wxPaletteChangedEvent',
    'wxQueryNewPaletteEvent',
    'wxScrollEvent',
    'wxScrollWinEvent',
    'wxSetCursorEvent',
    'wxShowEvent',
    'wxSizeEvent',
    'wxSysColourChangedEvent',
    'wxUpdateUIEvent',
    'wxWindowCreateEvent',
    'wxWindowDestroyEvent',
    
    #'wxThreadEvent',
]    
    
#---------------------------------------------------------------------------
# Parse the XML file(s) building a collection of Extractor objects

import etgtools
import etgtools.tweaker_tools as tools

module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
etgtools.parseDoxyXML(module, ITEMS)

#---------------------------------------------------------------------------
# Tweak the parsed meta objects in the module object as needed for customizing
# the generated code and docstrings.

module.addCppCode("""
#if !wxUSE_HOTKEY
#define wxEVT_HOTKEY 0
#endif
""")

module.insertItem(0, etgtools.WigCode("class wxWindow;  // forward declaration"))
module.insertItem(0, etgtools.WigCode("class wxDC;      // forward declaration"))
module.insertItem(0, etgtools.WigCode("class wxMenu;    // forward declaration"))
module.insertItem(0, etgtools.WigCode("class wxCursor;  // forward declaration"))

# TODO:
#   * PyEventBinder class
#   * event binder instances for all the event types implemented here
#   * Connect, Bind etc. methods for EvtHandler


#---------------------------------------
# wxEvtHandler
c = module.find('wxEvtHandler')
c.addPrivateCopyCtor()

# Ignore the Connect/Disconnect and Bind/Unbind methods for now. 
for item in c.allItems():
    if item.name in ['Connect', 'Disconnect', 'Bind', 'Unbind']:
        item.ignore()


# wxEventTable is not documented so we have to ignore SearchEventTable.
# TODO: Should wxEventTable be available to language bindings?
c.find('SearchEventTable').ignore()

# TODO: If we don't need to use the wxEvtHandler's client data for our own
# tracking then enable these....
c.find('GetClientObject').ignore()
c.find('SetClientObject').ignore()
c.find('GetClientData').ignore()
c.find('SetClientData').ignore()


#---------------------------------------
# wxEvent
c = module.find('wxEvent')
c.abstract = True
c.find('Clone').factory = True

# Clone is not declared in the derived classes where it is implemented so we
# need to pretend that it is not pure-virtual so the derived classes will not
# be marked as abstract. Although perhaps it would be better to go ahead and
# add the declaration to the derived classes?    TODO: decide this
c.find('Clone').isPureVirtual = False   

c.addProperty('EventObject GetEventObject SetEventObject')
c.addProperty('EventType GetEventType SetEventType')
c.addProperty('Id GetId SetId')
c.addProperty('Skipped GetSkipped')
c.addProperty('Timestamp GetTimestamp SetTimestamp')



#---------------------------------------
# wxCommandEvent
c = module.find('wxCommandEvent')
assert isinstance(c, etgtools.ClassDef)

c.find('GetClientObject').ignore()
c.find('SetClientObject').ignore()
c.find('GetClientData').ignore()
c.find('SetClientData').ignore()

c.addCppMethod('SIP_PYOBJECT', 'GetClientData', '()', """\
     wxPyClientData* data = (wxPyClientData*)sipCpp->GetClientObject();
     if (data) {
         Py_INCREF(data->m_obj);
         sipRes = data->m_obj;
     } else {
         Py_INCREF(Py_None);
         sipRes = Py_None;
     }
""")

c.addCppMethod('void', 'SetClientData', '(SIP_PYOBJECT clientData)', """\
    wxPyClientData* data = new wxPyClientData(clientData);
    sipCpp->SetClientObject(data);
""")


c.addProperty('ClientData GetClientData SetClientData')
c.addProperty('ExtraLong GetExtraLong SetExtraLong')
c.addProperty('Int GetInt SetInt')
c.addProperty('Selection GetSelection')
c.addProperty('String GetString SetString')
    

#---------------------------------------
# wxKeyEvent
c = module.find('wxKeyEvent')

c.find('GetPosition').findOverload('long').ignore()

c.addProperty('X GetX')
c.addProperty('Y GetY')
c.addProperty('KeyCode GetKeyCode')
c.addProperty('Position GetPosition')
c.addProperty('RawKeyCode GetRawKeyCode')
c.addProperty('RawKeyFlags GetRawKeyFlags')
c.addProperty('UnicodeKey GetUnicodeKey')

#---------------------------------------
# wxScrollEvent
c = module.find('wxScrollEvent')
c.addProperty('Orientation GetOrientation SetOrientation')
c.addProperty('Position GetPosition SetPosition')

#---------------------------------------
# wxScrollWinEvent
c = module.find('wxScrollWinEvent')
c.addProperty('Orientation GetOrientation SetOrientation')
c.addProperty('Position GetPosition SetPosition')

#---------------------------------------
# wxMouseEvent
c = module.find('wxMouseEvent')
c.addProperty('LinesPerAction GetLinesPerAction')
c.addProperty('LogicalPosition GetLogicalPosition')
c.addProperty('WheelDelta GetWheelDelta')
c.addProperty('WheelRotation GetWheelRotation')

#---------------------------------------
# wxSetCursorEvent
c = module.find('wxSetCursorEvent')
c.addProperty('Cursor GetCursor SetCursor')
c.addProperty('X GetX')
c.addProperty('Y GetY')

#---------------------------------------
# wxSizeEvent
c = module.find('wxSizeEvent')
c.addProperty('Rect GetRect SetRect')
c.addProperty('Size GetSize SetSize')

#---------------------------------------
# wxMoveEvent
c = module.find('wxMoveEvent')
c.addProperty('Rect GetRect SetRect')
c.addProperty('Position GetPosition SetPosition')

#---------------------------------------
# wxEraseEvent
c = module.find('wxEraseEvent')
c.addProperty('DC GetDC')

#---------------------------------------
# wxFocusEvent
c = module.find('wxFocusEvent')
c.addProperty('Window GetWindow SetWindow')

#---------------------------------------
# wxChildFocusEvent
c = module.find('wxChildFocusEvent')
c.addProperty('Window GetWindow')


#---------------------------------------
# wxActivateEvent
c = module.find('wxActivateEvent')
c.addProperty('Active GetActive')

#---------------------------------------
# wxMenuEvent
c = module.find('wxMenuEvent')
c.addProperty('Menu GetMenu')
c.addProperty('MenuId GetMenuId')

#---------------------------------------
# wxShowEvent
c = module.find('wxShowEvent')
c.addProperty('Show IsShown SetShow')

#---------------------------------------
# wxDropFilesEvent
c = module.find('wxDropFilesEvent')
c.addProperty('Files GetFiles')
c.addProperty('NumberOfFiles GetNumberOfFiles')
c.addProperty('Position GetPosition')

#---------------------------------------
# wxUpdateUIEvent
c = module.find('wxUpdateUIEvent')
c.addProperty('Checked GetChecked Check')
c.addProperty('Enabled GetEnabled Enable')
c.addProperty('Shown GetShown Show')
c.addProperty('Text GetText SetText')

#---------------------------------------
# wxMouseCaptureChangedEvent
c = module.find('wxMouseCaptureChangedEvent')
c.addProperty('CapturedWindow GetCapturedWindow')

#---------------------------------------
# wxPaletteChangedEvent
c = module.find('wxPaletteChangedEvent')
c.addProperty('ChangedWindow GetChangedWindow SetChangedWindow')

#---------------------------------------
# wxQueryNewPaletteEvent
c = module.find('wxQueryNewPaletteEvent')
c.addProperty('PaletteRealized GetPaletteRealized SetPaletteRealized')

#---------------------------------------
# wxNavigationKeyEvent
c = module.find('wxNavigationKeyEvent')
c.addProperty('CurrentFocus GetCurrentFocus SetCurrentFocus')
c.addProperty('Direction GetDirection SetDirection')
#c.addProperty('FromTab IsFromTab SetFromTab')
#c.addProperty('WindowChange IsWindowChange SetWindowChange')

# ignore the copy ctor because we'll be adding a private one below
c.find('wxNavigationKeyEvent').findOverload('const wxNavigationKeyEvent').ignore()


#---------------------------------------
# wxWindowCreateEvent
c = module.find('wxWindowCreateEvent')
c.addProperty('Window GetWindow')

#---------------------------------------
# wxWindowDestroyEvent
c = module.find('wxWindowDestroyEvent')
c.addProperty('Window GetWindow')

#---------------------------------------
# wxContextMenuEvent
c = module.find('wxContextMenuEvent')
c.addProperty('Position GetPosition SetPosition')





#--------------------------------------- 
# Supress the automatic use of an assignment operator for these classes, by
# the back-end generator, assuming they are smart enough to do that if they
# see a private assignment operator in the class declaration.

for name in [n for n in ITEMS if n.endswith('Event')]:
    c = module.find(name)
    c.addPrivateAssignOp()



#---------------------------------------------------------------------------
tools.ignoreAssignmentOperators(module)
tools.removeWxPrefixes(module)
#---------------------------------------------------------------------------
# Run the generators

# Create the code generator and make the wrapper code
wg = etgtools.getWrapperGenerator()
wg.generate(module)

# Create a documentation generator and let it do its thing
dg = etgtools.getDocsGenerator()
dg.generate(module)

#---------------------------------------------------------------------------
