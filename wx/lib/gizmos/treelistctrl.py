
#
#  **** THIS IS STILL A WIP ****
#

#----------------------------------------------------------------------
# Name:        wx.lib.gizmos.treelistctrl
# Purpose:     A Python port of the C++ wxTreeListCtrl from the old
#              gizmos module and the wxCode library.
#
# Author:      Robin Dunn
#
# Created:     16-Nov-2017
# Copyright:   (c) 2017 by Total Control Software
# Licence:     wxWindows license
# Tags:
#----------------------------------------------------------------------
"""
A generic widget that combines the multicolumn features of a wx.ListCtrl
with the hierarchical features of a wx.TreeCtrl.
"""

import wx


# Styles
TR_COLUMN_LINES = 0x1000 # Put border around items
TR_VIRTUAL      = 0x4000 # The application provides items text on demand

# Other public constants
DEFAULT_COL_WIDTH = 100
NO_IMAGE = -1

# Internal constants
class _const:
    LINEHEIGHT = 10
    LINEATROOT = 5
    MARGIN = 2
    MININDENT = 16
    BTNWIDTH = 9
    BTNHEIGHT = 9
    EXTRA_WIDTH = 4
    EXTRA_HEIGHT = 4
    HEADER_OFFSET_X = 1
    HEADER_OFFSET_Y = 1

    DRAG_TIMER_TICKS = 250      # minimum drag wait time in ms
    FIND_TIMER_TICKS = 500      # minimum find wait time in ms
    RENAME_TIMER_TICKS = 250    # minimum rename wait time in ms


#--------------------------------------------------------------------------

# modes for navigation
TL_MODE_NAV_FULLTREE = 0x0000  # default
TL_MODE_NAV_EXPANDED = 0x0001
TL_MODE_NAV_VISIBLE  = 0x0002
TL_MODE_NAV_LEVEL    = 0x0004

# modes for FindItem
TL_MODE_FIND_EXACT   = 0x0000  # default
TL_MODE_FIND_PARTIAL = 0x0010
TL_MODE_FIND_NOCASE  = 0x0020

# additional flag for HitTest
TREE_HITTEST_ONITEMCOLUMN = 0x2000

TreeListCtrlNameStr = 'treelistctrl'



