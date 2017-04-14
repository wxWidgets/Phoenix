#----------------------------------------------------------------------------
# Name:         combotreebox.py
# Purpose:
#
# Author:       Frank Niessink <frank@niessink.com>
#
# Created:
# Version:      1.1
# Date:         August 1, 2010
# Licence:      wxWidgets license
# Tags:         phoenix-port
#----------------------------------------------------------------------------
"""
ComboTreeBox provides a ComboBox that pops up a tree instead of a list.

ComboTreeBox tries to provide the same interface as :class:`wx.ComboBox` as much as
possible. However, whereas the ComboBox widget uses indices to access
items in the list of choices, ComboTreeBox uses TreeItemId's instead. If
you add an item to the ComboTreeBox (using Append or Insert), the
:class:`wx.TreeItemId` associated with the added item is returned. You can then use
that `wx.TreeItemId` to add items as children of that first item. For
example::

    from wx.lib.combotreebox import ComboTreeBox
    combo = ComboTreeBox(parent)
    item1 = combo.Append('Item 1') # Add a root item
    item1a = combo.Append('Item 1a', parent=item1) # Add a child to item1


You can also add client data to each of the items like this::

    item1 = combo.Append('Item 1', clientData=somePythonObject)
    item1a = combo.Append('Item 1a', parent=item1,
                           clientData=someOtherPythonObject)


And later fetch the client data like this::

    somePythonObject = combo.GetClientData(item1)


To get the client data of the currently selected item (if any)::

    currentItem = combo.GetSelection()
    if currentItem:
        somePythonObject = combo.GetClientData(currentItem)


Supported styles are the same as for :class:`wx.ComboBox`, i.e. ``wx.CB_READONLY`` and
``wx.CB_SORT``. Provide them as usual::

    combo = ComboTreeBox(parent, style=wx.CB_READONLY|wx.CB_SORT)


Supported platforms: wxMSW and wxMAC natively, wxGTK by means of a
workaround.

.. moduleauthor:: Frank Niessink <frank@niessink.com>

Copyright 2006, 2008, 2010, Frank Niessink
License: wxWidgets license
Version: 1.1
Date: August 1, 2010

"""

import wx

__all__ = ['ComboTreeBox'] # Export only the ComboTreeBox widget


# ---------------------------------------------------------------------------


class IterableTreeCtrl(wx.TreeCtrl):
    """
    TreeCtrl is the same as :class:`TreeCtrl`, with a few convenience methods
    added for easier navigation of items. """

    def GetPreviousItem(self, item):
        """
        Returns the item that is on the line immediately above item
        (as is displayed when the tree is fully expanded). The returned
        item is invalid if item is the first item in the tree.

        :param TreeItemId `item`: a :class:`TreeItemId`
        :return: the :class:`TreeItemId` previous to the one passed in or an invalid item
        :rtype: :class:`TreeItemId`

        """
        previousSibling = self.GetPrevSibling(item)
        if previousSibling:
            return self.GetLastChildRecursively(previousSibling)
        else:
            parent = self.GetItemParent(item)
            if parent == self.GetRootItem() and \
                (self.GetWindowStyle() & wx.TR_HIDE_ROOT):
                # Return an invalid item, because the root item is hidden
                return previousSibling
            else:
                return parent

    def GetNextItem(self, item):
        """
        Returns the item that is on the line immediately below item
        (as is displayed when the tree is fully expanded). The returned
        item is invalid if item is the last item in the tree.

        :param TreeItemId `item`: a :class:`TreeItemId`
        :return: :class:`TreeItemId` of the next item or an invalid item
        :rtype: :class:`TreeItemId`

        """
        if self.ItemHasChildren(item):
            firstChild, cookie = self.GetFirstChild(item)
            return firstChild
        else:
            return self.GetNextSiblingRecursively(item)

    def GetFirstItem(self):
        """
        Returns the very first item in the tree. This is the root item
        unless the root item is hidden. In that case the first child of
        the root item is returned, if any. If the tree is empty, an
        invalid tree item is returned.

        :return: :class:`TreeItemId`
        :rtype: :class:`TreeItemId`

        """
        rootItem = self.GetRootItem()
        if rootItem and (self.GetWindowStyle() & wx.TR_HIDE_ROOT):
            firstChild, cookie = self.GetFirstChild(rootItem)
            return firstChild
        else:
            return rootItem

    def GetLastChildRecursively(self, item):
        """
        Returns the last child of the last child ... of item. If item
        has no children, item itself is returned. So the returned item
        is always valid, assuming a valid item has been passed.

        :param TreeItemId `item`: a :class:`TreeItemId`
        :return: :class:`TreeItemId` of the last item or an invalid item
        :rtype: :class:`TreeItemId`

        """
        lastChild = item
        while self.ItemHasChildren(lastChild):
            lastChild = self.GetLastChild(lastChild)
        return lastChild

    def GetNextSiblingRecursively(self, item):
        """
        Returns the next sibling of item if it has one. If item has no
        next sibling the next sibling of the parent of item is returned.
        If the parent has no next sibling the next sibling of the parent
        of the parent is returned, etc. If none of the ancestors of item
        has a next sibling, an invalid item is returned.

        :param TreeItemId `item`: a :class:`TreeItemId`
        :return: :class:`TreeItemId` of the next item or an invalid item
        :rtype: :class:`TreeItemId`

        """
        if item == self.GetRootItem():
            return wx.TreeItemId() # Return an invalid TreeItemId
        nextSibling = self.GetNextSibling(item)
        if nextSibling:
            return nextSibling
        else:
            parent = self.GetItemParent(item)
            return self.GetNextSiblingRecursively(parent)

    def GetSelection(self):
        """
        Extend GetSelection to never return the root item if the
        root item is hidden.
        """
        selection = super(IterableTreeCtrl, self).GetSelection()
        if selection == self.GetRootItem() and \
            (self.GetWindowStyle() & wx.TR_HIDE_ROOT):
            return wx.TreeItemId() # Return an invalid TreeItemId
        else:
            return selection


