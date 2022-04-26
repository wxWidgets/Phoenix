#----------------------------------------------------------------------------
# Name:        wx.lib.eventwatcher
# Purpose:     A widget that allows some or all events for a particular widget
#              to be captured and displayed.
#
# Author:      Robin Dunn
#
# Created:     21-Jan-2009
# Copyright:   (c) 2009-2020 by Total Control Software
# Licence:     wxWindows license
#
# Tags:        phoenix-port
#----------------------------------------------------------------------------

"""
A widget and supporting classes for watching the events sent to some other widget.
"""

import importlib

import wx

#----------------------------------------------------------------------------
# Helpers for building the data structures used for tracking the
# various event binders that are available

_eventBinders = None
_eventIdMap = None

def _buildModuleEventMap(module):
    count = 0
    for name in dir(module):
        if name.startswith('EVT_'):
            item = getattr(module, name)
            if isinstance(item, wx.PyEventBinder) and \
               len(item.evtType) == 1 and \
               item not in _eventBinders:
                    _eventBinders.append(item)
                    _eventIdMap[item.typeId] = name
                    count += 1
    return count


def buildWxEventMap():
    """
    Add the event binders from the main wx namespace.  This is called
    automatically from the EventWatcher.
    """
    global _eventBinders
    global _eventIdMap
    if _eventBinders is None:
        _eventBinders = list()
        _eventIdMap = dict()
        _buildModuleEventMap(wx)


def addModuleEvents(module):
    """
    Adds all the items in module that start with ``EVT_`` to the event
    data structures used by the EventWatcher.
    """
    if _eventBinders is None:
        buildWxEventMap()
    return _buildModuleEventMap(module)


# Events that should not be watched by default
_noWatchList = [
    wx.EVT_PAINT,
    wx.EVT_NC_PAINT,
    wx.EVT_ERASE_BACKGROUND,
    wx.EVT_IDLE,
    wx.EVT_UPDATE_UI,
    wx.EVT_UPDATE_UI_RANGE,
    ]
OTHER_WIDTH = 250


def _makeSourceString(wdgt):
    if wdgt is None:
        return "None"
    else:
        name = ''
        id = 0
        if hasattr(wdgt, 'GetName'):
            name = wdgt.GetName()
        if hasattr(wdgt, 'GetId'):
            id = wdgt.GetId()
        return '%s "%s" (%d)' % (wdgt.__class__.__name__, name, id)

def _makeAttribString(evt):
    "Find all the getters"
    attribs = ""
    for name in dir(evt):
        if (name.startswith('Get') or name.startswith('Is')) and \
               name not in [ 'GetEventObject',
                             'GetEventType',
                             'GetId',
                             'GetSkipped',
                             'GetTimestamp',
                             'GetClientData',
                             'GetClientObject',
                             ]:
            try:
                value = getattr(evt, name)()
                attribs += "%s : %s\n" % (name, value)
            except Exception:
                pass

    return attribs.rstrip()

def cmp(a, b):
    return (a > b) - (a < b)

#----------------------------------------------------------------------------

class EventLog(wx.ListCtrl):
    """
    A virtual listctrl that displays information about the watched events.
    """
    def __init__(self, *args, **kw):
        kw['style'] = wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES
        wx.ListCtrl.__init__(self, *args, **kw)
        self.clear()

        if 'wxMac' in wx.PlatformInfo:
            self.SetWindowVariant(wx.WINDOW_VARIANT_SMALL)

        self.InsertColumn(0, "#", format=wx.LIST_FORMAT_RIGHT, width=50)
        self.InsertColumn(1, "Event", width=200)
        self.InsertColumn(2, "Source", width=200)

        self.SetMinSize((450+wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X), 450))
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onItemActivated)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onItemActivated)

    def append(self, evt):
        evtName = _eventIdMap.get(evt.GetEventType(), None)
        if evtName is None:
            evtName = 'Unknown: %d' % evt.GetEventType()
        source = _makeSourceString(evt.GetEventObject())
        attribs = _makeAttribString(evt)

        lastIsSelected = self.currItem == len(self.data)-1
        self.data.append( (evtName, source, attribs) )

        count = len(self.data)
        self.SetItemCount(count)
        self.RefreshItem(count-1)
        if lastIsSelected:
            self.Select(count-1)
            self.EnsureVisible(count-1)

    def clear(self):
        self.data = []
        self.SetItemCount(0)
        self.currItem = -1
        self.Refresh()

    def OnGetItemText(self, item, col):
        if col == 0:
            val = str(item+1)
        else:
            val = self.data[item][col-1]
        return val

    def OnGetItemAttr(self, item):  return None
    def OnGetItemImage(self, item): return -1

    def onItemSelected(self, evt):
        self.currItem = evt.GetIndex()

    def onItemActivated(self, evt):
        idx = evt.GetIndex()
        text = self.data[idx][2]
        wx.CallAfter(wx.TipWindow, self, text, OTHER_WIDTH)