class TreeListCtrl(wx.Control):
    def __init__(self, *args, **kw):
        self.m_header_win = None
        self.m_main_win = None
        self.m_headerHeight = 0
        super(TreeListCtrl, self).__init__()

        # Do the 2nd phase of the widget creation now too?
        if args or kw:
            self.Create(*args, **kw)


    def Create(self, parent, id=wx.ID_ANY,
               pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=wx.TR_DEFAULT_STYLE,
               validator=wx.DefaultValidator,
               name=TreeListCtrlNameStr):

        main_style = style & ~(wxSIMPLE_BORDER|wxSUNKEN_BORDER|wxDOUBLE_BORDER|
                               wxRAISED_BORDER|wxSTATIC_BORDER)
        ctrl_style = style & ~(wxVSCROLL|wxHSCROLL)

        if not super(TreeListCtrl, self).Create(parent, id, pos, size, ctrl_style, validator, name):
           return False

        self.m_main_win = _TreeListMainWindow(self, -1, (0, 0), size, main_style, validator)
        self.m_header_win = _TreeListHeaderWindow(self, -1, m_main_win, (0, 0), wx.DefaultSize, wx.TAB_TRAVERSAL);
        self._CalculateAndSetHeaderHeight()

        self.Bind(wx.EVT_SIZE, self.OnSize)
        return True


    def _CalculateAndSetHeaderHeight(self):
        if self.m_header_win:
            h = wx.RendererNative.Get().GetHeaderButtonHeight(self.m_header_win)

            # only update if changed
            if h != self.m_headerHeight:
                self.m_headerHeight = h
                self._DoHeaderLayout()


    def _DoHeaderLayout(self):
        w, h = self.GetClientSize()
        if self.m_header_win:
            self.m_header_win.SetSize(0, 0, w, self.m_headerHeight)
            self.m_header_win.Refresh()

        if self.m_main_win:
            self.m_main_win.SetSize(0, self.m_headerHeight + 1, w, h - self.m_headerHeight - 1)


    def OnSize(self, evt):
        self._DoHeaderLayout()


    def GetHeaderWindow(self):
        return self.m_header_win

    def GetMainWindow(self):
        return self.m_main_win


    # Most methods are simply delegated to the self.m_main_win object. We can
    # do some Python magic to make that a lot easier to implement, but I think
    # it is better to keep real methods here so the method signatures and
    # docstrings  are mor visible to the users of this class.

    def GetCount(self):
        """get the total number of items in the control"""
        return self.m_main_win.GetCount()

    def GetIndent(self):
        return self.m_main_win.GetIndent()

    def SetIndent(self, indent):
        """
        The indent is the number of pixels the children are indented relative
        to the parent's position.
        """
        self.m_main_win.SetIndent(indent)

    def GetLineSpacing(self):
        return self.m_main_win.GetLineSpacing()

    def SetLineSpacing(self, spacing):
        """
        The line spacing is the space above and below the text on each line.
        """
        self.m_main_win.SetLineSpacing(spacing)

    def GetImageList(self):
        return self.m_main_win.GetImageList()

    def GetStateImageList(self):
        return self.m_main_win.GetStateImageList()

    def GetButtonsImageList(self):
        return self.m_main_win.GetButtonsImageList()

    def SetImageList(self, imageList):
        self.m_main_win.SetImageList(imageList)

    def SetStateImageList(self, imageList):
        self.m_main_win.SetStateImageList(imageList)

    def SetButtonsImageList(self, imageList):
        self.m_main_win.SetButtonsImageList(imageList)

    def AssignImageList(self, imageList):
        self.m_main_win.AssignImageList(imageList)

    def AssignStateImageList(self, imageList):
        self.m_main_win.AssignStateImageList(imageList)

    def AssignButtonsImageList(self, imageList):
        self.m_main_win.AssignButtonsImageList(imageList)

    def GetItemText(self, item, column=-1):
        if column < 0:
            column = self.GetMainColumn()
        return self.m_main_win.GetItemText(item, column)

    def GetItemImage(self, item, column=-1, which=wx.TreeItemIcon_Normal):
        if column < 0:
            column = self.GetMainColumn()
        return self.m_main_win.GetItemImage(item, column, which)

    def GetItemData(self, item):
        return self.m_main_win.GetItemData(item)

    def GetItemBold(self, item):
        return self.m_main_win.GetItemBold(item)

    def GetItemTextColour(self, item):
        return self.m_main_win.GetItemTextColour(item)

    def GetItemBackgroundColour(self, item):
        return self.m_main_win.GetItemBackgroundColour(item)

    def GetItemFont(self, item):
        return self.m_main_win.GetItemFont(item)

    def SetItemText(self, item, text, column=-1):
        if column < 0:
            column = self.GetMainColumn()
        self.m_main_win.SetItemText(item, text, column)

    def SetItemImage(self, item, image, column=-1, which=wx.TreeItemIcon_Normal):
        if column < 0:
            column = self.GetMainColumn()
        self.m_main_win.SetItemImage(item, image, column, which)

    def SetItemData(self, item, data):
        self.m_main_win.SetItemData(item, data)

    def SetItemHasChildren(self, item, hasChildren=True):
        self.m_main_win.SetItemHasChildren(item, hasChildren)

    def SetItemBold(self, item, bold=True):
        self.m_main_win.SetItemBold(item, bold)

    def SetItemTextColour(self, item, colour):
        self.m_main_win.SetItemTextColour(item, colour)

    def SetItemBackgroundColour(self, item, colour):
        self.m_main_win.SetItemBackgroundColour(item, colour)

    def SetItemFont(self, item, font):
        self.m_main_win.SetItemFont(item, font)

    def SetFont(self, font):
        if self.m_header_win:
            self.m_header_win.SetFont(font)
            self._CalculateAndSetHeaderHeight()
            self.m_header_win.Refresh()

        if self.m_main_win:
            return self.m_main_win.SetFont(font)
        else:
            return False

    def SetWindowStyle(self, style):
        if self.m_main_win:
            self.m_main_win.SetWindowStyle(style)
        super(TreeListCtrl, self).SetWindowStyle(style)
        # TODO: provide something like wxTL_NO_HEADERS to hide m_header_win

    def GetWindowStyle(self):
        style = super(TreeListCtrl, self).GetWindowStyle()
        if self.m_main_win:
            style |= self.m_main_win.GetWindowStyle()
        return style

    def GetWindowStyleFlag(self):
        return self.GetWindowStyle()

    def IsVisible(self, item, fullRow=False):
        return self.m_main_win.IsVisible(item, fullRow)

    def HasChildren(self, item):
        return self.m_main_win.HasChildren(item)

    def IsExpanded(self, item):
        return self.m_main_win.IsExpanded(item)

    def IsSelected(self, item):
        return self.m_main_win.IsSelected(item)

    def IsBold(self, item):
        return self.m_main_win.IsBold(item)

    def GetChildrenCount(self, item, recursive=True):
        return self.m_main_win.GetChildrenCount(item, recursive)

    def GetRootItem(self):
        return self.m_main_win.GetRootItem()

    def GetSelection():
        return self.m_main_win.GetSelection()

    def GetSelections(self): # --> list of items
        return self.m_main_win.GetSelections()

    def GetItemParent(self, item):
        return self.m_main_win.GetItemParent(item)

    def GetCurrentItem(self):
        return self.m_main_win.GetCurrentItem()

    def SetCurrentItem(self, newItem):
        self.m_main_win.SetCurrentItem(newItem)


    def GetFirstChild(self, item): # --> item, cookie
        return self.m_main_win.GetFirstChild(item)

    def GetNextChild(self, item, cookie): # --> item, cookie
        return self.m_main_win.GetNextChild(item, cookie)

    def GetPrevChild(self, item, cookie): # --> item, cookie
        return self.m_main_win.GetPrevChild(item, cookie)

    def GetLastChild(self, item): # --> item, cookie
        return self.m_main_win.GetLastChild(item)


    def GetNextSibling(self, item):
        return self.m_main_win.GetNextSibling(item)

    def GetPrevSibling(self, item):
        return self.m_main_win.GetPrevSibling(item)

    def GetNext(self, item):
        return self.m_main_win.GetNext(item, True)

    def GetPrev(self, item):
        return self.m_main_win.GetPrev(item, True)


    def GetFirstExpandedItem(self):
        return self.m_main_win.GetFirstExpandedItem()

    def GetNextExpanded(self, item):
        return self.m_main_win.GetNextExpanded(item)

    def GetPrevExpanded(self, item):
        return self.m_main_win.GetPrevExpanded(item)

    def GetFirstVisibleItem(self, fullRow):
        return self.m_main_win.GetFirstVisibleItem(fullRow)

    def GetNextVisible(self, item, fullRow):
        return self.m_main_win.GetNextVisible(item, fullRow)

    def GetPrevVisible(self, item, fullRow):
        return self.m_main_win.GetPrevVisible(item, fullRow)


    def AddRoot(self, text, image=-1, selectedImage=-1, data=None):
        return self.m_main_win.AddRoot(text, image, selectedImage, data)

    def PrependItem(self, parent, text, image=-1, selectedImage=-1, data=None):
        return self.m_main_win.PrependItem(parent, text, image, selectedImage, data)

    def InsertItem(self, parent, previous_or_index, text, image=-1, selectedImage=-1, data=None):
        return self.m_main_win.InsertItem(parent, previous_or_index, text, image,
                                          selectedImage, data);

    def AppendItem(self, parent, text, image=-1, selectedImage=-1, data=None):
        return self.m_main_win.AppendItem(parent, text, image, selectedImage, data)


    def Delete(self, item):
        self.m_main_win.Delete(item)

    def DeleteChildren(self, item):
        self.m_main_win.DeleteChildren(item)

    def DeleteRoot(self):
        self.m_main_win.DeleteRoot()

    def Expand(self, item):
        self.m_main_win.Expand(item)

    def ExpandAll(self, item):
        self.m_main_win.ExpandAll(item)

    def Collapse(self, item):
        self.m_main_win.Collapse(item)

    def CollapseAndReset(self, item):
        self.m_main_win.CollapseAndReset(item)

    def Toggle(self, item):
        self.m_main_win.Toggle(item)

    def Unselect(self):
        self.m_main_win.Unselect()

    def UnselectAll(self):
        self.m_main_win.UnselectAll()

    def SelectItem(self, item, last=None, unselect_others=True):
        self.m_main_win.SelectItem (item, last, unselect_others)

    def SelectAll(self):
        self.m_main_win.SelectAll()

    def EnsureVisible(self, item):
        self.m_main_win.EnsureVisible(item)

    def ScrollTo(self, item):
        self.m_main_win.ScrollTo(item)

    def HitTest(self, pos): # --> item, flags, column
        return self.m_main_win.HitTest(pos)

    def GetBoundingRect(self, item, textOnly=False): # --> rect or None
        return self.m_main_win.GetBoundingRect(item, textOnly)

    def EditLabel(self, item, column=-1):
        if column < 0:
            column = self.GetMainColumn()
        self.m_main_win.EditLabel(item, column)


    def SortChildren(self, item):
        self.m_main_win.SortChildren(item)

    def FindItem(self, item, text, mode=TL_MODE_FIND_EXACT):
        return self.m_main_win.FindItem(item, text, mode)

    def SetDragItem(self, item=None):
        self.m_main_win.SetDragItem(item)


    def SetBackgroundColour(self, colour):
        if not self.m_main_win:
            return False
        return self.m_main_win.SetBackgroundColour(colour)

    def SetForegroundColour(self, colour):
        if not self.m_main_win:
            return False
        return self.m_main_win.SetForegroundColour(colour)


    def GetColumnCount(self):
        return self.m_main_win.GetColumnCount()

    def SetColumnWidth(self, column, width):
        if width == wx.LIST_AUTOSIZE_USEHEADER:
            font = m_header_win.GetFont()
            width,_,_,_ = self.m_header_win.GetFullTextExtent(
                self.m_header_win.GetColumnText(column), font)
            # search _TreeListHeaderWindow.OnPaint to understand this:
            width += 2*_const.EXTRA_WIDTH + _const.MARGIN
        elif width == wx.LIST_AUTOSIZE:
            width = self.m_main_win.GetBestColumnWidth(column)

        self.m_header_win.SetColumnWidth(column, width)
        self.m_header_win.Refresh()

    def GetColumnWidth(self, column):
        return m_header_win.GetColumnWidth(column)


    def SetMainColumn(self, column):
        self.m_main_win.SetMainColumn(column)

    def GetMainColumn(self):
        return self.m_main_win.GetMainColumn()

    def SetColumnText(self, column, text):
        self.m_header_win.SetColumnText(column, text)
        self.m_header_win.Refresh()

    def GetColumnText(self, column):
        return self.m_header_win.GetColumnText(column)


    def AddColumn(self, *args, **kw):
        if isinstance(args[0], TreeListColumnInfo):
            self.m_header_win.AddColumn(args[0])
        else:
            colInfo = TreeListColumnInfo(*args, **kw)
            self.m_header_win.AddColumn(colInfo)
        self._DoHeaderLayout()

    def InsertColumn(self, before, *args, **kw):
        if isinstance(args[0], TreeListColumnInfo):
            self.m_header_win.InsertColumn(before, args[0])
        else:
            colInfo = TreeListColumnInfo(*args, **kw)
            self.m_header_win.InsertColumn(before, colInfo)
        self.m_header_win.Refresh()

    def RemoveColumn(self, column):
        self.m_header_win.RemoveColumn(column)
        self.m_header_win.Refresh()

    def SetColumn(self, column, colInfo):
        self.m_header_win.SetColumn(column, colInfo)
        self.m_header_win.Refresh()

    def GetColumn(self, column):
        return self.m_header_win.GetColumn(column)

    def SetColumnImage(self, column, image):
        self.m_header_win.SetColumn(column, self.GetColumn(column).SetImage(image))
        self.m_header_win.Refresh()

    def GetColumnImage(self, column):
        return self.m_header_win.GetColumn(column).GetImage()

    def SetColumnEditable(self, column, edit=True):
        self.m_header_win.SetColumn(column, self.GetColumn(column).SetEditable(edit))

    def SetColumnShown(self, column, shown=True):
        assert column != self.GetMainColumn(), "The main column may not be hidden"
        self.m_header_win.SetColumn(
            column, self.GetColumn(column).SetShown(True if self.GetMainColumn()==column else shown))
        m_header_win.Refresh()

    def IsColumnEditable(self, column):
        return self.m_header_win.GetColumn(column).IsEditable()

    def IsColumnShown(self, column):
        return self.m_header_win.GetColumn(column).IsShown()

    def SetColumnAlignment(self, column, flag):
        self.m_header_win.SetColumn(column, self.GetColumn(column).SetAlignment(flag))
        self.m_header_win.Refresh()

    def GetColumnAlignment(self, column):
        return self.m_header_win.GetColumn(column).GetAlignment()

    def Refresh(self, erase=True, rect=None):
        self.m_main_win.Refresh(erase, rect)
        m_header_win.Refresh(erase, rect)


    def SetFocus(self):
        self.m_main_win.SetFocus()

    def DoGetBestSize(self):
        # something is better than nothing...
        return wx.Size(200,200)  # TODO, something better

    def OnGetItemText(self, item, column):
        return ""

    def OnCompareItems(self, item1, item2):
        # do the comparison here, and not delegate to self.m_main_win, in order
        # to let the user override it
        return cmp(self.GetItemText(item1), self.GetItemText(item2))