# ---------------------------------------------------------------------------


class BasePopupFrame(wx.Frame):
    """
    BasePopupFrame is the base class for platform specific versions of the
    PopupFrame. The PopupFrame is the frame that is popped up by ComboTreeBox.
    It contains the tree of items that the user can select one item from. Upon
    selection, or when focus is lost, the frame is hidden.
    """

    def __init__(self, parent):
        super(BasePopupFrame, self).__init__(parent,
            style=wx.DEFAULT_FRAME_STYLE & wx.FRAME_FLOAT_ON_PARENT &
                  ~(wx.RESIZE_BORDER | wx.CAPTION))
        self._createInterior()
        self._layoutInterior()
        self._bindEventHandlers()

    def _createInterior(self):
        self._tree = IterableTreeCtrl(self,
            style=wx.TR_HIDE_ROOT|wx.TR_LINES_AT_ROOT|wx.TR_HAS_BUTTONS)
        self._tree.AddRoot('Hidden root node')

    def _layoutInterior(self):
        frameSizer = wx.BoxSizer(wx.HORIZONTAL)
        frameSizer.Add(self._tree, flag=wx.EXPAND, proportion=1)
        self.SetSizerAndFit(frameSizer) #****

    def _bindEventHandlers(self):
        self._tree.Bind(wx.EVT_CHAR, self.OnChar)
        self._tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)
        self._tree.Bind(wx.EVT_LEFT_DOWN, self.OnMouseClick)

    def _bindKillFocus(self):
        self._tree.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

    def _unbindKillFocus(self):
        self._tree.Unbind(wx.EVT_KILL_FOCUS)

    def OnKillFocus(self, event):
        # We hide the frame rather than destroy it, so it can be
        # popped up again later. Use CallAfter so that clicking the combobox
        # button doesn't immediately popup the frame again.
        wx.CallAfter(self.Hide)
        self.GetParent().NotifyNoItemSelected()
        event.Skip()

    def OnChar(self, keyEvent):
        if self._keyShouldHidePopup(keyEvent):
            self.Hide()
            self.GetParent().NotifyNoItemSelected()
        keyEvent.Skip()

    def _keyShouldHidePopup(self, keyEvent):
        return keyEvent.GetKeyCode() == wx.WXK_ESCAPE

    def OnMouseClick(self, event):
        item, flags = self._tree.HitTest(event.GetPosition())
        if item and (flags & wx.TREE_HITTEST_ONITEMLABEL):
            self._tree.SelectItem(item)
            self.Hide()
            self.GetParent().NotifyItemSelected(self._tree.GetItemText(item))
        else:
            event.Skip()

    def OnItemActivated(self, event):
        item = event.GetItem()
        self.Hide()
        self.GetParent().NotifyItemSelected(self._tree.GetItemText(item))

    def Show(self):
        self._bindKillFocus()
        wx.CallAfter(self._tree.SetFocus)
        super(BasePopupFrame, self).Show()

    def Hide(self):
        self._unbindKillFocus()
        super(BasePopupFrame, self).Hide()

    def GetTree(self):
        return self._tree


