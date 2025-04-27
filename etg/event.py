#---------------------------------------------------------------------------
# Name:        etg/event.py
# Author:      Robin Dunn
#
# Created:     15-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import PyFunctionDef, PyCodeDef, PyPropertyDef

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "event"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [
    'wxEvtHandler',
    'wxEventBlocker',
    'wxPropagationDisabler',
    'wxPropagateOnce',

    'wxEvent',
    'wxCommandEvent',

    'wxActivateEvent',
    'wxChildFocusEvent',
    'wxClipboardTextEvent',
    'wxCloseEvent',
    'wxContextMenuEvent',
    'wxDisplayChangedEvent',
    'wxDPIChangedEvent',
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
    'wxFullScreenEvent',
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

    'wxGestureEvent',
    'wxPanGestureEvent',
    'wxZoomGestureEvent',
    'wxRotateGestureEvent',
    'wxTwoFingerTapEvent',
    'wxLongPressEvent',
    'wxPressAndTapEvent',


    'wxThreadEvent',

]


OTHERDEPS = [ 'src/event_ex.py',
              'src/event_ex.cpp',
              ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addCppCode("""
    #if !wxUSE_HOTKEY
    #define wxEVT_HOTKEY 0
    #endif
    """)


    module.addPyClass('PyEventBinder', ['object'],
        doc="""\
            Instances of this class are used to bind specific events to event handlers.
            """,
        items=[
            PyFunctionDef('__init__', '(self, evtType, expectedIDs=0)',
                body="""\
                    if expectedIDs not in [0, 1, 2]:
                        raise ValueError("Invalid number of expectedIDs")
                    self.expectedIDs = expectedIDs

                    if isinstance(evtType, (list, tuple)):
                        self.evtType = list(evtType)
                    else:
                        self.evtType = [evtType]
                    """),

            PyFunctionDef('Bind', '(self, target, id1, id2, function)',
                doc="""Bind this set of event types to target using its Connect() method.""",
                body="""\
                    for et in self.evtType:
                        target.Connect(id1, id2, et, function)
                    """),

            PyFunctionDef('Unbind', '(self, target, id1, id2, handler=None)',
                doc="""Remove an event binding.""",
                body="""\
                    success = 0
                    for et in self.evtType:
                        success += int(target.Disconnect(id1, id2, et, handler))
                    return success != 0
                    """),

            PyFunctionDef('_getEvtType', '(self)',
                doc="""\
                    Make it easy to get to the default wxEventType typeID for this
                    event binder.
                    """,
                body="""return self.evtType[0]"""),

            PyPropertyDef('typeId', '_getEvtType'),

            PyFunctionDef('__call__', '(self, *args)',
                deprecated="Use :meth:`EvtHandler.Bind` instead.",
                doc="""\
                    For backwards compatibility with the old ``EVT_*`` functions.
                    Should be called with either (window, func), (window, ID,
                    func) or (window, ID1, ID2, func) parameters depending on the
                    type of the event.
                    """,
                body="""\
                    assert len(args) == 2 + self.expectedIDs
                    id1 = ID_ANY
                    id2 = ID_ANY
                    target = args[0]
                    if self.expectedIDs == 0:
                        func = args[1]
                    elif self.expectedIDs == 1:
                        id1 = args[1]
                        func = args[2]
                    elif self.expectedIDs == 2:
                        id1 = args[1]
                        id2 = args[2]
                        func = args[3]
                    else:
                        raise ValueError("Unexpected number of IDs")

                    self.Bind(target, id1, id2, func)
                    """)
            ])


    module.includePyCode('src/event_ex.py')

    #---------------------------------------
    # wxEvtHandler
    c = module.find('wxEvtHandler')
    c.addPrivateCopyCtor()
    c.addPublic()

    c.includeCppCode('src/event_ex.cpp')

    # Ignore the Connect/Disconnect and Bind/Unbind methods (and all overloads) for now.
    for item in c.allItems():
        if item.name in ['Connect', 'Disconnect', 'Bind', 'Unbind']:
            item.ignore()


    # Connect and Disconnect methods for wxPython. Hold a reference to the
    # event handler function in the event table, so we can fetch it later when
    # it is time to handle the event.
    c.addCppMethod(
        'void', 'Connect', '(int id, int lastId, wxEventType eventType, PyObject* func)',
        doc="Make an entry in the dynamic event table for an event binding.",
        body="""\
            if (PyCallable_Check(func)) {
                self->Connect(id, lastId, eventType,
                              (wxObjectEventFunction)&wxPyCallback::EventThunker,
                              new wxPyCallback(func));
            }
            else if (func == Py_None) {
                self->Disconnect(id, lastId, eventType,
                                 (wxObjectEventFunction)(wxEventFunction)
                                 &wxPyCallback::EventThunker);
            }
            else {
                PyErr_SetString(PyExc_TypeError, "Expected callable object or None.");
            }
        """)


    c.addCppMethod(
        'bool', 'Disconnect', '(int id, int lastId=-1, '
                               'wxEventType eventType=wxEVT_NULL, '
                               'PyObject* func=NULL)',
        doc="Remove an event binding by removing its entry in the dynamic event table.",
        body="""\
            if (func && func != Py_None) {
                // Find the current matching binder that has this function
                // pointer and disconnect that one.  Unfortunately since we
                // wrapped the PyObject function pointer in another object we
                // have to do the searching ourselves...
                size_t cookie;
                wxDynamicEventTableEntry *entry = self->GetFirstDynamicEntry(cookie);
                while (entry)
                {
                    if ((entry->m_id == id) &&
                        ((entry->m_lastId == lastId) || (lastId == wxID_ANY)) &&
                        ((entry->m_eventType == eventType) || (eventType == wxEVT_NULL)) &&
                        entry->m_fn->IsMatching(wxObjectEventFunctor((wxObjectEventFunction)&wxPyCallback::EventThunker, NULL)) &&
                        (entry->m_callbackUserData != NULL))
                    {
                        wxPyThreadBlocker block;
                        wxPyCallback *cb = (wxPyCallback*)entry->m_callbackUserData;
                        // NOTE: Just comparing PyObject pointers is not enough, as bound
                        // methods can result in different PyObjects each time obj.Method
                        // is evaluated. (!!!)
                        if (PyObject_RichCompareBool(cb->m_func, func, Py_EQ) == 1) {
                            delete cb;
                            // Set callback data to a known value instead of NULL to
                            // ensure Disconnect() removes the correct handler.
                            entry->m_callbackUserData = new wxObject();
                            // Now Disconnect should work
                            return self->Disconnect(id, lastId, eventType,
                                                    (wxObjectEventFunction)&wxPyCallback::EventThunker,
                                                    entry->m_callbackUserData);
                        }
                    }
                    entry = self->GetNextDynamicEntry(cookie);
                }
                return false;
            }
            else {
                return self->Disconnect(id, lastId, eventType,
                                        (wxObjectEventFunction)&wxPyCallback::EventThunker);
            }
        """)


    # Ignore the C++ version of CallAfter. We have our own.
    # TODO: If we want to support this we'll need concrete implementations of
    # the template, probably using PyObject* args.
    for m in c.find('CallAfter').all():
        m.ignore()

    c.find('QueueEvent.event').transfer = True
    module.find('wxQueueEvent.event').transfer = True

    # TODO: If we don't need to use the wxEvtHandler's client data for our own
    # tracking then enable these....
    c.find('GetClientObject').ignore()
    c.find('SetClientObject').ignore()
    c.find('GetClientData').ignore()
    c.find('SetClientData').ignore()

    # We only care about overriding a few virtuals, ignore the rest.
    tools.removeVirtuals(c)
    c.find('ProcessEvent').isVirtual = True
    c.find('TryBefore').isVirtual = True
    c.find('TryAfter').isVirtual = True
    c.find('TryBefore').ignore(False)
    c.find('TryAfter').ignore(False)


    # Release the GIL for potentially blocking or long-running functions
    c.find('ProcessEvent').releaseGIL()
    c.find('ProcessEventLocally').releaseGIL()
    c.find('SafelyProcessEvent').releaseGIL()
    c.find('ProcessPendingEvents').releaseGIL()


    c.addPyMethod('Bind', '(self, event, handler, source=None, id=wx.ID_ANY, id2=wx.ID_ANY)',
        doc="""\
            Bind an event to an event handler.

            :param event: One of the ``EVT_*`` event binder objects that
                          specifies the type of event to bind.

            :param handler: A callable object to be invoked when the
                            event is delivered to self.  Pass ``None`` to
                            disconnect an event handler.

            :param source: Sometimes the event originates from a
                           different window than self, but you still
                           want to catch it in self.  (For example, a
                           button event delivered to a frame.)  By
                           passing the source of the event, the event
                           handling system is able to differentiate
                           between the same event type from different
                           controls.

            :param id: Used to spcify the event source by ID instead
                       of instance.

            :param id2: Used when it is desirable to bind a handler
                        to a range of IDs, such as with EVT_MENU_RANGE.
            """,
        body="""\
            assert isinstance(event, wx.PyEventBinder)
            assert callable(handler) or handler is None
            assert source is None or hasattr(source, 'GetId')
            if source is not None:
                id  = source.GetId()
            event.Bind(self, id, id2, handler)
            """)


    c.addPyMethod('Unbind', '(self, event, source=None, id=wx.ID_ANY, id2=wx.ID_ANY, handler=None)',
        doc="""\
            Disconnects the event handler binding for event from `self`.
            Returns ``True`` if successful.
            """,
        body="""\
            if source is not None:
                id  = source.GetId()
            return event.Unbind(self, id, id2, handler)
            """)

    module.addPyCode('PyEvtHandler = wx.deprecated(EvtHandler, "Use :class:`EvtHandler` instead.")')


    #---------------------------------------
    # wxEvent
    c = module.find('wxEvent')
    assert isinstance(c, etgtools.ClassDef)
    c.abstract = True
    c.find('Clone').factory = True

    c.find('GetEventUserData').ignore()

    c.addProperty('EventObject GetEventObject SetEventObject')
    c.addProperty('EventType GetEventType SetEventType')
    c.addProperty('Id GetId SetId')
    c.addProperty('Skipped GetSkipped')
    c.addProperty('Timestamp GetTimestamp SetTimestamp')


    #---------------------------------------
    # wxCommandEvent
    c = module.find('wxCommandEvent')

    # The [G|S]etClientData methods deal with untyped void* values, which we
    # don't support. The [G|S]etClientObject methods use wxClientData instances
    # which we have a MappedType for, so make the ClientData methods just be
    # aliases for ClientObjects. From the Python programmer's perspective they
    # would be virtually the same anyway.
    c.find('SetClientObject.clientObject').transfer = True
    c.find('SetClientObject.clientObject').name = 'data'
    c.find('GetClientData').ignore()
    c.find('SetClientData').ignore()
    c.find('GetClientObject').pyName = 'GetClientData'
    c.find('SetClientObject').pyName = 'SetClientData'
    c.addPyMethod('GetClientObject', '(self)',
        doc="Alias for :meth:`GetClientData`",
        body="return self.GetClientData()")
    c.addPyMethod('SetClientObject', '(self, data)',
        doc="Alias for :meth:`SetClientData`",
        body="self.SetClientData(data)")
    c.addPyProperty('ClientData GetClientData SetClientData')

    c.addProperty('ExtraLong GetExtraLong SetExtraLong')
    c.addProperty('Int GetInt SetInt')
    c.addProperty('Selection GetSelection')
    c.addProperty('String GetString SetString')


    #---------------------------------------
    # wxPaintEvent
    c = module.find('wxPaintEvent')
    # Although the default ctor is listed as public in the interface, it is
    # magically made private for the users of the library as it can only be
    # created within wxWidgets.
    c.find('wxPaintEvent').protection = 'private'

    #---------------------------------------
    # wxKeyEvent
    c = module.find('wxKeyEvent')

    c.find('GetPosition').findOverload('wxCoord').ignore()
    c.find('GetUnicodeKey').type = 'int'

    c.addCppMethod('void', 'SetKeyCode', '(int keyCode)',
        body="self->m_keyCode = keyCode;")

    c.addCppMethod('void', 'SetRawKeyCode', '(int rawKeyCode)',
        body="self->m_rawCode = rawKeyCode;")

    c.addCppMethod('void', 'SetRawKeyFlags', '(int rawFlags)',
        body="self->m_rawFlags = rawFlags;")

    c.addCppMethod('void', 'SetUnicodeKey', '(int uniChar)',
        body="self->m_uniChar = uniChar;")

    c.addProperty('X GetX')
    c.addProperty('Y GetY')
    c.addProperty('KeyCode GetKeyCode SetKeyCode')
    c.addProperty('Position GetPosition')
    c.addProperty('RawKeyCode GetRawKeyCode SetRawKeyCode')
    c.addProperty('RawKeyFlags GetRawKeyFlags SetRawKeyFlags')
    c.addProperty('UnicodeKey GetUnicodeKey SetUnicodeKey')

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

    c.addCppMethod('void', 'SetWheelAxis', '(wxMouseWheelAxis wheelAxis)',
        body="self->m_wheelAxis = wheelAxis;")

    c.addCppMethod('void', 'SetWheelRotation', '(int wheelRotation)',
        body="self->m_wheelRotation = wheelRotation;")

    c.addCppMethod('void', 'SetWheelDelta', '(int wheelDelta)',
        body="self->m_wheelDelta = wheelDelta;")

    c.addCppMethod('void', 'SetLinesPerAction', '(int linesPerAction)',
        body="self->m_linesPerAction = linesPerAction;")

    c.addCppMethod('void', 'SetColumnsPerAction', '(int columnsPerAction)',
        body="self->m_columnsPerAction = columnsPerAction;")

    c.addProperty('WheelAxis GetWheelAxis SetWheelAxis')
    c.addProperty('WheelRotation GetWheelRotation SetWheelRotation')
    c.addProperty('WheelDelta GetWheelDelta SetWheelDelta')
    c.addProperty('LinesPerAction GetLinesPerAction SetLinesPerAction')
    c.addProperty('ColumnsPerAction GetColumnsPerAction SetColumnsPerAction')

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
    c.find('GetShow').ignore()  # deprecated
    c.addProperty('Show IsShown SetShow')

    #---------------------------------------
    # wxDropFilesEvent
    c = module.find('wxDropFilesEvent')

    # wxDropFilesEvent assumes that the C array of wxString objects will
    # continue to live as long as the event object does, and does not take
    # ownership of the array. Unfortunately the mechanism used to turn the
    # Python list into a C array will also delete it after the API call, and
    # so when wxDropFilesEvent tries to access it later the memory pointer is
    # bad. So we'll copy that array into a special holder class and give that
    # one to the API, and also assign a Python reference to it to the event
    # object, so it will get garbage collected later.
    c.find('wxDropFilesEvent.files').array = True
    c.find('wxDropFilesEvent.files').transfer = True
    c.find('wxDropFilesEvent.noFiles').arraySize = True
    c.addHeaderCode('#include "arrayholder.h"')
    c.find('wxDropFilesEvent').setCppCode_sip("""\
        if (files) {
            wxStringCArrayHolder* holder = new wxStringCArrayHolder;
            holder->m_array = files;
            // Make a PyObject for the holder, and transfer its ownership to self.
            PyObject* pyHolder = sipConvertFromNewType(
                    (void*)holder, sipType_wxStringCArrayHolder, (PyObject*)sipSelf);
            Py_DECREF(pyHolder);
            sipCpp = new sipwxDropFilesEvent(id,(int)noFiles, holder->m_array);
        }
        else
            sipCpp = new sipwxDropFilesEvent(id);
        """)



    c.find('GetFiles').type = 'PyObject*'
    c.find('GetFiles').setCppCode("""\
        int         count   = self->GetNumberOfFiles();
        wxString*   files   = self->GetFiles();
        wxPyThreadBlocker   blocker;
        PyObject*   list    = PyList_New(count);
        if (!list) {
            PyErr_SetString(PyExc_MemoryError, "Can't allocate list of files!");
            return NULL;
        }
        for (int i=0; i<count; i++) {
            PyObject* s = wx2PyString(files[i]);
            PyList_SET_ITEM(list, i, s);
        }
        return list;
        """)

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
    # wxIconizeEvent
    c = module.find('wxIconizeEvent')
    # deprecated and removed
    c.find('Iconized').ignore()

    #---------------------------------------
    # wxThreadEvent
    c = module.find('wxThreadEvent')
    c.find('SetPayload').ignore()
    c.find('GetPayload').ignore()



    # Apply common fixups for all the event classes
    for name in [n for n in ITEMS if n.endswith('Event')]:
        c = module.find(name)
        tools.fixEventClass(c)

    #---------------------------------------
    # wxEventBlocker
    c = module.find('wxEventBlocker')
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')

    #---------------------------------------
    # wxPropagationDisabler
    c = module.find('wxPropagationDisabler')
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')
    c.addPrivateCopyCtor()

    #---------------------------------------
    # wxPropagateOnce
    c = module.find('wxPropagateOnce')
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')
    c.addPrivateCopyCtor()

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

