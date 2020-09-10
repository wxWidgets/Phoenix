# --------------------------------------------------------------------------------- #
# SHORTCUTEDITOR wxPython IMPLEMENTATION
# Inspired By the GIMP Shortcut Editor.
#
# Andrea Gavana, @ 05 March 2012
# Latest Revision: 27 Dec 2012, 21.00 GMT
#
#
# TODO List
#
# 1. Check the various IDs in the KEYMAP dictionary to try and understand if all
#    the possible shortcut combinations can be handled.
#
# 2. Verify that the current shortcut handling is working as advertised.
#
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@maerskoil.com
# andrea.gavana@gmail.com
#
# Or, Obviously, To The wxPython Mailing List!!!
#
# Tags:        phoenix-port, unittest, documented, py3-port
#
# End Of Comments
# --------------------------------------------------------------------------------- #


"""
:class:`~wx.lib.agw.shortcuteditor.ShortcutEditor` is a widget that allows the user to customize and change keyboard
shortcuts via a dialog. It can be used to edit :class:`wx.MenuItem` shortcuts or accelerators
defined in a :class:`AcceleratorTable`.

.. note::

    :class:`ShortcutEditor` **requires** the minimum AGW version 0.9.3 or the current
    SVN, for the various enhancements made to the :class:`~wx.lib.agw.hypertreelist.HyperTreeList`
    and :class:`~wx.lib.agw.genericmessagedialog.GenericMessageDialog`
    widgets.


Description
===========

:class:`ShortcutEditor` is a widget that allows the user to customize and change keyboard
shortcuts via a dialog. It can be used to edit :class:`wx.MenuItem` shortcuts or accelerators
defined in a :class:`AcceleratorTable`.

The interface itself is very much inpired by the GIMP shortcut editor:

http://graphicssoft.about.com/od/gimptutorials/tp/keyboard-shortcut-editor.htm

There are very few minor UI differences between :class:`ShortcutEditor` and the GIMP one,
although the behaviour should be pretty much equivalent.

Various features:

* Shortcuts are listed in a tree-like structure, pretty much reflecting a menu
  hierarchy (as most of the time :class:`ShortcutEditor` is used to edit :class:`wx.MenuItem`
  shortcuts);
* Accelerators defined via :class:`AcceleratorTable` are handled in a similar way;
* Support for I18N;
* Ability to restore default shortcuts/accelerators via a UI button;
* Possibility to send back the new/updated shortcuts to the original :class:`wx.MenuBar` or
  the original :class:`AcceleratorTable`;
* Filters on the shortcuts label (case-insensitive);
* Basic help window with instructions (customizable via :meth:`~ShortcutEditor.SetHTMLHelpFile`), via
  the ``Help`` button.

And a lot more. Check the demo for an almost complete review of the functionalities.


UI Interactions
===============

1. In the :class:`ShortcutEditor` dialog you can open sub-sections by clicking the small box
   with a + sign in it next to each section name. In the screen grab, you can see I've
   opened the *Options* sub-section as I'm going to add a keyboard shortcut to the
   *OptionsItem 1* item.

   .. figure:: _static/images/sphinxdocs/ShortcutEditor_1_thumb.png
      :alt: Open Subsections
      :figclass: floatcenter
      :target: _static/images/sphinxdocs/ShortcutEditor_1.png

      **Figure 1**


2. Now you need to scroll to the tool or command that you want to edit and click on it
   to select it. When selected, the text for that tool in the *Shortcut* column changes
   to read 'New accelerator...' and you can press the key or combination of keys you
   want to assign as a shortcut.

   .. figure:: _static/images/sphinxdocs/ShortcutEditor_2_thumb.png
      :alt: Assign Shortcut
      :figclass: floatcenter
      :target: _static/images/sphinxdocs/ShortcutEditor_2.png

      **Figure 2**


3. I've changed the *OptionsItem 1*'s keyboard shortcut to ``Shift+Ctrl+F`` by pressing
   the ``Shift``, ``Ctrl`` and ``F`` keys simultaneously. If you want to remove a keyboard
   shortcut from any tool or command, just click on it to select it and then when the
   'New accelerator...' text displays, press the backspace key and the text will change
   to 'Disabled'.

   Once you're happy that your keyboard shortcuts are set up as you wish, simply click
   the ``OK`` button.

   .. figure:: _static/images/sphinxdocs/ShortcutEditor_3_thumb.png
      :alt: Remove/Save Shortcuts
      :figclass: floatcenter
      :target: _static/images/sphinxdocs/ShortcutEditor_3.png

      **Figure 3**


4. If you thought my choice of ``Shift+Ctrl+F`` was an odd selection, I chose it because
   it was a keyboard combination that hadn't already been assigned to any tool or command.
   If you try to assign a keyboard shortcut that is already in use, an alert will open
   telling you what the shortcut is currently being used for. If you want to keep the
   original shortcut, just click the ``Cancel`` button, otherwise click ``Reassign shortcut``
   to make the shortcut apply to your new selection.

   .. figure:: _static/images/sphinxdocs/ShortcutEditor_4_thumb.png
      :alt: Reassigning Shortcuts
      :figclass: floatcenter
      :target: _static/images/sphinxdocs/ShortcutEditor_4.png

      **Figure 4**



Base Functionalities
====================

There are basically three ways to populate the :class:`ShortcutEditor` dialog, depending on
your needs. These approaches can be combined if needed.

1) Use the :meth:`~ShortcutEditor.FromMenuBar` method: if you need to give your user the ability to edit
   the various :class:`wx.MenuItem` shortcuts in your application, you can create :class:`ShortcutEditor`
   in this way::

        # Build your wx.MenuBar first!!!
        # "self" is an instance of wx.TopLevelWindow

        dlg = ShortcutEditor(self)
        dlg.FromMenuBar(self)

        # Here the user will make all the various modifications
        # to the shortcuts

        if dlg.ShowModal() == wx.ID_OK:
            # Changes accepted, send back the new shortcuts to
            # the TLW wx.MenuBar
            dlg.ToMenuBar(self)

        dlg.Destroy()


2) Use the :meth:`~ShortcutEditor.FromAcceleratorTable` method: if you need to give your user the ability to edit
   the various accelerators you set via :class:`AcceleratorTable` in your application, you can
   create :class:`ShortcutEditor` in this way::

        # Build your wx.AcceleratorTable first!!!
        # "accelTable" is a list of tuples (4 elements per tuple)

        accelTable = []

        # Every tuple is defined in this way:

        for label, flags, keyCode, cmdID in my_accelerators:
            # label:   the string used to show the accelerator into the ShortcutEditor dialog
            # flags:   a bitmask of wx.ACCEL_ALT, wx.ACCEL_SHIFT, wx.ACCEL_CTRL, wx.ACCEL_CMD,
            #          or wx.ACCEL_NORMAL used to specify which modifier keys are held down
            # keyCode: the keycode to be detected (i.e., ord('b'), wx.WXK_F10, etc...)
            # cmdID:   the menu or control command ID to use for the accelerator event.

            accel_tuple = (label, flags, keyCode, cmdID)
            accelTable.append(accel_tuple)

        dlg = ShortcutEditor(self)
        dlg.FromAcceleratorTable(accelTable)

        # Here the user will make all the various modifications
        # to the shortcuts

        if dlg.ShowModal() == wx.ID_OK:
            # Changes accepted, send back the new shortcuts to
            # the window with the wx.AcceleratorTable:
            dlg.ToAcceleratorTable(self)

        dlg.Destroy()


3) Build your own hierarchy of shortcuts using :meth:`~ShortcutEditor.GetShortcutManager`::

        dlg = ShortcutEditor(self)
        manager = dlg.GetShortcutManager()

        for label, accelerator, bitmap, help, cmdID in my_list:
            shortcut = Shortcut(label, accelerator, bitmap, help, accelId=cmdID)
            manager.AppendItem(shortcut)

        dlg.ShowModal()
        dlg.Destroy()


Usage
=====

Usage example::

    import wx
    import wx.lib.agw.shortcuteditor as SE

    class MyFrame(wx.Frame):

        def __init__(self, parent):

            wx.Frame.__init__(self, parent, -1, "ShortcutEditor Demo")

            bar = wx.MenuBar()
            menu = wx.Menu()

            menu.Append(101, "&Mercury", "This the text in the Statusbar")
            menu.Append(102, "&Venus", "")
            menu.Append(103, "&Earth", "You may select Earth too")
            menu.AppendSeparator()
            menu.Append(104, "&Close", "Close this frame")

            bar.Append(menu, 'File')
            self.SetMenuBar(bar)

            dlg = SE.ShortcutEditor(self)
            dlg.FromMenuBar(self)

            if dlg.ShowModal() == wx.ID_OK:
                # Changes accepted, send back the new shortcuts to the TLW wx.MenuBar
                dlg.ToMenuBar(self)

            dlg.Destroy()


    # our normal wxApp-derived class, as usual

    app = wx.App(0)

    frame = MyFrame(None)
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()



Window Styles
=============

`No particular window styles are available for this class.`


Events Processing
=================

This class processes the following events:

========================= ==================================================
Event Name                Description
========================= ==================================================
``EVT_SHORTCUT_CHANGING`` Event emitted when the user is about to change a shortcut.
``EVT_SHORTCUT_CHANGED``  Event emitted when the user has changed a shortcut.
========================= ==================================================


Supported Platforms
===================

:class:`ShortcutEditor` has been tested on the following platforms:
  * Windows (Windows Vista/7);


License And Version
===================

:class:`ShortcutEditor` is distributed under the wxPython license.

Latest Revision: Andrea Gavana @ 27 Dec 2012, 21.00 GMT

Version 0.1

.. versionadded:: 0.9.3

"""

# Version Info
__version__ = "0.1"

import wx
import os
import sys

import wx.html

import wx.lib.buttons as buttons
from wx.lib.embeddedimage import PyEmbeddedImage
from wx.lib.mixins import treemixin

# AGW stuff
from . import hypertreelist as HTL
from . import genericmessagedialog as GMD

# add support for I18N
_ = wx.GetTranslation

try:
    dirName = os.path.dirname(os.path.abspath(__file__))
except:
    dirName = os.path.dirname(os.path.abspath(sys.argv[0]))


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

DATA_DIR = os.path.join(dirName, 'data')
""" The folder where the default HTML help for :class:`ShortcutEditor` lives. """

# These commented out things need to be taken into account somehow, but I
# have no idea how to treat them and even if they could be valid accelerators