class MSWPopupFrame(BasePopupFrame):
    """MSWPopupFrame is the base class Windows PopupFrame."""
    def Show(self):
        # Comply with the MS Windows Combobox behaviour: if the text in
        # the text field is not in the tree, the first item in the tree
        # is selected.
        if not self._tree.GetSelection():
            self._tree.SelectItem(self._tree.GetFirstItem())
        super(MSWPopupFrame, self).Show()


class MACPopupFrame(BasePopupFrame):
    """MacPopupFrame is the base class Mac PopupFrame."""
    def _bindKillFocus(self):
        # On wxMac, the kill focus event doesn't work, but the
        # deactivate event does:
        self.Bind(wx.EVT_ACTIVATE, self.OnKillFocus)

    def _unbindKillFocus(self):
        self.Unbind(wx.EVT_ACTIVATE)

    def OnKillFocus(self, event):
        if not event.GetActive(): # We received a deactivate event
            self.Hide()
            wx.CallAfter(self.GetParent().NotifyNoItemSelected)
        event.Skip()


class GTKPopupFrame(BasePopupFrame):
    """GTKPopupFrame is the base class GTK PopupFrame."""
    def _keyShouldHidePopup(self, keyEvent):
        # On wxGTK, Alt-Up also closes the popup:
        return super(GTKPopupFrame, self)._keyShouldHidePopup(keyEvent) or \
            (keyEvent.AltDown() and keyEvent.GetKeyCode() == wx.WXK_UP)


# ---------------------------------------------------------------------------