#----------------------------------------------------------------------------


class EventChooser(wx.Panel):
    """
    Panel with CheckListBox for selecting which events will be watched.
    """
    def __init__(self, *args, **kw):
        wx.Panel.__init__(self, *args, **kw)
        self.updateCallback = lambda: None
        self.doUpdate = True
        self._event_name_filter = wx.SearchCtrl(self)
        self._event_name_filter.ShowCancelButton(True)
        self._event_name_filter.Bind(wx.EVT_TEXT, lambda evt: self.setWatchList(self.watchList))
        self._event_name_filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self._ClearEventFilter)
        self.lb = wx.CheckListBox(self, style=wx.LB_MULTIPLE)
        if 'wxMac' in wx.PlatformInfo:
            self.lb.SetWindowVariant(wx.WINDOW_VARIANT_SMALL)
        btn1 = wx.Button(self, -1, "All")
        btn2 = wx.Button(self, -1, "None")
        btn1.SetToolTip("Check all events")
        btn2.SetToolTip("Uncheck all events")

        self.Bind(wx.EVT_BUTTON, self.onCheckAll, btn1)
        self.Bind(wx.EVT_BUTTON, self.onUncheckAll, btn2)

        self.lb.Bind(wx.EVT_CHECKLISTBOX, self.onItemActivated)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(btn1, 0, wx.ALL, 5)
        btnSizer.Add(btn2, 0, wx.ALL, 5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._event_name_filter, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.lb, 1, wx.EXPAND)
        sizer.Add(btnSizer)
        self.SetSizer(sizer)


    def setUpdateCallback(self, func):
        self.updateCallback = func

    def setWatchList(self, watchList):
        self.doUpdate = False
        searched = self._event_name_filter.GetValue().lower()
        self.watchList = watchList

        items = []
        for index, (item, flag) in enumerate(self.watchList):
            text = _eventIdMap.get(item.typeId, "[Unknown]")
            if text.lower().find(searched) != -1:
                items.append((item, text, index, flag))
        items.sort(key=lambda k: _eventIdMap[k[0].typeId])

        self.lb.Clear()
        for position, (item, text, index, flag) in enumerate(items):
            self.lb.Insert(text, position, index)
            self.lb.Check(position, flag)
        self.doUpdate = True
        self.updateCallback()


    def onItemActivated(self, evt):
        position = evt.GetInt()
        is_checked = self.lb.IsChecked(position)
        index = self.lb.GetClientData(position)
        self.watchList[index] = (self.watchList[index][0], is_checked)
        if self.doUpdate:
            self.updateCallback()

    def checkAll(self, check):
        self.doUpdate = False
        for position in range(self.lb.GetCount()):
            self.lb.Check(position, check)
            index = self.lb.GetClientData(position)
            self.watchList[index] = (self.watchList[index][0], check)
        self.lb.Refresh()
        self.doUpdate = True
        self.updateCallback()

    def onCheckAll(self, evt):
        self.checkAll(True)

    def onUncheckAll(self, evt):
        self.checkAll(False)

    def _ClearEventFilter(self, evt):
        self._event_name_filter.SetValue("")

#----------------------------------------------------------------------------