#--------------------------------------------------------------------------
#--------------------------------------------------------------------------

class TreeListColumnInfo(wx.Object):
    def __init__(self, *args, **kw):
        super(TreeListColumnInfo, self).__init__()
        if args and isinstance(args[0], TreeListColumnInfo):
            self._init_copy(*args)
        else:
            self._init_default(*args, **kw)

    def _init_default(self, text="", width=DEFAULT_COL_WIDTH, flag=wx.ALIGN_LEFT,
                      image=NO_IMAGE, shown=True, edit=False):
        self.m_text = text
        self.m_width = width
        self.m_flag = flag
        self.m_image = image
        self.m_selected_image = NO_IMAGE
        self.m_shown = shown
        self.m_edit = edit


    def _init_copy(self, other):
        self.m_text = other.m_text
        self.m_width = other.m_width
        self.m_flag = other.m_flag
        self.m_image = other.m_image
        self.m_selected_image = other.m_selected_image
        self.m_shown = other.m_shown
        self.m_edit = other.m_edit


    def GetText(self): return self.m_text
    def SetText(self, text):
        self.m_text = text
        return self

    def GetWidth(self): return self.m_width
    def SetWidth(self, width):
        self.m_width = width
        return self

    def GetAlignment(self): return self.m_flag
    def SetAlignment(self, flag):
        self.m_flag = flag
        return self

    def GetImage(self): return self.m_image
    def SetImage(self, image):
        self.m_image = image
        return self

    def GetSelectedImage(self): return self.m_selected_image
    def SetSelectedImage(self, image):
        self.m_selected_image = image
        return self

    def IsEditable(self): return self.m_edit
    def SetEditable(self, edit):
        self.m_edit = edit
        return self

    def IsShown(self): return self.m_shown
    def SetShown(self, shown):
        self.m_shown = shown
        return self