class BaseComboTreeBox(object):
    """
    BaseComboTreeBox is the base class for platform specific versions of the
    ComboTreeBox.
    """

    def __init__(self, *args, **kwargs):
        style = kwargs.pop('style', 0)
        if style & wx.CB_READONLY:
            style &= ~wx.CB_READONLY # We manage readonlyness ourselves
            self._readOnly = True
        else:
            self._readOnly = False
        if style & wx.CB_SORT:
            style &= ~wx.CB_SORT # We manage sorting ourselves
            self._sort = True
        else:
            self._sort = False
        super(BaseComboTreeBox, self).__init__(style=style, *args, **kwargs)
        self._createInterior()
        self._layoutInterior()
        self._bindEventHandlers()

    # Methods to construct the widget.

    def _createInterior(self):
        self._popupFrame = self._createPopupFrame()
        self._text = self._createTextCtrl()
        self._button = self._createButton()
        self._tree = self._popupFrame.GetTree()

    def _createTextCtrl(self):
        return self # By default, the text control is the control itself.

    def _createButton(self):
        return self # By default, the dropdown button is the control itself.

    def _createPopupFrame(self):
        # It is a subclass responsibility to provide the right PopupFrame,
        # depending on platform:
        raise NotImplementedError

    def _layoutInterior(self):
        pass # By default, there is no layout to be done.

    def _bindEventHandlers(self):
        for eventSource, eventType, eventHandler in self._eventsToBind():
            eventSource.Bind(eventType, eventHandler)

    def _eventsToBind(self):
        """
        _eventsToBind returns a list of eventSource, eventType,
        eventHandlers tuples that will be bound. This method can be
        extended to bind additional events. In that case, don't
        forget to call _eventsToBind on the super class.

        :return: [(eventSource, eventType, eventHandlers), ]
        :rtype: list

        """
        return [(self._text, wx.EVT_KEY_DOWN, self.OnKeyDown),
                (self._text, wx.EVT_TEXT, self.OnText),
                (self._button, wx.EVT_BUTTON, self.OnMouseClick)]

    # Event handlers

    def OnMouseClick(self, event):
        if self._popupFrame.IsShown():
            self.Hide()
        else:
            self.Popup()
        # Note that we don't call event.Skip() to prevent popping up the
        # ComboBox's own box.

    def OnKeyDown(self, keyEvent):
        if self._keyShouldNavigate(keyEvent):
            self._navigateUpOrDown(keyEvent)
        elif self._keyShouldPopUpTree(keyEvent):
            self.Popup()
        else:
            keyEvent.Skip()

    def _keyShouldPopUpTree(self, keyEvent):
        return (keyEvent.AltDown() or keyEvent.MetaDown()) and \
                keyEvent.GetKeyCode() == wx.WXK_DOWN

    def _keyShouldNavigate(self, keyEvent):
        return keyEvent.GetKeyCode() in (wx.WXK_DOWN, wx.WXK_UP) and not \
            self._keyShouldPopUpTree(keyEvent)

    def _navigateUpOrDown(self, keyEvent):
        item = self.GetSelection()
        if item:
            navigationMethods = {wx.WXK_DOWN: self._tree.GetNextItem,
                                 wx.WXK_UP: self._tree.GetPreviousItem}
            getNextItem = navigationMethods[keyEvent.GetKeyCode()]
            nextItem = getNextItem(item)
        else:
            nextItem = self._tree.GetFirstItem()
        if nextItem:
            self.SetSelection(nextItem)

    def OnText(self, event):
        event.Skip()
        textValue = self._text.GetValue()
        selection = self._tree.GetSelection()
        if not selection or self._tree.GetItemText(selection) != textValue:
            # We need to change the selection because it doesn't match the
            # text just entered
            item = self.FindString(textValue)
            if item:
                self._tree.SelectItem(item)
            else:
                self._tree.Unselect()

    # Methods called by the PopupFrame, to let the ComboTreeBox know
    # about what the user did.

    def NotifyItemSelected(self, text):
        """
        Simulate selection of an item by the user. This is meant to
        be called by the PopupFrame when the user selects an item.
        """
        self._text.SetValue(text)
        self._postComboBoxSelectedEvent(text)
        self.SetFocus()

    def _postComboBoxSelectedEvent(self, text):
        """Simulate a selection event. """
        event = wx.CommandEvent(wx.wxEVT_COMMAND_COMBOBOX_SELECTED,
                                self.GetId())
        event.SetString(text)
        self.GetEventHandler().ProcessEvent(event)

    def NotifyNoItemSelected(self):
        """
        This is called by the PopupFrame when the user closes the
        PopupFrame, without selecting an item.
        """
        self.SetFocus()

    # Misc methods, not part of the ComboBox API.

    def Popup(self):
        """Pops up the frame with the tree."""
        comboBoxSize = self.GetSize()
        x, y = self.GetParent().ClientToScreen(self.GetPosition())
        y += comboBoxSize[1]
        width = comboBoxSize[0]
        height = 300
        self._popupFrame.SetSize(x, y, width, height)
        # On wxGTK, when the Combobox width has been increased a call
        # to SetMinSize is needed to force a resize of the popupFrame:
        self._popupFrame.SetMinSize((width, height))
        self._popupFrame.Show()

    def Hide(self):
        """Hide the popped up frame with the tree."""
        self._popupFrame.Hide()

    def GetTree(self):
        """Returns the tree control that is popped up."""
        return self._popupFrame.GetTree()

    def FindClientData(self, clientData, parent=None):
        """
        Finds the *first* item in the tree with client data equal to the
        given clientData. If no such item exists, an invalid item is
        returned.

        :param PyObject `clientData`: the client data to find
        :keyword TreeItemId `parent`: :class:`TreeItemId` parent or None
        :return: :class:`TreeItemId`
        :rtype: :class:`TreeItemId`

        """
        parent = parent or self._tree.GetRootItem()
        child, cookie = self._tree.GetFirstChild(parent)
        while child:
            if self.GetClientData(child) == clientData:
                return child
            else:
                result = self.FindClientData(clientData, child)
                if result:
                    return result
            child, cookie = self._tree.GetNextChild(parent, cookie)
        return child

    def SetClientDataSelection(self, clientData):
        """
        Selects the item with the provided clientData in the control.
        Returns True if the item belonging to the clientData has been
        selected, False if it wasn't found in the control.

        :param PyObject `clientData`: the client data to find
        :return: True if an item has been selected, otherwise False
        :rtype: bool

        """
        item = self.FindClientData(clientData)
        if item:
            self._tree.SelectItem(item)
            string = self._tree.GetItemText(item)
            if self._text.GetValue() != string:
                self._text.SetValue(string)
            return True
        else:
            return False

    # The following methods are all part of the ComboBox API (actually
    # the ControlWithItems API) and have been adapted to take TreeItemIds
    # as parameter and return :class:`TreeItemId`s, rather than indices.

    def Append(self, itemText, parent=None, clientData=None):
        """
        Adds the itemText to the control, associating the given clientData
        with the item if not None. If parent is None, itemText is added
        as a root item, else itemText is added as a child item of
        parent. The return value is the :class:`TreeItemId` of the newly added
        item.

        :param string `itemText`: text to add to the control
        :keyword TreeItemId `parent`: if None item is added as a root, else it
          is added as a child of the parent.
        :keyword PyObject `clientData`: the client data to find
        :return: :class:`TreeItemId` of newly added item
        :rtype: :class:`TreeItemId`

        """
        if parent is None:
            parent = self._tree.GetRootItem()
        item = self._tree.AppendItem(parent, itemText,
                                     data=clientData)
        if self._sort:
            self._tree.SortChildren(parent)
        return item

    def Clear(self):
        """Removes all items from the control."""
        return self._tree.DeleteAllItems()

    def Delete(self, item):
        """Deletes the item from the control."""
        return self._tree.Delete(item)

    def FindString(self, string, parent=None):
        """
        Finds the *first* item in the tree with a label equal to the
        given string. If no such item exists, an invalid item is
        returned.

        :param string `string`: string to be found in label
        :keyword TreeItemId `parent`: :class:`TreeItemId` parent or None
        :return: :class:`TreeItemId`
        :rtype: :class:`TreeItemId`

        """
        parent = parent or self._tree.GetRootItem()
        child, cookie = self._tree.GetFirstChild(parent)
        while child:
            if self._tree.GetItemText(child) == string:
                return child
            else:
                result = self.FindString(string, child)
                if result:
                    return result
            child, cookie = self._tree.GetNextChild(parent, cookie)
        return child

    def GetSelection(self):
        """
        Returns the :class:`TreeItemId` of the selected item or an invalid item
        if no item is selected.

        :return: a TreeItemId
        :rtype: :class:`TreeItemId`

        """
        selectedItem = self._tree.GetSelection()
        if selectedItem and selectedItem != self._tree.GetRootItem():
            return selectedItem
        else:
            return self.FindString(self.GetValue())

    def GetString(self, item):
        """
        Returns the label of the given item.

        :param TreeItemId `item`: :class:`TreeItemId` for which to get the label
        :return: label
        :rtype: string

        """
        if item:
            return self._tree.GetItemText(item)
        else:
            return ''

    def GetStringSelection(self):
        """
        Returns the label of the selected item or an empty string if no item
        is selected.

        :return: the label of the selected item or an empty string
        :rtype: string

        """
        return self.GetValue()

    def Insert(self, itemText, previous=None, parent=None, clientData=None):
        """
        Insert an item into the control before the ``previous`` item
        and/or as child of the ``parent`` item. The itemText is associated
        with clientData when not None.

        :param string `itemText`: the items label
        :keyword TreeItemId `previous`: the previous item
        :keyword TreeItemId `parent`: the parent item
        :keyword PyObject `clientData`: the data to associate
        :return: the create :class:`TreeItemId`
        :rtype: :class:`TreeItemId`

        """
        data = wx.TreeItemData(clientData)
        if parent is None:
            parent = self._tree.GetRootItem()
        if previous is None:
            item = self._tree.InsertItemBefore(parent, 0, itemText, data=data)
        else:
            item = self._tree.InsertItem(parent, previous, itemText, data=data)
        if self._sort:
            self._tree.SortChildren(parent)
        return item

    def IsEmpty(self):
        """
        Returns True if the control is empty or False if it has some items.

        :return: True if control is empty
        :rtype: boolean

        """
        return self.GetCount() == 0

    def GetCount(self):
        """
        Returns the number of items in the control.

        :return: items in control
        :rtype: integer

        """
        # Note: We don't need to substract 1 for the hidden root item,
        # because the TreeCtrl does that for us
        return self._tree.GetCount()

    def SetSelection(self, item):
        """
        Sets the provided item to be the selected item.

        :param TreeItemId `item`: Select this item

        """
        self._tree.SelectItem(item)
        self._text.SetValue(self._tree.GetItemText(item))

    Select = SetSelection

    def SetString(self, item, string):
        """
        Sets the label for the provided item.

        :param TreeItemId `item`: item on which to set the label
        :param string `string`: the label to set

        """
        self._tree.SetItemText(item, string)
        if self._sort:
            self._tree.SortChildren(self._tree.GetItemParent(item))

    def SetStringSelection(self, string):
        """
        Selects the item with the provided string in the control.
        Returns True if the provided string has been selected, False if
        it wasn't found in the control.

        :param string `string`: try to select the item with this string
        :return: True if an item has been selected
        :rtype: boolean

        """
        item = self.FindString(string)
        if item:
            if self._text.GetValue() != string:
                self._text.SetValue(string)
            self._tree.SelectItem(item)
            return True
        else:
            return False

    def GetClientData(self, item):
        """
        Returns the client data associated with the given item, if any.

        :param TreeItemId `item`: item for which to get clientData
        :return: the client data
        :rtype: PyObject

        """
        return self._tree.GetItemPyData(item)

    def SetClientData(self, item, clientData):
        """
        Associate the given client data with the provided item.

        :param TreeItemId `item`: item for which to set the clientData
        :param PyObject `clientData`: the data to set

        """
        self._tree.SetItemPyData(item, clientData)

    def GetValue(self):
        """
        Returns the current value in the combobox text field.

        :return: the current value in the combobox text field
        :rtype: string

        """
        if self._text == self:
            return super(BaseComboTreeBox, self).GetValue()
        else:
            return self._text.GetValue()

    def SetValue(self, value):
        """
        Sets the text for the combobox text field.

        NB: For a combobox with wxCB_READONLY style the string must be
        in the combobox choices list, otherwise the call to SetValue()
        is ignored.

        :param string `value`: set the combobox text field

        """
        item = self._tree.GetSelection()
        if not item or self._tree.GetItemText(item) != value:
            item = self.FindString(value)
        if self._readOnly and not item:
            return
        if self._text == self:
            super(BaseComboTreeBox, self).SetValue(value)
        else:
            self._text.SetValue(value)
        if item:
            if self._tree.GetSelection() != item:
                self._tree.SelectItem(item)
        else:
            self._tree.Unselect()