KEYMAP = {
    wx.WXK_BACK : 'Back',
    wx.WXK_TAB : 'Tab',
    wx.WXK_RETURN : 'Enter',
    wx.WXK_ESCAPE : 'Esc',
    wx.WXK_SPACE : 'Space',
    wx.WXK_DELETE : 'Delete',
    wx.WXK_START : 'Start',
    wx.WXK_CANCEL : 'Cancel',
    wx.WXK_CLEAR : 'Clear',
    wx.WXK_MENU : 'Menu',
    wx.WXK_PAUSE : 'Pause',
    wx.WXK_CAPITAL : 'Capital',

    wx.WXK_END : 'End',
    wx.WXK_HOME : 'Home',
    wx.WXK_LEFT : 'Left',
    wx.WXK_UP : 'Up',
    wx.WXK_RIGHT : 'Right',
    wx.WXK_DOWN : 'Down',
    wx.WXK_SELECT : 'Select',
    wx.WXK_PRINT : 'Print',
    wx.WXK_EXECUTE : 'Execute',
    wx.WXK_SNAPSHOT : 'Snapshot',
    wx.WXK_INSERT : 'Insert',
    wx.WXK_HELP : 'Help',
#    wx.WXK_NUMPAD0 : 'WXK_NUMPAD0',
#    wx.WXK_NUMPAD1 : 'WXK_NUMPAD1',
#    wx.WXK_NUMPAD2 : 'WXK_NUMPAD2',
#    wx.WXK_NUMPAD3 : 'WXK_NUMPAD3',
#    wx.WXK_NUMPAD4 : 'WXK_NUMPAD4',
#    wx.WXK_NUMPAD5 : 'WXK_NUMPAD5',
#    wx.WXK_NUMPAD6 : 'WXK_NUMPAD6',
#    wx.WXK_NUMPAD7 : 'WXK_NUMPAD7',
#    wx.WXK_NUMPAD8 : 'WXK_NUMPAD8',
#    wx.WXK_NUMPAD9 : 'WXK_NUMPAD9',
    wx.WXK_MULTIPLY : '*',
    wx.WXK_ADD : '+',
#    wx.WXK_SEPARATOR : 'WXK_SEPARATOR',
    wx.WXK_SUBTRACT : '-',
    wx.WXK_DECIMAL : '.',
    wx.WXK_DIVIDE : '/',
    wx.WXK_F1 : 'F1',
    wx.WXK_F2 : 'F2',
    wx.WXK_F3 : 'F3',
    wx.WXK_F4 : 'F4',
    wx.WXK_F5 : 'F5',
    wx.WXK_F6 : 'F6',
    wx.WXK_F7 : 'F7',
    wx.WXK_F8 : 'F8',
    wx.WXK_F9 : 'F9',
    wx.WXK_F10 : 'F10',
    wx.WXK_F11 : 'F11',
    wx.WXK_F12 : 'F12',
    wx.WXK_F13 : 'F13',
    wx.WXK_F14 : 'F14',
    wx.WXK_F15 : 'F15',
    wx.WXK_F16 : 'F16',
    wx.WXK_F17 : 'F17',
    wx.WXK_F18 : 'F18',
    wx.WXK_F19 : 'F19',
    wx.WXK_F20 : 'F20',
    wx.WXK_F21 : 'F21',
    wx.WXK_F22 : 'F22',
    wx.WXK_F23 : 'F23',
    wx.WXK_F24 : 'F24',
    wx.WXK_NUMLOCK : 'NumLock',
    wx.WXK_SCROLL : 'Scroll',
    wx.WXK_PAGEUP : 'PgUp',
    wx.WXK_PAGEDOWN : 'PgDn',
#    wx.WXK_NUMPAD_SPACE : 'WXK_NUMPAD_SPACE',
#    wx.WXK_NUMPAD_TAB : 'WXK_NUMPAD_TAB',
#    wx.WXK_NUMPAD_ENTER : 'WXK_NUMPAD_ENTER',
#    wx.WXK_NUMPAD_F1 : 'WXK_NUMPAD_F1',
#    wx.WXK_NUMPAD_F2 : 'WXK_NUMPAD_F2',
#    wx.WXK_NUMPAD_F3 : 'WXK_NUMPAD_F3',
#    wx.WXK_NUMPAD_F4 : 'WXK_NUMPAD_F4',
#    wx.WXK_NUMPAD_HOME : 'WXK_NUMPAD_HOME',
#    wx.WXK_NUMPAD_LEFT : 'WXK_NUMPAD_LEFT',
#    wx.WXK_NUMPAD_UP : 'WXK_NUMPAD_UP',
#    wx.WXK_NUMPAD_RIGHT : 'WXK_NUMPAD_RIGHT',
#    wx.WXK_NUMPAD_DOWN : 'WXK_NUMPAD_DOWN',
#    wx.WXK_NUMPAD_PAGEUP : 'WXK_NUMPAD_PAGEUP',
#    wx.WXK_NUMPAD_PAGEUP : 'WXK_NUMPAD_PAGEUP',
#    wx.WXK_NUMPAD_PAGEDOWN : 'WXK_NUMPAD_PAGEDOWN',
#    wx.WXK_NUMPAD_PAGEDOWN : 'WXK_NUMPAD_PAGEDOWN',
#    wx.WXK_NUMPAD_END : 'WXK_NUMPAD_END',
#    wx.WXK_NUMPAD_BEGIN : 'WXK_NUMPAD_BEGIN',
#    wx.WXK_NUMPAD_INSERT : 'WXK_NUMPAD_INSERT',
#    wx.WXK_NUMPAD_DELETE : 'WXK_NUMPAD_DELETE',
#    wx.WXK_NUMPAD_EQUAL : 'WXK_NUMPAD_EQUAL',
#    wx.WXK_NUMPAD_MULTIPLY : 'WXK_NUMPAD_MULTIPLY',
#    wx.WXK_NUMPAD_ADD : 'WXK_NUMPAD_ADD',
#    wx.WXK_NUMPAD_SEPARATOR : 'WXK_NUMPAD_SEPARATOR',
#    wx.WXK_NUMPAD_SUBTRACT : 'WXK_NUMPAD_SUBTRACT',
#    wx.WXK_NUMPAD_DECIMAL : 'WXK_NUMPAD_DECIMAL',
#    wx.WXK_NUMPAD_DIVIDE : 'WXK_NUMPAD_DIVIDE',
#
#    wx.WXK_WINDOWS_LEFT : 'WXK_WINDOWS_LEFT',
#    wx.WXK_WINDOWS_RIGHT : 'WXK_WINDOWS_RIGHT',
#    wx.WXK_WINDOWS_MENU : 'WXK_WINDOWS_MENU',

#    wx.WXK_SPECIAL1 : 'WXK_SPECIAL1',
#    wx.WXK_SPECIAL2 : 'WXK_SPECIAL2',
#    wx.WXK_SPECIAL3 : 'WXK_SPECIAL3',
#    wx.WXK_SPECIAL4 : 'WXK_SPECIAL4',
#    wx.WXK_SPECIAL5 : 'WXK_SPECIAL5',
#    wx.WXK_SPECIAL6 : 'WXK_SPECIAL6',
#    wx.WXK_SPECIAL7 : 'WXK_SPECIAL7',
#    wx.WXK_SPECIAL8 : 'WXK_SPECIAL8',
#    wx.WXK_SPECIAL9 : 'WXK_SPECIAL9',
#    wx.WXK_SPECIAL10 : 'WXK_SPECIAL10',
#    wx.WXK_SPECIAL11 : 'WXK_SPECIAL11',
#    wx.WXK_SPECIAL12 : 'WXK_SPECIAL12',
#    wx.WXK_SPECIAL13 : 'WXK_SPECIAL13',
#    wx.WXK_SPECIAL14 : 'WXK_SPECIAL14',
#    wx.WXK_SPECIAL15 : 'WXK_SPECIAL15',
#    wx.WXK_SPECIAL16 : 'WXK_SPECIAL16',
#    wx.WXK_SPECIAL17 : 'WXK_SPECIAL17',
#    wx.WXK_SPECIAL18 : 'WXK_SPECIAL18',
#    wx.WXK_SPECIAL19 : 'WXK_SPECIAL19',
#    wx.WXK_SPECIAL2 : 'WXK_SPECIAL2',
}

# Define a dictionary to hold the correspondence between wx.ACCEL_* and
# human-readable names
ACCELERATORS = {wx.ACCEL_ALT   : 'Alt',
                wx.ACCEL_CTRL  : 'Ctrl',
                wx.ACCEL_NORMAL: '',
                wx.ACCEL_SHIFT : 'Shift'}

# Define a dictionary to hold the correspondence between wx.MOD_* and
# human-readable names (platform dependent)
if wx.Platform == '__WXMAC__':
    MODIFIERS = [(wx.MOD_CONTROL, 'Cmd'), (wx.MOD_ALT, 'Alt'), (wx.MOD_SHIFT, 'Shift'), (wx.MOD_META, 'Meta')]
else:
    MODIFIERS = [(wx.MOD_CONTROL, 'Ctrl'), (wx.MOD_ALT, 'Alt'), (wx.MOD_SHIFT, 'Shift'), (wx.MOD_WIN, 'Win')]

# Define a couple of standard, default accelerators
NEW_ACCEL_STRING = _('New accelerator...')
""" The string to display when the user wants to enter a new accelerator (by default is `New accelerator...`). """
DISABLED_STRING = _('Disabled')
""" The string to display when an accelerator is disabled (by default is `Disabled`). """

# Events handled by ShortcutEditor
wxEVT_SHORTCUT_CHANGING = wx.NewEventType()
wxEVT_SHORTCUT_CHANGED = wx.NewEventType()

EVT_SHORTCUT_CHANGING = wx.PyEventBinder(wxEVT_SHORTCUT_CHANGING, 1)
""" Event emitted when the user is about to change a shortcut. """
EVT_SHORTCUT_CHANGED = wx.PyEventBinder(wxEVT_SHORTCUT_CHANGED, 1)
""" Event emitted when the user has changed a shortcut. """