#--------------------------------------------------------------------------

class TreeListItem(object):
    def __init__(self, owner=None, parent=None, text=None,
                 image=NO_IMAGE, selImage=NO_IMAGE, data=None):
        self.m_owner=owner
        self.m_parent=parent
        self.m_children = []
        self.m_data=data

        if text:
            self.m_text=text
        else:
            self.m_text = list()

        self.m_images = [NO_IMAGE] * wx.TreeItemIcon_Max
        self.m_images[wx.TreeItemIcon_Normal] = image
        self.m_images[wx.TreeItemIcon_Selected] = selImage
        self.m_col_images = []

        self.m_x = 0
        self.m_y = 0
        self.m_text_x = 0

        self.m_isCollapsed = True
        self.m_hasHilight = False
        self.m_hasPlus = False
        self.m_isBold = False

        self.m_attr = None

        self.m_width = 0
        self.m_height = 0


    def GetText(self, column=0):
        if not len(self.m_text):
            return ""
        if self.IsVirtual():
            return self.m_owner.GetItemText(self.m_data, column)
        else:
            return self.m_text[column]


    def GetImage(self, which=wx.TreeItemIcon_Normal, column=None):
        if column if None:
            return self.m_images[which]
        if column == self.m_owner.GetMainColumn():
            return self.m_images[which]
        if column < len(self.m_col_images):
            return self.m_col_images[column]
        return NO_IMAGE


    def SetText(self, text, column=None):
        if column is None:
            if len(self.m_text) > 0:
                self.m_text[0] = text
        else:
            if column < len(self.m_text):
                self.m_text[column] = text
            elif column < self.m_owner.GetColumnCount():
                howmany = self.m_owner.GetColumnCount()
                while len(self.m_text) < howmany:
                    self.m_text.append('')
                self.m_text[column] = text


    def SetImage(self, image, which, column=None):
        if column is None:
            self.m_images[which] = image
        elif column == self.m_owner.GetMainColumn():
            self.m_images[which] = image
        elif column < len(self.m_col_images):
            self.m_col_images[column] = image
        elif column < self.m_owner.GetColumnCount():
            howmany = self.m_owner.GetColumnCount()
            while len(self.m_col_images) < howmany:
                self.m_col_images.append(NO_IMAGE)
            self.m_col_images[column] = image


    def GetData(self): return self.m_data
    def SetData(self, data): self.m_data = data

    def SetHasPlus(self, has=True): self.m_hasPlus = has
    def SetBold(self, bold=True): self.m_isBold = bold

    def GetX(self): return self.m_x
    def GetY(self): return self.m_y
    def SetX(self, x): self.m_x = x
    def SetY(self, y): self.m_y = y

    def GetHeight(self): return self.m_height
    def GetWidth(self):  return self.m_width
    def SetHeight(self, height): self.m_height = height
    def SetWidth(self, width): self.m_width = width

    def GetTextX(self): return self.m_text_x
    def SetTextX(self, text_x): self.m_text_x = text_x

    def GetItemParent(self): return self.m_parent
    def GetChildren(self): return self.m_children


    def Expand(self): self.m_isCollapsed = False
    def Collapse(self): self.m_isCollapsed = True

    def SetHilight(self, hilight=True): self.m_hasHilight = hilight

    def HasChildren(self):  return len(self.m_children) != 0
    def IsSelected(self):   return self.m_hasHilight
    def IsExpanded(self):   return not self.m_isCollapsed
    def HasPlus(self):      return self.m_hasPlus or self.HasChildren()
    def IsBold(self):       return self.m_isBold
    def IsVirtual(self):    return self.m_owner.IsVirtual()


    def GetAttributes(self): return self.m_attr
    def Attr(self):
        if not self.m_attr:
            self.m_attr = TreeItemAttr()
        return self.m_attr
    def SetAttributes(self, attr): self.m_attr = attr
    def AssignAttributes(self, attr): self.m_attr = attr


    def DeleteChildren(self, tree=None):
        for child in self.m_children:
            if tree
                tree.SendDeleteEvent(child)
                if tree.m_selectItem == child:
                    tree.m_selectItem = None
                if tree.m_curItem == child:
                    tree.m_curItem = self
            child.DeleteChildren(tree)
        self.m_children = []


    def GetChildrenCount(self, recursively=True):
        count = len(self.m_children)
        if not recursively:
            return count

        total = count
        for child in self.m_children:
            total += child.GetChildrenCount(recursively)
        return total


    def Insert(self, child, index):
        self.m_children.insert(index, child)


    def GetSize(self, x, y, mainWindow): # -. x,y
        bottomY = self.m_y + mainWindow.GetLineHeight(self)
        if y < bottomY:
            y = bottomY
        width = self.m_x +  self.m_width
        if x < width:
            x = width

        if self.IsExpanded():
            for child in self.m_children:
                x, y = child.GetSize (x, y, mainWindow)

        return x, y


    def HitTest(self, point, theCtrl, level): # --> item, flags, column
        flags = 0
        column = -1
        header_win = theCtrl.m_owner.GetHeaderWindow()

        # for a hidden root node, don't evaluate it, but do evaluate children
        if not theCtrl.HasFlag(wx.TR_HIDE_ROOT) or level > 0:

            # check for right of all columns (outside)
            if point.x > header_win.GetWidth():
                return None, flags, column

            # evaluate if y-pos is okay
            h = theCtrl.GetLineHeight(self)
            if point.y >= self.m_y and point.y <= self.m_y + h:

                maincol = theCtrl.GetMainColumn()

                # check for above/below middle
                y_mid = self.m_y + h/2
                if point.y < y_mid:
                    flags |= wx.TREE_HITTEST_ONITEMUPPERPART
                else:
                    flags |= wx.TREE_HITTEST_ONITEMLOWERPART

                # check for button hit
                if self.HasPlus() and theCtrl.HasButtons():
                    bntX = self.m_x - theCtrl.m_btnWidth2
                    bntY = y_mid - theCtrl.m_btnHeight2
                    if ((point.x >= bntX) and (point.x <= (bntX + theCtrl.m_btnWidth)) and
                            (point.y >= bntY) && (point.y <= (bntY + theCtrl.m_btnHeight))):
                        flags |= wx.TREE_HITTEST_ONITEMBUTTON
                        column = maincol
                        return self, flags, column

                # check for image hit
                if theCtrl.m_imgWidth > 0:
                    imgX = self.m_text_x - theCtrl.m_imgWidth - _const.MARGIN
                    int imgY = y_mid - theCtrl.m_imgHeight2;
                    if ((point.x >= imgX) and (point.x <= (imgX + theCtrl.m_imgWidth)) and
                            (point.y >= imgY) and (point.y <= (imgY + theCtrl.m_imgHeight))):
                        flags |= wx.TREE_HITTEST_ONITEMICON
                        column = maincol
                        return self, flags, column

                # check for label hit
                if point.x >= self.m_text_x and point.x <= (self.m_text_x + self.m_width):
                    flags |= wx.TREE_HITTEST_ONITEMLABEL
                    column = maincol
                    return self, flags, column

                # check for indent hit after button and image hit
                if point.x < self.m_x:
                    flags |= wx.TREE_HITTEST_ONITEMINDENT
                    column = -1 # considered not belonging to main column
                    return self, flags, column

                # check for right of label
                end = 0
                for i in range(maincol+1):
                    end += header_win.GetColumnWidth(i)
                if point.x > (self.m_text_x + self.m_width) and point.x <= end:
                    flags |= wx.TREE_HITTEST_ONITEMRIGHT
                    column = -1 # considered not belonging to main column
                    return self, flags, column

                # else check for each column except main
                x = 0
                for j in range(theCtrl.GetColumnCount()):
                    if not header_win.IsColumnShown(j):
                        continue
                    w = header_win.GetColumnWidth(j)
                    if j != maincol and point.x >= x and point.x < x+w:
                        flags |= wx.TREE_HITTEST_ONITEMCOLUMN
                        column = j
                        return this, flags, column
                    x += w

                # no special flag or column found
                return this, flags, column

            # if children not expanded, return no item
            if not self.IsExpanded():
                return None, flags, column

        # in any case evaluate children
        for child in self.m_children:
            child, flags, column = child.HitTest(point, theCtrl, flags, column, level+1)
            if child:
                return child, flags, column

        # not found
        return None, flags, column


    def GetCurrentImage(self):
        image = NO_IMAGE
        if self.IsExpanded():
            if self.IsSelected():
                image = self.GetImage(wx.TreeItemIcon_SelectedExpanded)
            else:
                image = self.GetImage(wx.TreeItemIcon_Expanded)

        else: # not expanded
            if self.IsSelected():
                image = self.GetImage(wx.TreeItemIcon_Selected)
            else:
                image = self.GetImage(wx.TreeItemIcon_Normal)

        # maybe it doesn't have the specific image, try the default one instead
        if image == NO_IMAGE:
            image = self.GetImage()

        return image



#--------------------------------------------------------------------------

# NOTE: This class is in wxWidgets, but it's not declared in the public API.
# It probably could be if needed...

class TreeItemAttr(object):
    def __init__(self, colText=wx.NullColour, colBack=wx.NullColour, font=wx.NullFont):
        self.m_colText = colText
        self.m_colBack = colBack
        self.m_font = font

    def SetTextColour(self, colText): self.m_colText = colText
    def SetBackgroundColour(self, colBack): self.m_colBack = colBack
    def SetFont(self, font): self.m_font = font

    def HasTextColour(self): return self.m_colText.IsOk()
    def HasBackgroundColour(self): return self.m_colBack.IsOk()
    def HasFont(self): return self.m_font.IsOk()

    def GetTextColour(self): return self.m_colText
    def GetBackgroundColour(self): return self.m_colBack
    def GetFont(self):  return self.m_font



#--------------------------------------------------------------------------


class _TreeListHeaderWindow(wx.Window):
    pass

class _TreeListMainWindow(wx.ScrolledWindow):
    pass

class _TreeListRenameTimer(wx.Timer):
    pass

class _EditTextCtrl(wx.TextCtrl):
    pass


#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