class NativeComboTreeBox(BaseComboTreeBox, wx.ComboBox):
    """
    NativeComboTreeBox, and any subclass, uses the native ComboBox as basis,
    but prevent it from popping up its drop down list and instead pops up a
    PopupFrame containing a tree of items.
    """

    def _eventsToBind(self):
        events = super(NativeComboTreeBox, self)._eventsToBind()
        # Bind all mouse click events to self.OnMouseClick so we can
        # intercept those events and prevent the native Combobox from
        # popping up its list of choices.
        for eventType in (wx.EVT_LEFT_DOWN, wx.EVT_LEFT_DCLICK,
                          wx.EVT_MIDDLE_DOWN, wx.EVT_MIDDLE_DCLICK,
                          wx.EVT_RIGHT_DOWN, wx.EVT_RIGHT_DCLICK):
            events.append((self._button, eventType, self.OnMouseClick))
        if self._readOnly:
            events.append((self, wx.EVT_CHAR, self.OnChar))
        return events

    def OnChar(self, event):
        # OnChar is only called when in read only mode. We don't call
        # event.Skip() on purpose, to prevent the characters from being
        # displayed in the text field.
        pass


class MSWComboTreeBox(NativeComboTreeBox):
    """
    MSWComboTreeBox adds one piece of functionality as compared to
    NativeComboTreeBox: when the user browses through the tree, the
    ComboTreeBox's text field is continuously updated to show the
    currently selected item in the tree. If the user cancels
    selecting a new item from the tree, e.g. by hitting escape, the
    previous value (the one that was selected before the PopupFrame
    was popped up) is restored.
    """

    def _createPopupFrame(self):
        return MSWPopupFrame(self)

    def _eventsToBind(self):
        events = super(MSWComboTreeBox, self)._eventsToBind()
        events.append((self._tree, wx.EVT_TREE_SEL_CHANGED,
            self.OnSelectionChangedInTree))
        return events

    def OnSelectionChangedInTree(self, event):
        if not self:
            return
        item = event.GetItem()
        if item:
            selectedValue = self._tree.GetItemText(item)
            if self.GetValue() != selectedValue:
                self.SetValue(selectedValue)
        event.Skip()

    def _keyShouldPopUpTree(self, keyEvent):
        return super(MSWComboTreeBox, self)._keyShouldPopUpTree(keyEvent) or \
            (keyEvent.GetKeyCode() == wx.WXK_F4 and not keyEvent.HasModifiers()) or \
            ((keyEvent.AltDown() or keyEvent.MetaDown()) and \
              keyEvent.GetKeyCode() == wx.WXK_UP)

    def SetValue(self, value):
        """
        Extend SetValue to also select the text in the
        ComboTreeBox's text field.

        :param string `value`: set the value and select it

        """
        super(MSWComboTreeBox, self).SetValue(value)
        # We select the text in the ComboTreeBox's text field.
        # There is a slight complication, however. When the control is
        # deleted, SetValue is called. But if we call SetMark at that
        # time, wxPython will crash. We can prevent this by comparing the
        # result of GetLastPosition and the length of the value. If they
        # match, all is fine. If they don't match, we don't call SetMark.
        if self._text.GetLastPosition() == len(value):
            self._text.SetTextSelection(0, self._text.GetLastPosition())

    def Popup(self, *args, **kwargs):
        """
        Extend Popup to store a copy of the current value, so we can
        restore it later (in NotifyNoItemSelected). This is necessary
        because MSWComboTreeBox will change the value as the user
        browses through the items in the popped up tree.
        """
        self._previousValue = self.GetValue()
        super(MSWComboTreeBox, self).Popup(*args, **kwargs)

    def NotifyNoItemSelected(self, *args, **kwargs):
        """
        Restore the value copied previously, because the user has
        not selected a new value.
        """
        self.SetValue(self._previousValue)
        super(MSWComboTreeBox, self).NotifyNoItemSelected(*args, **kwargs)