# Standard images for all the buttons we use in the dialog
#----------------------------------------------------------------------
_cancel = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAAK/INwWK6QAAABl0"
    "RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAQQSURBVHjaAEEAvv8BXTIyAAL9"
    "/UEy6Oip+fn5BqAAAHX1/f2bBP7+ACMDAwA4BQUAB/z8AAH6+hQhCQm7FAsLKpPm5qfh/f1g"
    "4QAAAAIAQQC+/wMtGBhBLufnr1w5ORI1JycI+traR9QBAev4/v7NFQICABsDAwAB/PwUFwAA"
    "vDdJSTA0X18DIujoL9Lm5iLZAACyAgBBAL7/A2ADA8xhKSkREoaGAAQ9PQAm398DAeDgRtP/"
    "/+gKAgLOHQEBDBr//782NDQwIGpqAP84OAAgFBQBKOXlLr3n5wcCAEEAvv8E9fn5CAcBAQD5"
    "3NwA+A8PAA5aWgBY+PgG/cjIlMcCAhUUAQFSMScnMB1VVQD/AAAA99HRAAj4+AAFBQUBAf//"
    "NAKI+TEf36uvT5546N+4wczMxcXwE2gYu6Qkg8T79yxCb986KUtKSiu7ujKwAA3/9ewZA/fN"
    "mwxX1q5lyD979sXZ//9LAAKImZeL69w5oJ//v37tqvP4MQsj0IA/wEBjBWrg+fmTUVRZmYGD"
    "lxesmePpU4Zbx44xFF269OLQ379xQAftBgggZgFOToYvf/+ePcPA8ILl0yc35RcvWP79+sXA"
    "9PMnAxc3NwML0LA/L14w/H79muHarVsM5TduvDj6928UUPNeIGYACCBmbXFxBkFgVPEwM597"
    "xcn5W/DXLxexp08Zf338yPDn/XuGX0CNPz5/ZvgGNLD93r13R37/DhBkYDjMA9QMChOAAGLR"
    "FBEBpQOG/3/+8Mn+/Bmi8OkT40eg5ncfPjB8BXqHhZ2dgRvoHVFRUQYvMTHuN48fa/xgYDjG"
    "C9R8H4gBAohZDxhgP///55H68eOg34sXxmJAze+BEh/+/2f4DqT/sLAwsAK9ycbGxmAhJcUi"
    "yczscfrDh9dAQ85+BcoDBBCztoyMpMz37/vCnjwxkAY69QNQ8BsQswI18EtIMHACaRBgBbqE"
    "CYiNZGRYRP//d738/v3rF0BDAAKI2U9A4EjMw4f6il+/MnwEKvwJxCBNT4SFGab/+PGem42N"
    "WY+bm/kvMFWyAMWZga4xVVBgkfj3z23f27cPAQKISebzZ21toOa/QI3/gJgfGKCPgZq7v317"
    "sfPdO7+Fr19nnv/585cIUCMTKMEBY4UFmF7M5eTYBJmZkwACiPk1F5cCPyengTYwzlmBtpwG"
    "aq7//v3F+Y8fo9gYGQ+xMzCcv/7ly0sxFhY3HSEhFkFgmvgEjJ2ms2d/7Pz6dSpAADHIAkNX"
    "R1x80SoxsX+bxMX/6/HzPwc6xBnkbw6gjWpAF6kDaUNGxoxFSko/7lpY/E/n5//ByMBQAlID"
    "EEAMqmJiDNJAWxX4+dsluLh2A8XcGKAAZoA+MEdqAvn6jIwx+iwse5kZGAphagACDAAeLHBa"
    "S9SUbwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_clear = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAA"
    "B3RJTUUH1wYeFCULmGdR+AAAAnpJREFUOI2V0ktIVFEcBvDv3jveufO4jk46ZVlGNUGRLTIp"
    "K8OCoAdBIM2ioo2LCKFsI7QJCQoiiJ60nCDBTbUpsJSh0cxw42DImA2j1vhImXFmvPM493VO"
    "izDS6WFn/X0/+H8cDv/xHpyzXuYs/FVdVT2iVbre/CTXxq+0fP+M9ZLNId/YVd+4+tTZFo5o"
    "rBUAVgQ8PI9VsOBmTf1JR3+wE18igyCcHAUAy0oAysSLFeuqBJFMoW7nerwZ+JzLGFLLP4FP"
    "70r7KOOeBzqMZpeYl+KxEPqiYlbVhHt3XnwN/PUEf5tfMg3Lfrmk+tYhn3VNWXUeUYXXFogQ"
    "GhNi1xZzwp+AxiN7H01EjtaoxCt4KmvhLMvA6priqzaTjrxFDQSDYADALS+Ov4WkWzxPDWY7"
    "np4/IY0Ob+RHQgrc5QnsafgIQx+CrqH1WJNyuwCI9DrLqeAI2GXvlrVVp22MmdDyMYyPJvDM"
    "TxEJ21HXMNBeXjvU5PNBWwJEu0tdpk18L5ft9pa4a0ShSIapzUGZHwEvZKCTafR2ZzXOmfP4"
    "LiTTiz0eAGL9lTbDLnY53dWbZNd2MZuegKnHoeYnkVuIQVdnoKszcDhTBVvxAJCj2iuH7N3h"
    "kLfapsdewlFcAY1MITU7AmokoaSmAVDoKoDkbwBK1cOi6LZPjLbD6fJCV2cQDfeAZGdBzSSS"
    "CQrGAMPgeJBkvgAAuIZvk0HoGiBKEsKhTj0VT4IaC+AFA/E5DprKATzSvrYf4y0Bth1M9RDT"
    "soHSosfhwdcsq5AiajBqmgbyhEdGARJxRnmOdS/foOAfAECXv9hrmuwuIeyApqL4Z5jn9vmu"
    "KB9+zX4H1k8cy/juDWsAAAAASUVORK5CYII=")

#----------------------------------------------------------------------
_default = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlw"
    "SFlzAAAK8AAACvABQqw0mAAAACV0RVh0U29mdHdhcmUATWFjcm9tZWRpYSBGaXJld29ya3Mg"
    "TVggMjAwNId2rM8AAAAWdEVYdENyZWF0aW9uIFRpbWUAMDIvMTEvMDeS+i0/AAACvklEQVR4"
    "nKWSXUjVdxjHP7/f/+W8qdPqj5rRPAsryDM2FIRBjEQotjuHsV2NCIPqoqju6iqnuYu9ZKtw"
    "N7mKujGqDXQ3o9UQEsl8mYl1OGp5lDRt5+h5+Z/j///rIgVfops98MDDw/N8+D4vQinF/zG5"
    "NtHU2LDn8qWL1StS1q329khj43dPZ1/P578X8Mfvdw/W1Oy9Mzo21l5bW1vjy/XKCy0tZ4LB"
    "YHBudq6s/uC3x9YCdADchIUMzHR13du/9cOyvEgkAspp7uvpMzs7/wz9dP5nno2GldBFIWAA"
    "2dUKhMoODju1wZ11u65fu0o0GnW2lIbse38/CMXiMR739rF722fcbrr5iZ1JhFYqEG+XOCR+"
    "aStr/W/erNfFDAG/oYpzXtrXrh7x9j4b52T5VxyvPMHAZA+bzlZt3Fxgza0egV0qmcy+TsRB"
    "ahYTzxFf11327jtXxmSsku0l20hfuE9qmnSgwFp1tqUl9oFAahKkAE1X2Il5csxpthdPwNg/"
    "QAqh68IF8Q5AaY6hu7arKaQXhAZCGiB1cAS4BkJqCEN6AmQ3rb8CnhJpZ/qHHjrkF9r4/Dmg"
    "ZcFYAkhBMp3GNfMepTHC5nqAb2TqZWJrMu4wM5lkYTHKSO4gRVUpKC1CMwMMd00ytUNMV4H7"
    "DgWQXURJAZqhkcnAq5EIsdlpjKJxuiMbyA7v58nGoY/vHD5QveWDwti55ubHgLv8SNLjdV3d"
    "cFhcANcRxFIJpN+DtpDgxWiaT/MsOu9fKentCv+lS42Ojo6m/oGB08uv/NGhA/qjyqr5b8pD"
    "dnd+QZxcv4lKJzGERkxPcjLRwr/OKHbaxvR4lGVZDwFQSi15dDk2w2MTX6Qe/Ppj+PsvpzIN"
    "5W5zdZ5Cw/X5fcmKiorrbW2/7VjuWwFY73GlyrP9N9pbT9WNf16z94emxoaja2veALFzTWMO"
    "z/GRAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
_help = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC+ElEQVR4nGWTP2xbVRjFf9+9"
    "9/01TgwJCQkMbkMKqCkEKGoXBpiQEqkpZUL8y8BeRqYwMMBQRMWMGtQgJCSKYWCohARIVCCo"
    "MJUgLbSipVERTuzYcexn+713L4OlirafdLZzznC+c4TbbnZxrSTIEkoeQ9S8iICob0WkevHM"
    "C5Xb+XKLeOH08WIxXnloZqoUhSFRFDHIcmr1XerNDts7navWuTfWPz1SucNgduH0qfm58mt7"
    "y/ezfq1LrZmR2SHFaAg9QTtLo1WnnybLv3+yuHrTYHZh7a1DT8ysFEfH+eVyh73TEa8vTvL0"
    "o0WsdXzz6w6nzm5x5cYALdDtNMgG3aO/ffxcRWYX18pTE6W/Dj7+CN9daDM17lN5+2GsteS5"
    "w1qLc44b9ZSXTlxHRHDOkrRqTWvzPXp837GVw0/OHl7fyOiljt2eJQ4U9VbGiTM1HLBn0iP2"
    "hR8v92n1QGmNaB3m6eCS8QNvSZmI7XYXRECED76skTshs6C18OyBGOccm7uOTjrMLNQRottH"
    "zOhIoVxrpsM0BPqpo9vJEa15YMLnzWNjWGs590efRg/8yABQUJB0dclYB71BjnWwvZORI3i+"
    "RnuKd16ZIA6EK/9mnPy6QxB7KDV8XDFw1BsGM0hzBMfmdooTwfgKZRQLB+9iZtJgrePD7xNS"
    "ZQgChdIKgJGCRZRGdZJBpd1OsM4hSlB6iKl7DM45nHNc2nQEoSGIPMLYY2TEIwxAtKkaRH3R"
    "au8uFcNRulZQaojKzwn7pn22EjC+xgs0fuhhfE15DP5cbyFKf6Qufvb8atJPqpHOMQKIIEo4"
    "+lTMoRmfhTmfuWmD9jReqJm+10ORs/FPv3L+/QNVBeBwy4O01QzE3uz2hesp3QFs7MDfTYdR"
    "cN+oUPIyzv3QqIrSy7dsYf+LX82jzOe5GS3rsEgcGeKCR6FouLvkMVYybDV6XNtIqoNMnvnp"
    "3Qebd6xx7uWzJZQ6Ltp71XhBOS7EhJEhzS27SV4VbU6ef2//6v81/wH6bjI8fK9HXAAAAABJ"
    "RU5ErkJggg==")

#----------------------------------------------------------------------
_info = PyEmbeddedImage(
    "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")

#----------------------------------------------------------------------
_ok = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAANkE3LLaAgAAAjpJ"
    "REFUeJy90k1IkwEcx/Hvs2evMt1KJ741Wy0zexMy0US6WHSKgii8pAUZKUEFubSgkjKRQgT1"
    "kL0hZNChMpJCi/RQGQll0sBE09wWw5c2c5rbs+fptIgutQ59758//8MP/nNCcsWSm5ajS+8C"
    "6qh1con5So+3W3ni6lTiS81XAe1f45QDsXV3JloVT2BC8c57lGZng6LZJVz8+Ub8fpVD0Mri"
    "1DVqf8dpZYYLZ6pOOjJi1jDqHyIoS7xwdyMbla1qANNO7fHDx0rrZPV3WufbpOl26iM4/Yju"
    "XEXlwdNWvZ3xuY9IssKDT23c6+0l3McjUVfEoe2Vm5vyEwuJ1yVgyRO3jflHfIFBXtvK1dUl"
    "jt016ZpM/MFJZiUfTyfbed7/Ct9t6hmiRkzeR2Moddo6G5xBJYZJjEkiMUcoIvtrzo7iLeUp"
    "Ohu+oJcpycPA3DPefXiP6zoN0gAOQBYRyLRslAqmtS7coSF8iguNQVFZs0yrtYIGb2iE0eBb"
    "3OFBvMMzOBuk2oV+qgAZQFz8zMvwPGkrc3XZQlyIb4KfsNqPUYhFL6pRqWQMOjULEwJ9l3yX"
    "Z/uojmAAEQgFhukKLsq2rLyE9XqTiiTtMuwxWaQb7Cw3ZjDjCtBx1tk41SNX/oojBwBCfidd"
    "QUlalVtgX5tqsmHVrWCdKZfxL2M0nXrY4nksnQDCf9pL3IZy/f1m917ljXxD6fCeV+zF2ugW"
    "B5gLHcbOFtceZVOZ4RagjwZHSrLkUwHE/guOqh90ld9+870vDgAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
