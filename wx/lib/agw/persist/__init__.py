"""
Persistent objects are simply the objects which automatically save their state
when they are destroyed and restore it when they are recreated, even during
another program invocation.


.. _persistent-overview:

Persistent Object Overview
==========================

Most often, persistent objects are, in fact, persistent windows as it is especially
convenient to automatically restore the UI state when the program is restarted but
an object of any class can be made persistent. Moreover, persistence is implemented
in a non-intrusive way so that the original object class doesn't need to be modified
at all in order to add support for saving and restoring its properties.

The persistence framework involves:

* **PersistenceManager** which all persistent objects register themselves with. This class
  handles actual saving and restoring of persistent data as well as various global
  aspects of persistence, e.g. it can be used to disable restoring the saved data;
* **PersistentObject** is the base class for all persistent objects or, rather, adaptors
  for the persistent objects as this class main purpose is to provide the bridge between
  the original class -- which has no special persistence support -- and PersistenceManager;
* **PersistentHandlers** which handle different kind of saving/restoring actions depending
  on the widget kind.
  

Using Persistent Windows
========================

wxPython has built-in support for a (constantly growing) number of controls. Currently the
following classes are supported:

* wx.TopLevelWindow (and hence wx.Frame and wx.Dialog, together with their own AUI perspectives);
* wx.MenuBar, FlatMenuBar;
* AuiToolBar;
* wx.Notebook, wx.Toolbook, wx.Treebook, wx.Choicebook, AuiNotebook (together with its own AUI perspective),
  FlatNotebook, LabelBook, FlatImageBook;
* wx.CheckBox;
* wx.ListBox, wx.VListBox, wx.HtmlListBox, wx.SimpleHtmlListBox, wx.adv.EditableListBox;
* wx.ListCtrl, wx.ListView, UltimateListCtrl;
* wx.CheckListBox;
* wx.Choice, wx.ComboBox, wx.adv.OwnerDrawnComboBox;
* wx.RadioBox;
* wx.RadioButton;
* wx.ScrolledWindow, wx.lib.scrolledpanel.ScrolledPanel;
* wx.Slider, KnobCtrl;
* wx.SpinButton, wx.SpinCtrl, FloatSpin;
* wx.SplitterWindow;
* wx.TextCtrl, wx.SearchCtrl, wx.lib.expando.ExpandoTextCtrl, wx.lib.masked.Ctrl;
* wx.ToggleButton, wx.lib.buttons.GenToggleButton, wx.lib.buttons.GenBitmapToggleButton,
  wx.lib.buttons.GenBitmapTextToggleButton, SToggleButton,
  SBitmapToggleButton, SBitmapTextToggleButton;
* wx.TreeCtrl, wx.GenericDirCtrl, CustomTreeCtrl;
* HyperTreeList;
* wx.lib.calendar.CalendarCtrl, wx.adv.CalendarCtrl;
* wx.CollapsiblePane, PyCollapsiblePane;
* wx.adv.DatePickerCtrl, wx.adv.GenericDatePickerCtrl;
* wx.media.MediaCtrl;
* wx.ColourPickerCtrl, wx.lib.colourselect.ColourSelect;
* wx.FilePickerCtrl, wx.DirPickerCtrl;
* wx.FontPickerCtrl;
* wx.FileHistory;
* wx.DirDialog, wx.FileDialog;
* wx.FindReplaceDialog;
* wx.FontDialog;
* wx.ColourDialog, CubeColourDialog;
* FoldPanelBar;
* wx.SingleChoiceDialog, wx.MultiChoiceDialog;
* wx.TextEntryDialog, wx.PasswordEntryDialog.


To automatically save and restore the properties of the windows of classes listed
above you need to:

* Set a unique name for the window using `SetName()`: this step is important as the
  name is used in the configuration file and so must be unique among all windows of
  the same class;
* Call `PersistenceManager.Register(window)` at any moment after creating the window
  and then `PersistenceManager.Restore(window)` when the settings may be restored
  (which can't be always done immediately, e.g. often the window needs to be populated
  first). If settings can be restored immediately after the window creation, as is often
  the case for wx.TopLevelWindow, for example, then `PersistenceManager.RegisterAndRestore(window)`
  can be used to do both at once.
* If you want the settings for the window to be saved when your main frame is destroyed (or your app closes), simply call
  `PersistenceManager.SaveAndUnregister(window)` with no arguments.


Usage
=====

Example of using a notebook control which automatically remembers the last open page::

    import wx, os
    import wx.lib.agw.persist as PM

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "Persistent Controls Demo")

            self.book = wx.Notebook(self, wx.ID_ANY)

            # Very important step!!            
            self.book.SetName("MyBook") # Do not use the default name!!

            self.book.AddPage(wx.Panel(self.book), "Hello")
            self.book.AddPage(wx.Panel(self.book), "World")
            self.Bind(wx.EVT_CLOSE, self.OnClose)

            self._persistMgr = PM.PersistenceManager.Get()

            _configFile = os.path.join(os.getcwd(), self.book.GetName())
            self._persistMgr.SetPersistenceFile(_configFile)

            if not self._persistMgr.RegisterAndRestoreAll(self.book):
                # Nothing was restored, so choose the default page ourselves
                self.book.SetSelection(0)

        def OnClose(self, event):
            self._persistMgr.SaveAndUnregister(self.book)
            event.Skip()

    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()


.. _persistent-windows:
    
Defining Custom Persistent Windows
==================================

User-defined classes can be easily integrated with PersistenceManager. To add support
for your custom class MyWidget you just need to:

* Define a MyWidgetHandler class inheriting from `AbstractHandler`;
* Implement its `GetKind()` method returning a unique string identifying all MyWidget
  objects, typically something like "widget";
* Implement its `Save()` and `Restore()` methods to actually save and restore the widget
  settings using `PersistentObject.SaveValue()` and `PersistentObject.RestoreValue()` methods.
  
If you want to add persistence support for a class not deriving from wx.Window, you need
to derive MyPersistentWidget directly from PersistentObject and so implement its
`PersistentObject.GetName()` method too. Additionally, you must ensure that
`PersistenceManager.SaveAndUnregister()` is called when your object is destroyed as this
can be only done automatically for windows.


TODOs
=====

* Find a way to handle :class:`ToolBar` UI settings as it has been done for :class:`~lib.agw.aui.auibar.AuiToolBar`:
  current :class:`ToolBar` doesn't seem to have easy access to the underlying toolbar tools;
* Implement handler(s) for :class:`grid.Grid` for row/columns sizes (possibly adding another style
  to `PersistenceManager` as :class:`grid.Grid` sets up arrays to store individual row and column
  sizes when non-default sizes are used. The memory requirements for this could become prohibitive
  if the grid is very large);
* Find a way to properly save and restore dialog data (:class:`ColourDialog`, :class:`FontDialog` etc...);
* Add handlers for the remaining widgets not yet wrapped (mostly in :mod:`lib`).


License And Version
===================

`PersistentObjects` library is distributed under the wxPython license. 

Latest revision: Andrea Gavana @ 27 Mar 2013, 21.00 GMT
Version 0.5. 

"""

__author__ = "Andrea Gavana <andrea.gavana@gmail.com>"
__date__ = "16 November 2009"


from .persist_constants import *
from .persistencemanager import *
from .persist_handlers import *