class EventWatcher(wx.Frame):
    """
    A frame that will catch and display all events sent to some widget.
    """
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)
        self.SetTitle("EventWatcher")
        self.SetExtraStyle(wx.WS_EX_BLOCK_EVENTS)
        self._watchedWidget = None

        buildWxEventMap()
        self.buildWatchList(_noWatchList)

        # Make the widgets
        self.splitter = wx.SplitterWindow(self)
        panel = wx.Panel(self.splitter)
        self.splitter.Initialize(panel)
        self.log = EventLog(panel)
        clearBtn = wx.Button(panel, -1, "Clear")
        addBtn = wx.Button(panel, -1, "Add Module")
        watchBtn = wx.ToggleButton(panel, -1, "Watch")
        watchBtn.SetValue(True)
        selectBtn = wx.ToggleButton(panel, -1, ">>>")
        self.selectBtn = selectBtn

        clearBtn.SetToolTip("Clear the event log")
        addBtn.SetToolTip("Add the event binders in an additional package or module to the watcher")
        watchBtn.SetToolTip("Toggle the watching of events")
        selectBtn.SetToolTip("Show/hide the list of events to be logged")

        # Do the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(clearBtn, 0, wx.RIGHT, 5)
        btnSizer.Add(addBtn, 0, wx.RIGHT, 5)
        btnSizer.Add((1,1), 1)
        btnSizer.Add(watchBtn, 0, wx.RIGHT, 5)
        btnSizer.Add((1,1), 1)
        btnSizer.Add(selectBtn, 0, wx.RIGHT, 5)
        sizer.Add(self.log, 1, wx.EXPAND)
        sizer.Add(btnSizer, 0, wx.EXPAND|wx.ALL, 5)
        panel.SetSizer(sizer)
        self.Sizer = wx.BoxSizer()
        self.Sizer.Add(self.splitter, 1, wx.EXPAND)
        self.Fit()

        # Bind events
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Bind(wx.EVT_BUTTON, self.onClear, clearBtn)
        self.Bind(wx.EVT_BUTTON, self.onAddModule, addBtn)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggleWatch, watchBtn)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.onToggleSelectEvents, selectBtn)



    def watch(self, widget):
        assert self._watchedWidget is None, "Can only watch one widget at a time"
        self.SetTitle("EventWatcher for " + _makeSourceString(widget))
        for evtBinder, flag in self._watchedEvents:
            if flag:
                widget.Bind(evtBinder, self.onWatchedEvent)
        self._watchedWidget = widget


    def unwatch(self):
        self.SetTitle("EventWatcher")
        if self._watchedWidget:
            for evtBinder, flag in self._watchedEvents:
                self._watchedWidget.Unbind(evtBinder, handler=self.onWatchedEvent)
        self._watchedWidget = None


    def updateBindings(self):
        widget = self._watchedWidget
        self.unwatch()
        self.buildWatchList(_noWatchList)
        if widget:
            self.watch(widget)


    def onWatchedEvent(self, evt):
        if self:
            self.log.append(evt)
        evt.Skip()

    def buildWatchList(self, exclusions):
        # This is a list of (PyEventBinder, flag) tuples where the flag indicates
        # whether to bind that event or not. By default all execpt those in
        # the _noWatchList will be set to be watched.
        self._watchedEvents = list()
        for item in _eventBinders:
            self._watchedEvents.append( (item, item not in exclusions) )

    def onCloseWindow(self, evt):
        self.unwatch()
        evt.Skip()

    def onClear(self, evt):
        self.log.clear()

    def onAddModule(self, evt):
        try:
            dlg = wx.TextEntryDialog(
                self,
                "Enter the package or module name to be scanned for \"EVT_\" event binders.",
                "Add Module")
            if dlg.ShowModal() == wx.ID_OK:
                modname = dlg.GetValue()
                try:
                    module = importlib.import_module(modname)
                except ImportError:
                    wx.MessageBox("Unable to import \"%s\"" % modname,
                                  "Error")
                    return
                count = addModuleEvents(module)
                wx.MessageBox("%d new event binders found" % count,
                              "Success")

                # Now unwatch and re-watch so we can get the new events bound
                self.updateBindings()
        finally:
            dlg.Destroy()


    def onToggleWatch(self, evt):
        if evt.IsChecked():
            self.watch(self._unwatchedWidget)
            self._unwatchedWidget = None
        else:
            self._unwatchedWidget = self._watchedWidget
            self.unwatch()


    def onToggleSelectEvents(self, evt):
        if evt.IsChecked():
            self.selectBtn.SetLabel("<<<")
            self._selectList = EventChooser(self.splitter)
            self._selectList.setUpdateCallback(self.updateBindings)
            self._selectList.setWatchList(self._watchedEvents)

            self.SetSize(self.GetSize() + (OTHER_WIDTH,0))
            self.splitter.SplitVertically(self.splitter.GetWindow1(),
                                          self._selectList,
                                          -OTHER_WIDTH)
        else:
            self.selectBtn.SetLabel(">>>")
            sashPos = self.splitter.GetSashPosition()
            self.splitter.Unsplit()
            self._selectList.Destroy()
            cs = self.GetClientSize()
            self.SetClientSize((sashPos, cs.height))

#----------------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App(redirect=False)
    frm = wx.Frame(None, title="Test Frame")
    pnl = wx.Panel(frm)
    txt = wx.TextCtrl(pnl, -1, "text", pos=(20,20))
    btn = wx.Button(pnl, -1, "button", pos=(20,50))
    frm.Show()

    ewf=EventWatcher(frm)
    ewf.watch(frm)
    ewf.Show()

    #import wx.lib.inspection
    #wx.lib.inspection.InspectionTool().Show()

    app.MainLoop()