_reassign = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9i"
    "ZSBJbWFnZVJlYWR5ccllPAAAAsZJREFUeNqck1lIVGEUx393thaXCm0qtdJrm4FlONGkWESb"
    "tthDUA9F9dDyFhTRghI9WJpgPgSBD/UWQRvZrg6CSFk5FuJDD+nYTFCmmaDV2Cz3dr7LBEIv"
    "0oE/937nfP/DOed/Pm1XPZMyU2AYNBom5TYNzWYDTXw2KyhRCVjff4iJWDwOv2OU1+5tYDyK"
    "qc7qui1u8EACpnJGYtyVsxVQUP8Zs3QzHMH8JfDq0Nl3jIrycyqZKRWhldZiXt1XQSQeo6PP"
    "j/9jP6HhgKbKm5+mmx5dx5tbKFVoAged/VXYpe7Zyfu45ruJQ93sDF4kHAXvovOkp6zmec9t"
    "q5kdBfvJmeugI3AeK6Mq2SGQBCPhkHW2L97IoXchZqYmwc9oG0vmFZAydSHBbwE2r9LpDF0i"
    "OAhdfeAUonuWkH/o3HvVTdNpPPZeH74+Hzdc+ZTNSGbGOG/IdS9jqtPNrVfXZdzwoptg40k2"
    "TVnF0bSZTlreDtN8Bk95PV12kXFo6Va+PDtDiy2fw0nTscftPeS4c0hx5fL4dW+ktZL1O+vo"
    "joYpDQ4ZWU2KfIUu1ZZNNdt4wmRzNfcPbNzuGh7RCQxA/+gTFmT8ZE9JkUtidx6elJtOvHUH"
    "G9hUjf+vWjYjTuuWGs3cXVK8OCtzjOKiAP2SIPgVPofbUb7t3uV5G6o0c+1KGfiQyLhHZIwm"
    "ZCy7jHn8QB7x2DSGwm8JfYIvId2a8NzMANlZkOpaRMwYs6Qc+z2AbCJuh8j4SGRU+zhivCcm"
    "9QQ/w8sOBpsrA9tUgi0XeSJDnKNn92IkFktLyPg9IaNWWoVfc1GoVjYe5nXLBY7IYHuwZkN+"
    "WQ2twktX5OI1IHvFyIDO07YAzWfxqPVYIkhJrP6okD9MfAuSZAVqfGLSrn9diYu29gjPEzJq"
    "k32NysZHaXUmseHxKTzC6+I/LFdQONHxR4ABANuzKntCBWfVAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------

_html_back = PyEmbeddedImage(
    "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")

#----------------------------------------------------------------------
_html_forward = PyEmbeddedImage(
    "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"
    "AAgwANtDcqAqYx6xAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
_html_home = PyEmbeddedImage(
    "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")

#----------------------------------------------------------------------
_html_print = PyEmbeddedImage(
    "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"
    "rkJggg==")

#----------------------------------------------------------------------
_html_reload = PyEmbeddedImage(
    "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"
    "XnDxjsZXyQAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------

def FontFromFont(font):
    """
    Creates a copy of the input `font`.

    :param `font`: an instance of :class:`wx.Font`.
    """

    new_font = wx.Font(font.GetPointSize(), font.GetFamily(), font.GetStyle(),
                       font.GetWeight(), font.GetUnderlined(),
                       font.GetFaceName(), font.GetEncoding())

    return new_font


# ----------------------------------------------------------------------------
# HTMLHelpWindow is a frame containing the HTML help page for ShortcutEditor
# ----------------------------------------------------------------------------

class HTMLHelpWindow(wx.Frame):
    """
    A simple :class:`wx.Frame` container for the basic help provided to :class:`ShortcutEditor`.
    The help page is actually straightly derived from:

    http://graphicssoft.about.com/od/gimptutorials/tp/keyboard-shortcut-editor.htm
    """

    def __init__(self, parent, htmlFile):
        """
        Default class constructor.

        :param `parent`: an instance of :class:`ShortcutEditor`;
        :param string `htmlFile`: a valid HTML file containing either the default help
         or your particular definition of help.
        """

        wx.Frame.__init__(self, parent, title=_('Configure Keyboard Shortcuts Help'))

        self.htmlFile = htmlFile

        toolbar = self.CreateToolBar(wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_TEXT)
        self.BuildToolBar(toolbar)

        self.html = wx.html.HtmlWindow(self, style=wx.SUNKEN_BORDER)
        self.printer = wx.html.HtmlEasyPrinting()

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.html, 1, wx.EXPAND)

        self.SetSizer(box)
        self.SetAutoLayout(True)

        self.SetIcon(parent.GetIcon())
        self.CreateStatusBar()

        xvideo = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        yvideo = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        self.SetSize((xvideo/2, yvideo/2))

        self.html.LoadFile(self.htmlFile)
        self.Show()


    def BuildToolBar(self, toolbar):
        """
        Creates a toolbar for :class:`HTMLHelpWindow` containing the standard browsing
        buttons like `Back`, `Forward`, `Home`, `Refresh` and `Print`.

        :param `toolbar`: an instance of :class:`ToolBar`.
        """

        w, h = _html_reload.GetBitmap().GetWidth(), _html_reload.GetBitmap().GetHeight()
        toolbar.SetToolBitmapSize((w, h))

        toolbar.AddTool(wx.ID_BACKWARD, _('Back'), _html_back.GetBitmap(), wx.NullBitmap, shortHelpString=_('Back'),
                        longHelpString=_('Go to the previous page'))

        toolbar.AddTool(wx.ID_FORWARD, _('Forward'), _html_forward.GetBitmap(), wx.NullBitmap, shortHelpString=_('Forward'),
                        longHelpString=_('Go to the next page'))

        toolbar.AddSeparator()

        toolbar.AddTool(wx.ID_HOME, _('Home'), _html_home.GetBitmap(), wx.NullBitmap, shortHelpString=_('Home Page'),
                        longHelpString=_('Go to the home page'))

        toolbar.AddTool(wx.ID_REFRESH, _('Refresh'), _html_reload.GetBitmap(), wx.NullBitmap, shortHelpString=_('Refresh'),
                        longHelpString=_('Refresh the current page'))

        toolbar.AddSeparator()
        toolbar.AddStretchableSpace()

        toolbar.AddTool(wx.ID_PRINT, _('Print'), _html_print.GetBitmap(), wx.NullBitmap, shortHelpString=_('Print'),
                        longHelpString=_('Print the current page'))

        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.OnHTMLToolbar)
        self.Bind(wx.EVT_UPDATE_UI, self.OnUpdateUI)
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def OnHTMLToolbar(self, event):
        """
        Handles all the ``wx.EVT_TOOL`` events for :class:`HTMLHelpWindow`.

        :param `event`: an instance of :class:`CommandEvent`.
        """

        evId = event.GetId()

        if evId == wx.ID_BACKWARD:
            self.html.HistoryBack()
        elif evId == wx.ID_FORWARD:
            self.html.HistoryForward()
        elif evId == wx.ID_HOME:
            self.html.LoadFile(self.htmlFile)
        elif evId == wx.ID_REFRESH:
            self.html.LoadPage(self.html.GetOpenedPage())
        elif evId == wx.ID_PRINT:
            self.printer.GetPrintData().SetPaperId(wx.PAPER_LETTER)
            self.printer.PrintFile(self.html.GetOpenedPage())
        else:
            raise Exception('Invalid toolbar item in HTMLHelpWindow')


    def OnUpdateUI(self, event):
        """
        Handles all the ``wx.EVT_UPDATE_UI`` events for :class:`HTMLHelpWindow`.

        :param `event`: an instance of :class:`UpdateUIEvent`.
        """

        evId = event.GetId()

        if evId == wx.ID_BACKWARD:
            event.Enable(self.html.HistoryCanBack())
        elif evId == wx.ID_FORWARD:
            event.Enable(self.html.HistoryCanForward())
        else:
            event.Skip()


    def OnClose(self, event):
        """
        Handles the ``wx.EVT_CLOSE`` event for :class:`HTMLHelpWindow`.

        :param `event`: an instance of :class:`CloseEvent`.
        """

        parent = self.GetParent()
        self.Destroy()

        parent.htmlWindow = None
        event.Skip()


# ----------------------------------------------------------------------------
# ShortcutEvent is a special subclassing of wx.PyCommandEvent
# ----------------------------------------------------------------------------

class ShortcutEvent(wx.PyCommandEvent):
    """
    :class:`ShortcutEvent` is a special subclassing of :class:`PyCommandEvent`.

    This event gets emitted when the user is about to change a shortcut (via ``EVT_SHORTCUT_CHANGING``)
    and when the user has changed a shortcut (via ``EVT_SHORTCUT_CHANGED``).
    """

    def __init__(self, evtType, evtId, **kwargs):
        """
        Default class constructor.
        For internal use: do not call it in your code!

        :param integer `evtType`: the event type;
        :param integer `evtId`: the event identifier.
        """

        wx.PyCommandEvent.__init__(self, evtType, evtId, **kwargs)


    def GetAccelerator(self):
        """
        Gets the shortcut string for which the operation was performed for ``EVT_SHORTCUT_CHANGED``
        and ``EVT_SHORTCUT_CHANGING`` events.

        :return: A string representing the new shortcut string (accelerator).
        """

        return self.accelerator


    def SetAccelerator(self, accelerator):
        """
        Sets the shortcut string for which the operation was performed for ``EVT_SHORTCUT_CHANGED``
        and ``EVT_SHORTCUT_CHANGING`` events.

        :param string `accelerator`: a string representing the new shortcut string (accelerator).
        """

        self.accelerator = accelerator


    def GetOldAccelerator(self):
        """
        Returns the previous shortcut string for ``EVT_SHORTCUT_CHANGED`` and
        ``EVT_SHORTCUT_CHANGING`` events.

        :return: A string representing the old shortcut string (accelerator).
        """

        return self.oldAccelerator


    def SetOldAccelerator(self, accelerator):
        """
        Sets the previous shortcut string for ``EVT_SHORTCUT_CHANGED`` and
        ``EVT_SHORTCUT_CHANGING`` events.

        :param string `accelerator`: a string representing the old shortcut string (accelerator).
        """

        self.oldAccelerator = accelerator


    def SetShortcut(self, shortcut):
        """
        Sets the shortcut class used for ``EVT_SHORTCUT_CHANGED`` and
        ``EVT_SHORTCUT_CHANGING`` events.

        :param `shortcut`: an instance of :class:`Shortcut`.
        """

        self.shortcut = shortcut
        self.accelerator = shortcut.accelerator


    def GetShortcut(self):
        """
        Returns the shortcut class used for ``EVT_SHORTCUT_CHANGED`` and
        ``EVT_SHORTCUT_CHANGING`` events.

        :return: An instance of :class:`Shortcut`.
        """

        return self.shortcut


# ----------------------------------------------------------------------------
# Shortcut is a class containing the details for a shortcut, whether from
# a menu item, an accelerator or a user-defined shortcut. It behaves like
# a tree, with children and parents.
# ----------------------------------------------------------------------------