class GTKComboTreeBox(BaseComboTreeBox, wx.Panel):
    """
    The ComboTreeBox widget for wxGTK. This is actually a work
    around because on wxGTK, there doesn't seem to be a way to intercept
    mouse events sent to the Combobox. Intercepting those events is
    necessary to prevent the Combobox from popping up the list and pop up
    the tree instead. So, until wxPython makes intercepting those events
    possible we build a poor man's Combobox ourselves using a TextCtrl and
    a BitmapButton.
    """

    def _createPopupFrame(self):
        return GTKPopupFrame(self)

    def _createTextCtrl(self):
        if self._readOnly:
            style = wx.TE_READONLY
        else:
            style = 0
        return wx.TextCtrl(self, style=style)

    def _createButton(self):
        bitmap = wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, client=wx.ART_BUTTON)
        return wx.BitmapButton(self, bitmap=bitmap)

    def _layoutInterior(self):
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        panelSizer.Add(self._text, flag=wx.EXPAND, proportion=1)
        panelSizer.Add(self._button)
        self.SetSizerAndFit(panelSizer)


# class MACComboTreeBox(NativeComboTreeBox):
#     def _createPopupFrame(self):
#         return MACPopupFrame(self)
#
#     def _createButton(self):
#         return self.GetChildren()[0] # The choice button
#
#     def _keyShouldNavigate(self, keyEvent):
#         return False # No navigation with up and down on wxMac
#
#     def _keyShouldPopUpTree(self, keyEvent):
#         return super(MACComboTreeBox, self)._keyShouldPopUpTree(keyEvent) or \
#             keyEvent.GetKeyCode() == wx.WXK_DOWN


# The MAC implementation based on the NativeComboTreeBox is no longer working,
# so let's use the GTKComboTreeBox instead.
MACComboTreeBox = GTKComboTreeBox


# ---------------------------------------------------------------------------


def ComboTreeBox(*args, **kwargs):
    """
    Factory function to create the right ComboTreeBox depending on
    platform. You may force a specific class, e.g. for testing
    purposes, by setting the keyword argument 'platform', e.g.
    'platform=GTK' or 'platform=MSW' or 'platform=MAC'.

    :keyword string `platform`: 'GTK'|'MSW'|'MAC' can be used to override the
      actual platform for testing

    """

    platform = kwargs.pop('platform', None) or wx.PlatformInfo[0][4:7]
    ComboTreeBoxClassName = '%sComboTreeBox' % platform
    ComboTreeBoxClass = globals()[ComboTreeBoxClassName]
    return ComboTreeBoxClass(*args, **kwargs)