class Shortcut(object):
    """
    :class:`Shortcut` is a class containing the details for a shortcut, whether from
    a menu item, an accelerator or a user-defined shortcut. It behaves like
    a tree, with children and parents.
    """

    def __init__(self, label='', accelerator='', bitmap=wx.NullBitmap, help='',
                 menuItem=None, accelId=None):
        """
        Default class constructor.

        :param string `label`: the shortcut label string;
        :param string `accelerator`: the shortcut accelerator string;
        :param `bitmap`: an instance of :class:`wx.Bitmap`, to display along the shortcut `label`
         in the interface tree;
        :param string `help`: the help string for this shortcut, to display in the interface tree;
        :param `menuItem`: if this :class:`Shortcut` is derived from a :class:`wx.MenuItem`, the :class:`wx.MenuItem`
         to which it should be associated;
        :param integer `accelId`: if this :class:`Shortcut` is derived from an accelerator in a :class:`AcceleratorTable`
         or from a custom, developer-defined shortcut, it represents the ID it is associated with.
        """

        self.label = label
        self.accelerator = accelerator
        self.bitmap = bitmap
        self.help = help
        self.menuItem = menuItem
        self.accelId = accelId

        self.parent = None
        self.topMenu = False
        self.imageIndex = -1
        self.changed = False
        self.shown = True
        self.position = None

        self.originalAccelerator = accelerator
        self.children = []


    def AppendItem(self, item):
        """
        Appends a :class:`Shortcut` item as a last child of its parent.

        :param `item`: an instance of :class:`Shortcut`.
        """

        item.parent = self
        self.children.append(item)


    def GetAccelerator(self):
        """ Returns the string accelerator associated with this shortcut. """

        return self.accelerator


    def SetAccelerator(self, accelerator):
        """
        Sets the string accelerator associated with this shortcut.

        :param string `accelerator`: a string representing the shortcut string (accelerator).
        """

        self.accelerator = accelerator
        self.changed = False

        if self.originalAccelerator != accelerator:
            self.changed = True


    def HasChanged(self):
        """
        Returns ``True`` if the current accelerator associated with this :class:`Shortcut` is
        different from the original one, ``False`` otherwise.
        """

        return self.changed


    def GetBitmap(self):
        """
        Returns the bitmap associated with this :class:`Shortcut`.

        :note: You should always check if the returned bitmap is a valid one or not::

            bitmap = shortcut.GetBitmap()
            if bitmap.IsOk():
                DoSomething()


         as the default bitmap associated with a :class:`Shortcut` is :class:`NullBitmap`.
        """

        return self.bitmap


    def SetBitmap(self, bitmap):
        """
        Sets the bitmap associated with this :class:`Shortcut`.

        :param `bitmap`: an instance of :class:`wx.Bitmap` (can be invalid, i.e., :class:`NullBitmap`).
        """

        self.bitmap = bitmap


    def GetLabel(self):
        """ Returns the string label associated with this shortcut. """

        return self.label


    def IsTop(self):
        """
        Returns ``True`` if this :class:`Shortcut` is associated with a top-level :class:`wx.Menu`,
        (i.e., in the top :class:`wx.MenuBar` level), ``False`` otherwise.
        """

        return self.topMenu


    def GetFirstChild(self, item):
        """
        Returns this :class:`Shortcut`'s first child and an integer value 'cookie'.
        Call :meth:`~Shortcut.GetNextChild` for the next child using this very 'cookie' return
        value as an input.

        :param `item`: an instance of :class:`Shortcut`.

        :return: A tuple with the first value being an instance of :class:`Shortcut` or ``None`` if there are no
         further children, and as second value an integer parameter 'cookie'.

        :note: This method returns ``None`` if there are no further children.
        """

        cookie = 0
        return self.GetNextChild(item, cookie)


    def GetNextChild(self, item, cookie):
        """
        Returns this :class:`Shortcut`'s next child.

        :param `item`: an instance of :class:`Shortcut`;
        :param integer `cookie`: a parameter which is opaque for the application but is necessary
         for the library to make this function reentrant (i.e. allow more than one
         enumeration on one and the same object simultaneously).

        :return: A tuple with the first value being an instance of :class:`Shortcut` or ``None`` if there are no
         further children, and as second value an integer parameter 'cookie'.

        :note: This method returns ``None`` if there are no further children.
        """

        children = item.children
        if cookie < len(children):
            return children[cookie], cookie + 1

        return None, cookie


    def GetImageIndex(self):
        """ Returns an integer index to be used in the :class:`ListShortcut` own :class:`wx.ImageList`. """

        return self.imageIndex


    def CheckAccelerator(self, item, shortcut, accelerator):
        """
        Checks if a shortcut string entered by the user has already been taken by another entry
        in the :class:`Shortcut` hierarchy.

        :param `item`: an instance of :class:`Shortcut`;
        :param `shortcut`: another instance of :class:`Shortcut`, to compare with the previous `item`;
        :param string `accelerator`: the user-edited accelerator string to check.

        :return: An instance of :class:`Shortcut` if the shortcut string entered by the user conflicts
         with an existing one, ``None`` otherwise.
        """

        child, cookie = self.GetFirstChild(item)

        while child:
            existingAccel = child.accelerator.lower().split('+')
            existingAccel.sort()

            if existingAccel == accelerator and shortcut != child:
                return child

            conflict = self.CheckAccelerator(child, shortcut, accelerator)

            if conflict:
                return conflict

            child, cookie = self.GetNextChild(item, cookie)

        return None


    def Match(self, filter='', item=None):
        """
        Matches this :class:`Shortcut` label string against the `filter` input variable.

        :param string `filter`: a string to match;
        :param `item`: an instance of :class:`Shortcut`: its label string is compared with
         the `filter` string to look for a match.

        :return: An instance of :class:`Shortcut` if the `filter` string is contained in
         the `item` lable, ``None`` otherwise.

        :note: The string-matching is case-insensitive.
        """

        if item is None:
            item = self

        child, cookie = self.GetFirstChild(item)

        while child:

            if filter in child.label.lower():
                self.ShowHierarchy(child)

            self.Match(filter, child)
            child, cookie = self.GetNextChild(item, cookie)


    def ShowHierarchy(self, item):
        """
        Set the status of this :class:`Shortcut` ans its parent as `shown` in the
        :class:`ListShortcut` tree hierarchy.

        :param `item`: an instance of :class:`Shortcut`.
        """

        item.shown = True
        parent = item.parent

        while parent:
            parent.shown = True
            parent = parent.parent


    def ResetVisibility(self, item=None):
        """
        Set the status of this :class:`Shortcut` and its parent as `hidden` in the
        :class:`ListShortcut` tree hierarchy.

        :param `item`: an instance of :class:`Shortcut`, used only to make this function reentrant
         (i.e. allow more than one enumeration on one and the same object simultaneously).
        """

        if item is None:
            item = self

        child, cookie = self.GetFirstChild(item)

        while child:
            child.shown = False
            item.shown = False
            self.ResetVisibility(child)
            child, cookie = self.GetNextChild(item, cookie)


    def Get(self, label, item=None):
        """
        Returns an instance of :class:`Shortcut` whose label matches the input `label` string.

        :param string `label`: the string label to compare against this :class:`Shortcut` label;
        :param `item`: an instance of :class:`Shortcut`, used only to make this function reentrant
         (i.e. allow more than one enumeration on one and the same object simultaneously).

        :return: An instance of :class:`Shortcut` or ``None`` if no match was found.
        """

        if item is None:
            item = self

        child, cookie = self.GetFirstChild(item)
        retChild = None

        while child:
            if child.label.lower() == label.lower():
                return child

            retChild = self.Get(label, child)
            child, cookie = self.GetNextChild(item, cookie)

        return retChild


    def GetById(self, id, item=None):
        """
        Returns an instance of :class:`Shortcut` whose ID matches the input `id`.

        :param integer `id`: an integer ID to compare against this :class:`Shortcut` id;
        :param `item`: an instance of :class:`Shortcut`, used only to make this function reentrant
         (i.e. allow more than one enumeration on one and the same object simultaneously).

        :return: An instance of :class:`Shortcut` or ``None`` if no match was found.
        """

        if item is None:
            item = self

        child, cookie = self.GetFirstChild(item)
        retChild = None

        while child:
            if child.menuItem and child.menuItem.GetId() == id:
                return child
            elif child.accelId == id:
                return child

            retChild = self.GetById(id, child)
            child, cookie = self.GetNextChild(item, cookie)

        return retChild


    def GetId(self):
        """ Returns this :class:`Shortcut` ID. """

        if self.menuItem is not None:
            if isinstance(self.menuItem, wx.Menu):
                return 1
            return self.menuItem.GetId()

        return self.accelId


    def RestoreDefaults(self, item=None):
        """
        Restore the original shortcut string for this :class:`Shortcut`.

        :param `item`: an instance of :class:`Shortcut`, used only to make this function reentrant
         (i.e. allow more than one enumeration on one and the same object simultaneously).
        """

        if item is None:
            item = self

        child, cookie = self.GetFirstChild(item)

        while child:
            child.accelerator = child.originalAccelerator
            child.changed = False
            self.RestoreDefaults(child)
            child, cookie = self.GetNextChild(item, cookie)


    def FromMenuItem(self):
        """
        Constructs this :class:`Shortcut` starting from a :class:`wx.Menu` or :class:`wx.MenuItem`.

        The attributes needed to properly construct a :class:`Shortcut` are the label,
        the accelerator string, the help string (optional) and the bitmap associated
        with it (optional).
        """

        if self.menuItem is None:
            return

        menuItem = self.menuItem

        if isinstance(menuItem, wx.Menu):
            label = menuItem.GetTitle()
            accelerator = DISABLED_STRING
            help = ''
            bitmap = wx.NullBitmap
        else:
            label = menuItem.GetItemLabelText()
            accelerator = menuItem.GetItemLabel()

            if '\t' in accelerator:
                accelerator = accelerator[accelerator.index('\t')+1:]
            else:
                accelerator = DISABLED_STRING

            help = menuItem.GetHelp()
            bitmap = menuItem.GetBitmap()

        self.label = label
        self.accelerator = accelerator
        self.help = help
        self.bitmap = bitmap

        self.originalAccelerator = accelerator


    def ToMenuItem(self, menuBar):
        """
        Dumps this :class:`Shortcut` into a :class:`wx.Menu` or :class:`wx.MenuItem`.

        The attributes needed to properly dump a :class:`Shortcut` into a :class:`wx.Menu` or :class:`wx.MenuBar`
        are the label and the accelerator string.

        :param `menuBar`: an instance of :class:`wx.MenuBar`.
        """

        if self.menuItem is None or not self.changed:
            return

        menuItem = self.menuItem

        if isinstance(menuItem, wx.Menu):

            if self.accelerator == DISABLED_STRING:
                label = self.label
            else:
                label = '%s\t%s'%(self.label, self.accelerator)

            menuBar.SetMenuLabel(menuItem.position, label)

        else:

            label = menuItem.GetItemLabel()
            if '\t' in label:
                label = label[0:label.index('\t')]

            if self.accelerator != DISABLED_STRING:
                label = '%s\t%s'%(label, self.accelerator)

            menuBar.SetLabel(menuItem.GetId(), label)


    def ToAcceleratorItem(self, table):
        """
        Dumps this :class:`Shortcut` into a tuple of 3 elements:

        * **flags**: a bitmask of ``wx.ACCEL_ALT``, ``wx.ACCEL_SHIFT``, ``wx.ACCEL_CTRL``, ``wx.ACCEL_CMD``
          or ``wx.ACCEL_NORMAL`` used to specify which modifier keys are held down;
        * **keyCode**: the keycode to be detected (i.e., ord('b'), wx.WXK_F10, etc...);
        * **cmdID**: the menu or control command ID to use for the accelerator event.

        :param `table`: a list of tuples, with the above specifications.
        """

        if self.menuItem is not None or not self.changed:
            return

        if self.GetId() is None:
            return

        accelerator = self.accelerator
        accelId = self.accelId

        split = accelerator.split('+')
        modifiers, keyCode = split[0:-1], split[-1]

        inv_Accel = dict(zip(ACCELERATORS.values(), ACCELERATORS.keys()))
        inv_KeyMap = dict(zip(KEYMAP.values(), KEYMAP.keys()))

        base = wx.ACCEL_NORMAL

        for mod in modifiers:
            base |= inv_Accel[mod]

        if keyCode in inv_KeyMap:
            keyCode = inv_KeyMap[keyCode]
        else:
            keyCode = ord(keyCode)

        accelItem = (base, keyCode, accelId)
        table.append(accelItem)


# ----------------------------------------------------------------------------
# ConflictDialog is a subclass of GenericMessageDialog, customized to look
# like the GIMP conflict dialog.
# ----------------------------------------------------------------------------

class ConflictDialog(GMD.GenericMessageDialog):
    """
    :class:`ConflictDialog` is a subclass of :class:`GenericMessageDialog`, customized to look
    like the GIMP conflict dialog. This class is used to resolve shortcut
    conflicts when the user assigns a shortcut that is already taken by another
    entry in the shortcut list.
    """

    def __init__(self, parent, conflict):
        """
        Default class constructor.

        :param `parent`: an instance of :class:`ShortcutEditor`;
        :param `conflict`: an instance of :class:`Shortcut`, representing the conflicting
         shortcut.
        """

        transDict = dict(shortcut=conflict.accelerator, item=conflict.label, group=conflict.parent.label)
        message = _('Shortcut "%(shortcut)s" is already taken by\n"%(item)s" from the "%(group)s" group. ')%transDict

        transDict = dict(item=conflict.label)
        extendedMessage = _('Reassigning the shortcut will cause it to be removed from \n"%(item)s". ')%transDict

        GMD.GenericMessageDialog.__init__(self, parent, message, _('Conflicting Shortcuts'),
                                          wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION)

        self.SetOKLabel(_('Reassing shortcut '))
        self.SetOKBitmap(_reassign.GetBitmap())

        self.SetExtendedMessage(extendedMessage + '\n')
        self.SetIcon(parent.GetParent().GetIcon())


# ----------------------------------------------------------------------------
# ListShortcut is a subclass of HyperTreeList, customized to look
# like the GIMP main shortcut list.
# ----------------------------------------------------------------------------

class ListShortcut(HTL.HyperTreeList, treemixin.ExpansionState):
    """
    :class:`ListShortcut` is a subclass of :class:`~wx.lib.agw.hypertreelist.HyperTreeList`,
    customized to look like the GIMP main shortcut list. This class is used to display the
    shortcut label (with an optional bitmap next to it), its accelerator and
    the help string associated with it (if present).

    This information is displayed in 3 columns inside :class:`ListShortcut`.
    """

    def __init__(self, parent):
        """
        Default class constructor.

        :param `parent`: an instance of :class:`ShortcutEditor`.
        """

        HTL.HyperTreeList.__init__(self, parent, style=wx.BORDER_THEME,
                                   agwStyle=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|
                                   wx.TR_FULL_ROW_HIGHLIGHT|HTL.TR_ELLIPSIZE_LONG_ITEMS)

        self.SetBackgroundColour(wx.WHITE)

        self.AddColumn(_('Action'))
        self.AddColumn(_('Shortcut'))
        self.AddColumn(_('Help Label'))
        self.SetMainColumn(0) # the one with the tree in it...

        self.AddRoot('')
        self.CalculateOffset()

        self.selectedItem = None
        self.hookBound = False
        self.filter = ''
        self.expansionState = []

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged)
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpandCollapse)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnExpandCollapse)

        mainWindow = self.GetMainWindow()
        mainWindow.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        mainWindow.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)


    def CalculateOffset(self):
        """
        Calculates an offset (in pixels) so that the :class:`Shortcut` items without
        a bitmap look parallel to the ones with a bitmap.
        """

        dc = wx.MemoryDC()
        dc.SelectObject(wx.Bitmap(20, 20))
        dc.SetFont(self.GetFont())

        space = 0
        text = ''

        while space < 15:
            space, dummy = dc.GetTextExtent(text)
            text += ' '

        dc.SelectObject(wx.NullBitmap)
        self.offset = text

        boldFont = FontFromFont(self.GetFont())
        boldFont.SetWeight(wx.FONTWEIGHT_BOLD)

        self.boldFont = boldFont


    def Populate(self, item=None, shortcut=None):
        """
        Recursively populates the :class:`ListShortcut` with information from the :class:`Shortcut` tree.

        :param `item`: an instance of :class:`~wx.lib.agw.customtreectrl.GenericTreeItem`. If ``None``, it is defaulted to
         the :class:`ListShortcut` root item to make this function reentrant (i.e. allow more than one
         enumeration on one and the same object simultaneously);
        :param `shortcut`: an instance of :class:`Shortcut`. If ``None``, it is defaulted to
         `self.manager` to make this function reentrant (i.e. allow more than one
         enumeration on one and the same object simultaneously).
        """

        if shortcut is None:
            shortcut = self.manager
            item = self.GetRootItem()

        for child in shortcut.children:

            if not child.shown:
                continue

            image = child.GetImageIndex()
            label = child.label

            if image < 0:
                if not child.IsTop():
                    label = self.offset + label

                newItem = self.AppendItem(item, label, data=child)
            else:
                newItem = self.AppendItem(item, label, image=image, data=child)

            if child.IsTop():
                self.SetItemFont(newItem, self.boldFont)

            self.SetItemText(newItem, child.accelerator, 1)
            self.SetItemText(newItem, child.help, 2)

            colour = (child.HasChanged() and [wx.RED] or [wx.BLACK])[0]
            self.SetItemTextColour(newItem, colour)

            self.Populate(newItem, child)


    def MakeImageList(self):
        """ Builds the :class:`ListShortcut` image list based on the bitmaps in the :class:`Shortcut` hierarchy. """

        self.imageList = wx.ImageList(16, 16)
        self.BuildImageList()
        self.AssignImageList(self.imageList)


    def BuildImageList(self, shortcut=None, index=None):
        """
        Recursively builds the :class:`ListShortcut` image list based on the bitmaps in the
        :class:`Shortcut` hierarchy.

        :param `shortcut`: an instance of :class:`Shortcut`. If ``None``, it is defaulted to
         `self.manager` to make this function reentrant (i.e. allow more than one
         enumeration on one and the same object simultaneously);
        :param integer `index`: the current image index inside the :class:`ListShortcut` own :class:`wx.ImageList`.
        """

        if shortcut is None:
            shortcut = self.manager
            index = 0

        for child in shortcut.children:
            bitmap = child.GetBitmap()

            if bitmap.IsOk():
                if bitmap.GetSize() != (16, 16):
                    bitmap = bitmap.ConvertToImage().Scale(16, 16, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
                self.imageList.Add(bitmap)
                child.imageIndex = index
                index += 1

            index = self.BuildImageList(child, index)

        return index


    def GetItemIdentity(self, item):
        """
        Return a hashable object that represents the identity of a :class:`ListShortcut` item.

        In this implementation this returns the item label.

        :param `item`: an instance of :class:`~wx.lib.agw.customtreectrl.GenericTreeItem`.
        """

        return self.GetItemText(item)


    def OnSelChanged(self, event):
        """
        Handles the ``wx.EVT_TREE_SEL_CHANGED`` event for :class:`ListShortcut`.

        :param `event`: an instance of :class:`TreeEvent`.
        """

        selectedItem = event.GetItem()

        if selectedItem != self.selectedItem:
            if self.selectedItem is not None:
                pydata = self.GetPyData(self.selectedItem)
                self.SetItemText(self.selectedItem, pydata.accelerator, 1)
            else:
                pydata = self.GetPyData(selectedItem)
                if pydata.GetId() is not None:
                    self.SetItemText(selectedItem, NEW_ACCEL_STRING, 1)
        else:

            pydata = self.GetPyData(selectedItem)
            self.SetItemText(selectedItem, pydata.accelerator, 1)

        self.selectedItem = selectedItem
        self.ShowShortcutText(False)


    def OnExpandCollapse(self, event):
        """
        Handles the ``wx.EVT_TREE_ITEM_COLLAPSED`` / ``wx.EVT_TREE_ITEM_EXPANDED`` events for :class:`ListShortcut`.

        :param `event`: an instance of :class:`TreeEvent`.
        """

        event.Skip()
        self.expansionState = self.GetExpansionState()


    def OnLeftDown(self, event):
        """
        Handles the ``wx.EVT_LEFT_DOWN`` event for :class:`ListShortcut`.

        :param `event`: an instance of :class:`MouseEvent`.
        """

        if not self.hookBound:
            self.GetParent().Bind(wx.EVT_CHAR_HOOK, self.OnShortcut)
            self.hookBound = True

        currentItem, flags, column = self.HitTest(event.GetPosition())

        if self.selectedItem is None or not currentItem:
            event.Skip()
            return

        pydata = self.GetPyData(currentItem)

        if pydata.GetId() is None:
            event.Skip()
            return

        if self.GetItemText(currentItem, 1) != NEW_ACCEL_STRING:
            self.SetItemText(currentItem, NEW_ACCEL_STRING, 1)
        else:
            self.SetItemText(currentItem, pydata.accelerator, 1)

        event.Skip()


    def OnKillFocus(self, event):
        """
        Handles the ``wx.EVT_KILL_FOCUS`` event for :class:`ListShortcut`.

        :param `event`: an instance of :class:`FocusEvent`.
        """

        self.GetParent().Unbind(wx.EVT_CHAR_HOOK)
        self.hookBound = False

        self.ShowShortcutText(False)

        if self.selectedItem:
            pydata = self.GetPyData(self.selectedItem)
            self.SetItemText(self.selectedItem, pydata.accelerator, 1)

        event.Skip()


    def OnShortcut(self, event):
        """
        Handles the ``wx.EVT_CHAR_HOOK`` event for :class:`ShortcutEditor`, implemented in :class:`ListShortcut`
        as it is easier to deal with in this class.

        :param `event`: an instance of :class:`KeyEvent`.
        """

        if self.selectedItem is None:
            # How did we get here???
            event.Skip()
            return

        pydata = self.GetPyData(self.selectedItem)
        currentText = self.GetItemText(self.selectedItem, 1)

        if pydata.GetId() is None:
            # Don't allow to change labels for shortcuts without an ID
            event.Skip()
            return

        self.ShowShortcutText(True)
        textCtrl = self.GetParent().hiddenText

        keyCode = event.GetKeyCode()
        modifiers = event.GetModifiers()

        # If we press backspace with no modifers down, *and* the current text is
        # "New accelerator..." then we reset the accelerator to "Disabled"
        if keyCode == wx.WXK_BACK and modifiers == 0 and currentText in [NEW_ACCEL_STRING, DISABLED_STRING]:

            accelerator = DISABLED_STRING

            if not self.FireShortcutChanging(pydata, accelerator):
                return

            pydata.SetAccelerator(accelerator)
            self.SetItemText(self.selectedItem, pydata.accelerator, 1)

            colour = (pydata.HasChanged() and [wx.RED] or [wx.BLACK])[0]
            self.SetItemTextColour(self.selectedItem, colour)

            self.ShowShortcutText(False)
            self.FireShortcutChanged(pydata, accelerator)

            return

        newContent = ''

        for mod_int, mod_name in MODIFIERS:

            if modifiers & mod_int == 0:
                continue

            newContent += mod_name + '+'

        if newContent.strip():
            textCtrl.ChangeValue(newContent)

        accelerator = ''

        if keyCode in KEYMAP:
            accelerator = newContent + KEYMAP[keyCode]
        else:
            try:
                toChar = chr(keyCode)
                accelerator = newContent + toChar
            except ValueError:
                pass

        if accelerator:

            if not self.FireShortcutChanging(pydata, accelerator):
                return

            if self.AcceptShortcut(pydata, accelerator):

                pydata.SetAccelerator(accelerator)
                self.SetItemText(self.selectedItem, pydata.accelerator, 1)

                colour = (pydata.HasChanged() and [wx.RED] or [wx.BLACK])[0]
                self.SetItemTextColour(self.selectedItem, colour)

                self.ShowShortcutText(False)
                self.FireShortcutChanged(pydata, accelerator)


    def AcceptShortcut(self, shortcut, accelerator):
        """
        Returns ``True`` if the input `accelerator` is a valid shortcut, ``False`` otherwise.

        :param `shortcut`: an instance of :class:`Shortcut`;
        :param string `accelerator`: the new accelerator to check.

        :note: Conflicting shortcuts are handled inside this method by presenting the user with
         a conflict dialog. At this point the user can decide to reassign an existing shortcut
         or to back away, in which case this method will return ``False``.
        """

        sortedAccel = accelerator.lower().split('+')
        sortedAccel.sort()

        conflict = self.manager.CheckAccelerator(self.manager, shortcut, sortedAccel)

        if conflict is None:
            return True

        dlg = ConflictDialog(self.GetParent(), conflict)

        if dlg.ShowModal() == wx.ID_OK:
            self.DisableShortcut(conflict)
            dlg.Destroy()
            return True

        dlg.Destroy()
        return False


    def DisableShortcut(self, conflict, item=None):
        """
        If the user decides to reassign a shortcut to another item, this method will disable
        the conflicting shortcut (by putting a "Disabled" string as its accelerator).

        :param `conflict`: an instance of :class:`Shortcut` to reset;
        :param `item`: an instance of :class:`~wx.lib.agw.customtreectrl.GenericTreeItem`. If defaulted to ``None``, it is set
         to the :class:`ListShortcut` root item and used only to make this function reentrant
         (i.e. allow more than one enumeration on one and the same object simultaneously).
        """

        if item is None:
            item = self.GetRootItem()

        child, cookie = self.GetFirstChild(item)

        while child:
            if child.GetData() == conflict:
                conflict.SetAccelerator(DISABLED_STRING)
                self.SetItemText(child, conflict.accelerator, 1)

                colour = (conflict.HasChanged() and [wx.RED] or [wx.BLACK])[0]
                self.SetItemTextColour(child, colour)
                return

            self.DisableShortcut(conflict, child)
            child, cookie = self.GetNextChild(item, cookie)


    def FireShortcutChanging(self, shortcut, newAccel):
        """
        Fires the ``EVT_SHORTCUT_CHANGING`` event for :class:`ListShortcut`.

        The event propagation (and thus the shortcut renaming by the user) can be
        interrupted by *not* calling `event.Skip()` in your handler for this event.

        :param `shortcut`: an instance of :class:`Shortcut` that is about to be renamed;
        :param string `newAccel`: the new accelerator just entered by the user.
        """

        event = ShortcutEvent(wxEVT_SHORTCUT_CHANGING, self.GetId())
        event.SetShortcut(shortcut)
        event.oldAccelerator = shortcut.accelerator
        event.accelerator = newAccel
        event.SetEventObject(self)

        if self.GetEventHandler().ProcessEvent(event):
            # the caller didn't use event.Skip()
            return False

        return True


    def FireShortcutChanged(self, shortcut, newAccel):
        """
        Fires the ``EVT_SHORTCUT_CHANGED`` event for :class:`ListShortcut`.

        :param `shortcut`: an instance of :class:`Shortcut` that has been renamed;
        :param string `newAccel`: the new accelerator just entered by the user.
        """

        event = ShortcutEvent(wxEVT_SHORTCUT_CHANGED, self.GetId())
        event.SetShortcut(shortcut)
        event.oldAccelerator = shortcut.accelerator
        event.accelerator = newAccel
        event.SetEventObject(self)

        self.GetEventHandler().ProcessEvent(event)

        return True


    def ShowShortcutText(self, show):
        """
        Shows/Hides a :class:`TextCtrl` used to display the combination of keystrokes the user
        has entered. This :class:`TextCtrl` remains visible only for a short amount of time
        and only when some keys are down.

        :param bool `show`: ``True`` to show the :class:`TextCtrl`, ``False`` to hide it.
        """

        textCtrl = self.GetParent().hiddenText

        if show and not textCtrl.IsShown():
            textCtrl.Show()

        elif not show and textCtrl.IsShown():
            textCtrl.Hide()


    def SetFilter(self, filter=''):
        """
        Sets the `filter` string against all the shortcuts in the :class:`ListShortcut` are matched.

        :param string `filter`: a string to match.
        """

        self.filter = filter

        self.manager.ResetVisibility()
        self.manager.Match(filter)
        self.RecreateTree()


    def RecreateTree(self):
        """ Recreates the entire :class:`ListShortcut` (columns excluded). """

        self.Freeze()
        self.DeleteAllItems()
        self.AddRoot('')

        self.Populate()

        if not self.expansionState:
            # Only the root item
            self.ExpandAll()
        else:
            self.SetExpansionState(self.expansionState)

        self.Thaw()


    def HasFlag(self, flag):
        """
        Overridden from :class:`wx.Window` as a workaround on the conflicts between `treemixin` and
        :class:`~wx.lib.agw.hypertreelist.HyperTreeList` with the ``wx.TR_HIDE_ROOT`` `agwStyle` set.

        :param integer `flag`: an integer bit flag specifying the `agwStyle` style.

        :return: ``True`` if the :class:`ListShortcut` has the input `flag` set, ``False`` otherwise.

        :note: Overridden from :class:`wx.Window`.
        """

        return self.HasAGWFlag(flag)


# ----------------------------------------------------------------------------
# ShortcutEditor is a subclass of wx.Dialog, customized to look
# like the GIMP main shortcut dialog.
# ----------------------------------------------------------------------------

class ShortcutEditor(wx.Dialog):
    """
    :class:`ShortcutEditor` is a widget that allows the user to customize and change keyboard
    shortcuts via a dialog. It can be used to edit :class:`wx.MenuItem` shortcuts or accelerators
    defined in a :class:`AcceleratorTable`.

    The interface itself is very much inpired by the GIMP shortcut editor:

    http://graphicssoft.about.com/od/gimptutorials/tp/keyboard-shortcut-editor.htm

    There are very few minor UI differences between :class:`ShortcutEditor` and the GIMP one,
    although the behaviour should be pretty much equivalent.
    """

    def __init__(self, parent):
        """
        Default class constructor.

        :param `parent`: an instance of :class:`wx.Window`, it can also be ``None``.
        """

        wx.Dialog.__init__(self, parent, title=_('Configure Keyboard Shortcuts'),
                           style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        self.htmlFile = os.path.join(DATA_DIR, 'default_help_text.html')
        self.htmlWindow = None

        self.CreateWidgets()
        self.DoLayout()
        self.BindEvents()

        if parent is not None and isinstance(parent, wx.TopLevelWindow):
            self.SetIcon(parent.GetIcon())

        self.Init()


    def CreateWidgets(self):
        """
        Creates all the widgets needed to populate the interface, such as buttons,
        texts and, most importantly, :class:`ListShortcut`.
        """

        self.topStatic = wx.StaticText(self, -1, _('&Search:'))
        self.searchText = wx.TextCtrl(self, -1, '')

        clearBmp = _clear.GetBitmap()
        self.clearButton = wx.BitmapButton(self, wx.ID_CLEAR, clearBmp, style=wx.NO_BORDER)

        self.listShortcut = ListShortcut(self)
        self.hiddenText = wx.TextCtrl(self, -1, '', style=wx.BORDER_THEME)

        w, h, d, e = self.hiddenText.GetFullTextExtent('Ctrl+Shift+Alt+q+g+M', self.hiddenText.GetFont())
        self.hiddenText.SetMinSize((w, h+d-e+1))

        defaultBmp = _default.GetBitmap()
        self.defaultButton = buttons.ThemedGenBitmapTextButton(self, wx.ID_RESET, defaultBmp,
                                                               _('Restore Defaults '), size=(-1, 29))

        self.infoBitmap = wx.StaticBitmap(self, -1, _info.GetBitmap())

        message = _('To edit a shortcut key, click on the corresponding row\n' \
                    'and type a new accelerator, or press backspace to clear.')

        italicFont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        italicFont.SetStyle(wx.FONTSTYLE_ITALIC)

        self.infoStatic = wx.StaticText(self, -1, message)
        self.infoStatic.SetFont(italicFont)

        okBmp = _ok.GetBitmap()
        cancelBmp = _cancel.GetBitmap()
        helpBmp = _help.GetBitmap()

        self.okButton = buttons.ThemedGenBitmapTextButton(self, wx.ID_OK, okBmp, _('OK'))
        self.cancelButton = buttons.ThemedGenBitmapTextButton(self, wx.ID_CANCEL, cancelBmp, _('Cancel'))
        self.helpButton = buttons.ThemedGenBitmapTextButton(self, wx.ID_HELP, helpBmp, _('Help'))

        self.okButton.SetDefault()


    def DoLayout(self):
        """ Lays out the widgets using sizers in a platform-independent way. """

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        mainSizer.Add((0, 5))
        topSizer.Add(self.topStatic, 0, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5)
        topSizer.Add(self.searchText, 1, wx.RIGHT, 5)
        topSizer.Add(self.clearButton, 0, wx.ALIGN_CENTER_VERTICAL)

        mainSizer.Add(topSizer, 0, wx.ALL|wx.EXPAND, 10)
        mainSizer.Add(self.listShortcut, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)
        mainSizer.Add((0, 5))

        hiddenSizer = wx.BoxSizer(wx.HORIZONTAL)
        hiddenSizer.Add(self.hiddenText, 0, wx.LEFT|wx.RIGHT|wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 10)
        hiddenSizer.Add((1, 0), 1, wx.EXPAND)
        hiddenSizer.Add(self.defaultButton, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 10)

        mainSizer.Add(hiddenSizer, 0, wx.EXPAND|wx.BOTTOM, 5)

        centerSizer = wx.BoxSizer(wx.HORIZONTAL)
        centerSizer.Add(self.infoBitmap, 0, wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 10)
        centerSizer.Add(self.infoStatic, 1, wx.ALIGN_CENTER)

        mainSizer.Add(centerSizer, 0, wx.TOP|wx.BOTTOM|wx.RIGHT, 10)

        otherSizer = wx.BoxSizer(wx.HORIZONTAL)
        # Add the fancy buttons
        otherSizer.Add(self.okButton, 0, wx.ALL, 10)
        otherSizer.Add((0, 0), 1, wx.EXPAND)
        otherSizer.Add(self.cancelButton, 0, wx.LEFT|wx.TOP|wx.BOTTOM, 10)
        otherSizer.Add(self.helpButton, 0, wx.ALL, 10)
        mainSizer.Add(otherSizer, 0, wx.EXPAND|wx.TOP, 5)

        self.hiddenText.Hide()
        self.SetSizer(mainSizer)
        mainSizer.Layout()


    def BindEvents(self):
        """
        Binds a few events we will need to process:

        * ``wx.EVT_TEXT`` for the label filtering;
        * ``wx.EVT_BUTTON`` for clearing the filtering, for the HTML help window and
          to reset all the shortcuts to their defaults.
        """

        self.searchText.Bind(wx.EVT_TEXT, self.OnSetFilter)
        self.clearButton.Bind(wx.EVT_BUTTON, self.OnClearFilter)

        self.defaultButton.Bind(wx.EVT_BUTTON, self.OnRestoreDefaults)
        self.helpButton.Bind(wx.EVT_BUTTON, self.OnHTMLHelp)


    def Init(self):
        """ Common initialization procedures. """

        self.manager = Shortcut()
        self.listShortcut.manager = self.manager


    def FromMenuBar(self, topWindow):
        """
        Builds the entire shortcut hierarchy starting from a :class:`wx.MenuBar`.

        :param `topWindow`: an instance of :class:`TopLevelWindow`, containing the :class:`wx.MenuBar`
         we wish to scan.
        """

        def MenuItemSearch(menu, item):

            for menuItem in list(menu.GetMenuItems()):
                label = menuItem.GetItemLabel()

                if not label:
                    # It's a separator
                    continue

                shortcutItem = Shortcut(menuItem=menuItem)
                shortcutItem.FromMenuItem()

                item.AppendItem(shortcutItem)

                subMenu = menuItem.GetSubMenu()

                if subMenu:
                    MenuItemSearch(subMenu, shortcutItem)

        position = 0

        for menu, name in topWindow.GetMenuBar().GetMenus():

            shortcutItem = Shortcut(menuItem=menu)
            shortcutItem.topMenu = True
            shortcutItem.position = position
            shortcutItem.FromMenuItem()

            position += 1
            self.manager.AppendItem(shortcutItem)
            MenuItemSearch(menu, item=shortcutItem)


    def ToMenuBar(self, topWindow):
        """
        Dumps the entire shortcut hierarchy (for shortcuts associated with a :class:`wx.MenuItem`), into
        a :class:`wx.MenuBar`, changing only the :class:`wx.Menu` / :class:`wx.MenuItem` labels (it does **not** rebuild
        the :class:`wx.MenuBar`).

        :param `topWindow`: an instance of :class:`TopLevelWindow`, containing the :class:`wx.MenuBar`
         we wish to repopulate.
        """

        def MenuItemSet(shortcut, menuBar):

            child, cookie = shortcut.GetFirstChild(shortcut)

            while child:
                child.ToMenuItem(menuBar)
                MenuItemSet(child, menuBar)
                child, cookie = shortcut.GetNextChild(shortcut, cookie)

        manager = self.GetShortcutManager()
        menuBar = topWindow.GetMenuBar()

        MenuItemSet(manager, menuBar)


    def FromAcceleratorTable(self, accelTable):
        """
        Builds the entire shortcut hierarchy starting from a modified version of a :class:`AcceleratorTable`.

        :param `accelTable`: a modified version of :class:`AcceleratorTable`, is a list of tuples (4 elements per tuple),
         populated like this::

            accelTable = []

            # Every tuple is defined in this way:

            for label, flags, keyCode, cmdID in my_accelerators:
                # label:   the string used to show the accelerator into the ShortcutEditor dialog
                # flags:   a bitmask of wx.ACCEL_ALT, wx.ACCEL_SHIFT, wx.ACCEL_CTRL, wx.ACCEL_CMD,
                #          or wx.ACCEL_NORMAL used to specify which modifier keys are held down
                # keyCode: the keycode to be detected (i.e., ord('b'), wx.WXK_F10, etc...)
                # cmdID:   the menu or control command ID to use for the accelerator event.

                accel_tuple = (label, flags, keyCode, cmdID)
                accelTable.append(accel_tuple)

        """

        parentShortcut = Shortcut(_('Accelerators'))

        parentShortcut.topMenu = True
        self.manager.AppendItem(parentShortcut)

        for text, modifier, accel, ids in accelTable:
            modifier = ACCELERATORS[modifier]
            if accel in KEYMAP:
                accel = KEYMAP[accel]
            else:
                accel = chr(accel)

            shortcut = (modifier and ['%s+%s'%(modifier, accel)] or [accel])[0]
            shortcutItem = Shortcut(text, shortcut, accelId=ids)
            parentShortcut.AppendItem(shortcutItem)


    def ToAcceleratorTable(self, window):
        """
        Dumps the entire shortcut hierarchy (for shortcuts associated with a :class:`AcceleratorTable`), into
        a :class:`AcceleratorTable`. This method **does** rebuild the :class:`AcceleratorTable` and sets it back
        to the input `window`.

        :param `window`: an instance of :class:`wx.Window`, to which the new :class:`AcceleratorTable` should be set.
        """

        def AccelItemSet(shortcut, table):

            child, cookie = shortcut.GetFirstChild(shortcut)

            while child:
                child.ToAcceleratorItem(table)
                table = AccelItemSet(child, table)
                child, cookie = shortcut.GetNextChild(shortcut, cookie)

            return table

        manager = self.GetShortcutManager()
        table = AccelItemSet(manager, table=[])

        window.SetAcceleratorTable(wx.AcceleratorTable(table))


    def SetColumnWidths(self):
        """
        Sets the :class:`ListShortcut` columns widths to acceptable and eye-pleasing
        numbers (in pixels).
        """

        total_width = 0
        for col in range(self.listShortcut.GetColumnCount()):
            self.listShortcut.SetColumnWidth(col, wx.LIST_AUTOSIZE)
            width = self.listShortcut.GetColumnWidth(col)

            if col == 0:
                width += 20
            elif col == 1:
                width += 5
            else:
                width = min(width, 200)

            width = max(50, width)
            self.listShortcut.SetColumnWidth(col, width)
            total_width += width

        self.listShortcut.GetMainWindow()._lineHeight += 5
        dialogHeight = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)/2

        self.SetSize((total_width+60, dialogHeight))

        self.Center()


    def OnSetFilter(self, event=None):
        """
        Handles the ``wx.EVT_TEXT`` event for :class:`ShortcutEditor`.

        :param `event`: if not ``None``, an instance of :class:`KeyEvent`.
        """

        if event:
            event.Skip()

        filter = self.searchText.GetValue()
        filter = filter.lower().strip()

        self.listShortcut.SetFilter(filter)


    def OnClearFilter(self, event):
        """
        Handles the ``wx.EVT_BUTTON`` event for :class:`ShortcutEditor` when the user clears the
        label filter at the top of the user interface.

        :param `event`: an instance of :class:`CommandEvent`.
        """

        self.searchText.SetValue('')


    def OnRestoreDefaults(self, event):
        """
        Handles the ``wx.EVT_BUTTON`` event for :class:`ShortcutEditor` when the user restores the
        original shortcuts.

        :param `event`: an instance of :class:`CommandEvent`.
        """

        self.manager.RestoreDefaults()
        self.listShortcut.RecreateTree()


    def OnHTMLHelp(self, event):
        """
        Handles the ``wx.EVT_BUTTON`` event for :class:`ShortcutEditor` when the user presses the ``Help``
        button.

        :param `event`: an instance of :class:`CommandEvent`.

        .. note::

           By default, this method launches a :class:`html.HtmlWindow` containing the default
           HTML help file. If you wish to load another help file, you should call :meth:`~ShortcutEditor.SetHTMLHelpFile`
           with another input HTML file.

        """

        if self.htmlWindow:
            self.htmlWindow.Show()
            self.htmlWindow.Restore()
            self.htmlWindow.Raise()
            return

        self.htmlWindow = HTMLHelpWindow(self, self.htmlFile)


    def GetShortcutManager(self):
        """ Returns the root :class:`Shortcut` containing the whole shortcut hierarchy. """

        return self.manager


    def SetHTMLHelpFile(self, htmlFile):
        """
        Sets a new HTML help file (a valid html file) to be loaded when the user seeks
        for an explanation on how the UI works.

        :param string `htmlFile`: a valid HTML file.
        """

        if not os.path.isfile(htmlFile):
            raise Exception('Invalid HTML help file passed to ShortcutEditor')

        self.htmlFile = htmlFile

        if self.htmlWindow is not None:
            self.htmlWindow.htmlFile = htmlFile
            self.htmlWindow.LoadFile(self.htmlFile)


    def PreShow(self):
        """ Does some more common initialization before showing :class:`ShortcutEditor`. """

        self.listShortcut.MakeImageList()
        self.listShortcut.RecreateTree()

        self.SetColumnWidths()


    def ShowModal(self):
        """
        Shows the :class:`ShortcutEditor` dialog in an application-modal way.

        Program flow does not return until the dialog has been dismissed with `EndModal`.

        :return: The value set with :meth:`~Dialog.SetReturnCode`.

        .. note::

           Notice that it is possible to call :meth:`~ShortcutEditor.ShowModal` for a dialog which had been
           previously shown with :meth:`~ShortcutEditor.Show`, this allows to make an existing modeless dialog
           modal. However :meth:`~ShortcutEditor.ShowModal` can't be called twice without intervening `EndModal` calls.


        .. note::

           Note that this function creates a temporary event loop which takes precedence
           over the application's main event loop (see :class:`EventLoopBase`) and which is
           destroyed when the dialog is dismissed. This also results in a call to
           :meth:`AppConsole.ProcessPendingEvents` ().

        """

        self.PreShow()
        return wx.Dialog.ShowModal(self)


    def Show(self, show=True):
        """
        Hides or shows the :class:`ShortcutEditor` dialog.

        The preferred way of dismissing a modal dialog is to use `EndModal`.

        :param bool `show`: if ``True``, the dialog box is shown and brought to the front,
         otherwise the box is hidden. If ``False`` and the dialog is modal, control is
         returned to the calling program.

        :note: Reimplemented from :class:`wx.Window`.
        """

        self.PreShow()
        wx.Dialog.Show(self, show)


