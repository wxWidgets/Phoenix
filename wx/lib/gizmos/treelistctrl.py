
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
        if column is None:
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
            if tree:
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
                            (point.y >= bntY) and (point.y <= (bntY + theCtrl.m_btnHeight))):
                        flags |= wx.TREE_HITTEST_ONITEMBUTTON
                        column = maincol
                        return self, flags, column

                # check for image hit
                if theCtrl.m_imgWidth > 0:
                    imgX = self.m_text_x - theCtrl.m_imgWidth - _const.MARGIN
                    imgY = y_mid - theCtrl.m_imgHeight2
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
    def __init__(self, parent, id, owner, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0, name="wxtreelistctrlcolumntitles"):
        super(_TreeListHeaderWindow, self).__init__(parent, id, pos, size, style, name)
        self.m_owner = owner
        self.m_columns = []

        self.m_currentCursor = None
        self.m_resizeCursor = wx.Cursor(wx.CURSOR_SIZEWE)
        self.m_isDragging = False
        self.m_dirty = False
        self.m_total_col_width = 0
        self.m_hotTrackCol = -1

        self.m_column = -1
        self.m_currentX = -1
        self.m_minX = -1
        self.m_hotTrackCol = -1

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)


    def DoDrawRect(self, dc, x, y, w, h):
        corner = 1
        if 'wxMac' in wx.PlatformInfo:
            pen = wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNSHADOW), 1)
        else:
            pen = wx.BLACK_PEN
        dc.SetPen(pen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        dc.DrawLine( x+w-corner+1, y, x+w, y+h )  # right (outer)
        dc.DrawRectangle( x, y+h, w+1, 1 )          # bottom (outer)

        if 'wxMac' in wx.PlatformInfo:
            pen = wx.Pen( wx.Colour( 0x88 , 0x88 , 0x88 ), 1)

        dc.SetPen( pen )
        dc.DrawLine( x+w-corner, y, x+w-1, y+h )  # right (inner)
        dc.DrawRectangle( x+1, y+h-1, w-2, 1 )      # bottom (inner)

        dc.SetPen( wx.WHITE_PEN )
        dc.DrawRectangle( x, y, w-corner+1, 1 )   # top (outer)
        dc.DrawRectangle( x, y, 1, h )              # left (outer)
        dc.DrawLine( x, y+h-1, x+1, y+h-1 )
        dc.DrawLine( x+w-1, y, x+w-1, y+1 )


    def DrawCurrent(self):
        x1 = self.m_currentX
        y1 = 0
        x1, y1 = self.ClientToScreen(x1, y1)

        x2 = m_currentX-1
        if 'wxMSW' in wx.PlatformInfo:
            x2 += 1 # but why ????

        _, y2 = self.m_owner.GetClientSize()
        x2, y2 = self.m_owner.ClientToScreen( x2, y2 )

        dc = wx.ScreenDC()
        dc.SetLogicalFunction(wx.INVERT)
        dc.SetPen(wx.Pen(wx.BLACK, 2, wx.SOLID))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        self.AdjustDC(dc)
        dc.DrawLine(x1, y1, x2, y2)
        dc.SetLogicalFunction(wxCOPY)
        dc.SetPen(wx.NullPen)
        dc.SetBrush(wx.NullBrush)


    def AdjustDC(self, dc):
        xpix, ypix = self.m_owner.GetScrollPixelsPerUnit()
        x, y = self.m_owner.GetViewStart()

        # account for the horz scrollbar offset
        dc.SetDeviceOrigin( -x * xpix, 0 )


    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        self.PrepareDC( dc )
        self.AdjustDC( dc )

        x = _const.HEADER_OFFSET_X

        # width and height of the entire header window
        w, h = self.GetClientSize()
        w, _ = self.m_owner.CalcUnscrolledPosition(w, 0)
        dc.SetBackgroundMode(wx.TRANSPARENT)

        numColumns = self.GetColumnCount()
        for i in range(numColumns):
            if x >= w:
                break

            if not self.IsColumnShown(i):
                continue # skip to next column if not shown

            params = wx.HeaderButtonParams()

            # TODO: columnInfo should have label colours...
            params.m_labelColour = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
            params.m_labelFont = self.GetFont()

            column = self.GetColumn(i)
            wCol = column.GetWidth()
            flags = 0
            rect = wx.Rect(x, 0, wCol, h)
            x += wCol

            if i == self.m_hotTrackCol:
                flags |= wx.CONTROL_CURRENT

            params.m_labelText = column.GetText()
            params.m_labelAlignment = column.GetAlignment()

            image = column.GetImage()
            imageList = self.m_owner.GetImageList()
            if image != -1 and imageList:
                params.m_labelBitmap = imageList.GetBitmap(image)

            wx.RendererNative.Get().DrawHeaderButton(self, dc, rect, flags,
                                                     wx.HDR_SORT_ICON_NONE, params)

        if x < w:
            rect = wx.Rect(x, 0, w-x, h)
            wx.RendererNative.Get().DrawHeaderButton(self, dc, rect)



    def OnMouse(self, event):
        # we want to work with logical coords
        x, _ = self.m_owner.CalcUnscrolledPosition(event.GetX(), 0)
        y = event.GetY()

        if event.Moving():
            col = self.XToCol(x)
            if col != self.m_hotTrackCol:
                # Refresh the col header so it will be painted with hot tracking
                # (if supported by the native renderer.)
                self.RefreshColLabel(col)

                # Also refresh the old hot header
                if self.m_hotTrackCol >= 0:
                    self.RefreshColLabel(self.m_hotTrackCol)

                self.m_hotTrackCol = col

        if event.Leaving() and self.m_hotTrackCol >= 0:
            # Leaving the window so clear any hot tracking indicator that may be present
            self.RefreshColLabel(self.m_hotTrackCol)
            self.m_hotTrackCol = -1

        if self.m_isDragging:
            self.SendListEvent(wx.wxEVT_COMMAND_LIST_COL_DRAGGING, event.GetPosition())

            # we don't draw the line beyond our window, but we allow dragging it
            # there
            w, _ = self.GetClientSize()
            w, _ = self.m_owner.CalcUnscrolledPosition(w, 0)
            w -= 6

            # erase the line if it was drawn
            if self.m_currentX < w:
                self.DrawCurrent()

            if event.ButtonUp():
                self.m_isDragging = False
                if self.HasCapture():
                    self.ReleaseMouse()
                self.m_dirty = True
                self.SetColumnWidth(self.m_column, self.m_currentX - self.m_minX)
                self.Refresh()
                self.SendListEvent(wx.wxEVT_COMMAND_LIST_COL_END_DRAG, event.GetPosition())
            else:
                self.m_currentX = max(self.m_minX + 7, x)

                # draw in the new location
                if self.m_currentX < w:
                    self.DrawCurrent()

        else: # not dragging
            self.m_minX = 0
            hit_border = False

            # end of the current column
            xpos = 0

            # find the column where this event occurred
            for column in range(self.GetColumnCount()):
                if not self.IsColumnShown(column):
                    continue
                xpos += self.GetColumnWidth(column)
                self.m_column = column
                if abs(x-xpos) < 3 and y < 22:
                    # near the column border
                    hit_border = True
                    break

                if x < xpos:
                    # inside the column
                    break

                self.m_minX = xpos

            if event.LeftDown() and event.RightUp():
                if hit_border and event.LeftDown():
                    self.m_isDragging = True
                    self.CaptureMouse()
                    self.m_currentX = x
                    self.DrawCurrent()
                    self.SendListEvent(wxEVT_COMMAND_LIST_COL_BEGIN_DRAG, event.GetPosition())

                else: # click on a column
                    evt = wx.wxEVT_COMMAND_LIST_COL_CLICK if event.LeftDown() \
                          else wx.wxEVT_COMMAND_LIST_COL_RIGHT_CLICK
                    self.SendListEvent(evt, event.GetPosition())

            elif event.LeftDClick() and hit_border:
                self.SetColumnWidth(self.m_column, self.m_owner.GetBestColumnWidth(self.m_column))
                self.Refresh()

            elif event.Moving():
                if hit_border:
                    setCursor = self.m_currentCursor == wxSTANDARD_CURSOR
                    m_currentCursor = self.m_resizeCursor
                else:
                    setCursor = self.m_currentCursor != wxSTANDARD_CURSOR
                    self.m_currentCursor = wxSTANDARD_CURSOR
                if setCursor:
                    self.SetCursor(self.m_currentCursor)


    def OnSetFocus(self, event):
        self.m_owner.SetFocus()


    def SendListEvent(self, evtType, pos):
        parent = self.GetParent()
        le = wx.ListEvent(evtType, parent.GetId())
        le.SetEventObject(parent)
        # the position should be relative to the parent window, not
        # this one, for compatibility with MSW and common sense: the
        # user code doesn't know anything at all about this header
        # window, so why should it get positions relative to it?
        pos = wx.Point(*pos)
        pos.y -= self.GetSize().y
        le.SetPoint(pos)
        le.SetColumn(self.m_column)
        parent.GetEventHandler().ProcessEvent(le)


    def AddColumn(self, colInfo):
        self.m_columns.append(colInfo)
        self.m_total_col_width += colInfo.GetWidth()
        self.m_owner.AdjustMyScrollbars()
        self.m_owner.m_dirty = True


    def SetColumnWidth(self, column, width):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        self.m_total_col_width -= self.m_columns[column].GetWidth()
        self.m_columns[column].SetWidth(width)
        self.m_total_col_width += width
        self.m_owner.AdjustMyScrollbars()
        self.m_owner.m_dirty = True

    def InsertColumn(self, before, colInfo):
        assert before >= 0 and before < self.GetColumnCount(), "Invalid column";
        self.m_columns.insert(before, colInfo)
        self.m_total_col_width += colInfo.GetWidth()
        self.m_owner.AdjustMyScrollbars()
        self.m_owner.m_dirty = True


    def RemoveColumn(self,  column):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        self.m_total_col_width -= self.m_columns[column].GetWidth()
        del self.m_columns[column]
        self.m_owner.AdjustMyScrollbars()
        self.m_owner.m_dirty = True


    def SetColumn(self, column, colInfo):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        w = self.m_columns[column].GetWidth()
        self.m_columns[column] = colInfo
        if w != colInfo.GetWidth():
            self.m_total_col_width += colInfo.GetWidth() - w
            self.m_owner.AdjustMyScrollbars()
        self.m_owner.m_dirty = True


    def GetWidth(self):
        return self.m_total_col_width


    def GetColumnCount(self):
        return len(self.m_columns)


    def GetColumn(self, column):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        return self.m_columns[column]


    def GetColumnText(self, column):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        return self.m_columns[column].GetText()


    def SetColumnText(self, column, text):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        self.m_columns[column].SetText(text)


    def GetColumnAlignment(self, column):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        return self.m_columns[column].GetAlignment()


    def SetColumnAlignment(self, column, flag):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        self.m_columns[column].SetAlignment(flag)


    def GetColumnWidth(self, column):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        return self.m_columns[column].GetWidth()


    def IsColumnEditable(self, column):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        return self.m_columns[column].IsEditable()


    def IsColumnShown(self, column):
        assert column >= 0 and column < self.GetColumnCount(), "Invalid column"
        return self.m_columns[column].IsShown()


    def XToCol(self, x):
        colLeft = 0
        numColumns = self.GetColumnCount()
        for col in range(numColumns):
            if not self.IsColumnShown(col):
                continue
            column = self.GetColumn(col)
            if x < (colLeft + column.GetWidth()):
                 return col
            colLeft += column.GetWidth()

        return -1


    def RefreshColLabel(self, col):
        if col >= self.GetColumnCount():
            return

        x = 0
        width = 0
        idx = 0
        while idx < col:
            if not self.IsColumnShown(idx):
                continue
            column = self.GetColumn(idx)
            x += width
            width = column.GetWidth()
            idx += 1

        x, _ = self.m_owner.CalcScrolledPosition(x, 0)
        self.RefreshRect(wx.Rect(x, 0, width, self.GetSize().GetHeight()))


#--------------------------------------------------------------------------

class _TreeListMainWindow(wx.ScrolledWindow):
    def __init__(self, parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TR_DEFAULT_STYLE, validator=wx.DefaultValidator,
                 name="wxtreelistmainwindow"):

        if 'wxMac' in wx.PlatformInfo:
            style &= ~wx.TR_LINES_AT_ROOT
            style |= wx.TR_NO_LINES

        super(_TreeListMainWindow, self).__init__(parent, id, pos, size, style, name)
        self.SetValidator(validator)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_LISTBOX))

        if 'wxMSW' in wx.PlatformInfo:
            bmp = wx.Bitmap(8,8)
            bdc = wx.MemoryDC(bmp)
            bdc.SetPen(wx.GREY_PEN)
            bdc.DrawRectangle(-1, -1, 10, 10)
            for i in range(8):
                for j in range(8):
                    if not ((i + j) & 1):
                        bdc.DrawPoint(i, j)
            del bdc
            self.m_dottedPen = wx.Pen(bmp, 1)
        else:
            self.m_dottedPen = wx.Pen("grey", 0, 0)

        self.m_owner = parent
        self.m_main_column = 0

        self.m_rootItem = None
        self.m_curItem = None
        self.m_shiftItem = None
        self.m_editItem = None
        self.m_selectItem = None
        self.m_select_me = None

        self.m_curColumn = -1
        self.m_drag_item = None

        self.m_hasFocus = False
        self.m_dirty = False
        self.m_should_return = False

        self.m_lineHeight = _const.LINEHEIGHT
        self.m_indent = _const.MININDENT
        self.m_linespacing = 4

        self.m_hilightBrush = wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.m_hilightUnfocusedBrush = wx.Brush(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNSHADOW))

        self.m_imageListNormal = None
        self.m_imageListButtons = None
        self.m_imageListState = None
        self.m_ownsImageListNormal = False
        self.m_ownsImageListButtons = False
        self.m_ownsImageListState = False

        self.m_imgWidth = 0
        self.m_imgWidth2 = 0
        self.m_imgHeight = 0
        self.m_imgHeight2 = 0
        self.m_btnWidth = 0
        self.m_btnWidth2 = 0
        self.m_btnHeight = 0
        self.m_btnHeight2 = 0

        self.m_dragCount = 0
        self.m_isDragging = False
        self.m_dragTimer = wx.Timer(self)
        self.m_dragItem = None

        self.m_renameTimer = _TreeListRenameTimer(self)
        self.m_lastOnSame = False
        self.m_left_down_selection = False

        self.m_findTimer = wx.Timer(self)

        ##if defined( __WXMAC__ ) && defined(__WXMAC_CARBON__)
        #    m_normalFont.MacCreateFromThemeFont (kThemeViewsFont);
        ##else
        self.m_normalFont = nf = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.m_boldFont = wxFont( m_normalFont.GetPointSize(),
                             #(m_normalFont.GetFamily() != wxFONTFAMILY_UNKNOWN ? m_normalFont.GetFamily() : wxSWISS),
                             nf.GetFamily() if nf.GetFamily() != wx.FONTFAMILY_UNKNOWN else wx.FONTFAMILY_SWISS,
                             nf.GetStyle(),
                             wx.FONTWEIGHT_BOLD,
                             nf.GetUnderlined(),
                             nf.GetFaceName(),
                             nf.GetEncoding())

        self.Bind(wx.EVT_PAINT,        self.OnPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)
        self.Bind(wx.EVT_CHAR,         self.OnChar)
        self.Bind(wx.EVT_SET_FOCUS,    self.OnSetFocus)
        self.Bind(wx.EVT_KILL_FOCUS,   self.OnKillFocus)
        self.Bind(wx.EVT_IDLE,         self.OnIdle)
        self.Bind(wx.EVT_SCROLLWIN,    self.OnScroll)


    def __dtor__(self):
        self.m_dragTimer.Stop()
        self.m_renameTimer.Stop()
        self.m_findTimer.Stop()
        self.DeleteRoot()


    def IsVirtual(self):
        return self.HasFlag(TR_VIRTUAL)

    def GetCount(self):
        return 0 if self.m_rootItem is None else self.m_rootItem.GetChildrenCount()

    def GetIndent(self):
        return self.m_indent

    def SetIndent(self, indent):
        self.m_indent = max(_const.MININDENT, indent)
        self.m_dirty = True

    def GetLineSpacing(self):
        return self.m_linespacing

    def SetLineSpacing(self, spacing):
        self.m_linespacing = spacing
        self.m_dirty = True
        self._CalculateLineHeight()


    def GetImageList(self): return self.m_imageListNormal
    def GetStateImageList(self): return self.m_imageListState
    def GetButtonsImageList(self): return self.m_imageListButtons


    def SetImageList(self, imageList): pass #TODO
    def SetStateImageList(self, imageList): pass #TODO
    def SetButtonsImageList(self, imageList): pass #TODO
    def AssignImageList(self, imageList): pass #TODO
    def AssignStateImageList(self, imageList): pass #TODO
    def AssignButtonsImageList(self, imageList): pass #TODO

    def GetItemText(self, item, column): pass #TODO

    def GetItemImage(self, item, column, which):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.GetImage(column, which)

    def GetItemData(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.GetData()


    def GetItemBold(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.IsBold()

    def GetItemTextColour(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.Attr().GetTextColour()

    def GetItemBackgroundColour(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.Attr().GetBackgroundColour()

    def GetItemFont(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.Attr().GetFont()

    def SetItemText(self, item, column, text): pass #TODO

    def SetItemImage(self, item, column, image, which):
        self._checkItem(item)
        tli = self._id2tli(item)
        tli.SetImage(column, image, which)
        dc = wx.ClientDC(self)
        self._CalculateSize(tli, dc)
        self._RefreshLine(tli)

    def SetItemData(self, item, data):
        self._checkItem(item)
        tli = self._id2tli(item)
        tli.SetData(data)

    def SetItemHasChildren(self, item, hasChildren):
        self._checkItem(item)
        tli = self._id2tli(item)
        tli.SetHasPlus(hasChildren)
        self._RefreshLine(tli)

    def SetItemBold(self, item, bold):
        self._checkItem(item)
        tli = self._id2tli(item)
        if tli.IsBold() != bold:
            tli.SetBold(bold)
            self._RefreshLine(tli)

    def SetItemTextColour(self, item, colour):
        self._checkItem(item)
        tli = self._id2tli(item)
        tli.Attr().SetTextColout(colour)
        self._RefreshLine(tli)

    def SetItemBackgroundColour(self, item, colour):
        self._checkItem(item)
        tli = self._id2tli(item)
        tli.Attr().SetBackgroundColour(colour)
        self._RefreshLine(tli)

    def SetItemFont(self, item, font):
        self._checkItem(item)
        tli = self._id2tli(item)
        tli.Attr().SetFont(font)
        self._RefreshLine(tli)


    def SetFont(self, font):
        super(_TreeListMainWindow, self).SetFont(font)
        self.m_normalFont = font
        self.m_boldFont = wx.Font(font.GetPointSize(),
                                  font.GetFamily(),
                                  font.GetStyle(),
                                  wx.FONTWEIGHT_BOLD,
                                  font.GetUnderlined(),
                                  font.GetFaceName())
        self._CalculateLineHeight()
        return True


    def SetWindowStyle(self, styles):
        super(_TreeListMainWindow, self).SetWindowStyle(styles)
        self.m_dirty = True


    def IsVisible(self, item, fullRow):
        self._checkItem(item)
        tli = self._id2tli(item)
        parent = tli.GetItemParent()
        while parent:
            if parent == self.m_rootItem and self.HasFlag(wx.TR_HIDE_ROOT):
                break
            if not parent.IsExpanded():
                return False
            parent = parent.GetItemParent()

        clientSize = self.GetClientSize()
        rect = self.GetBoundingRect(item)
        if (rect is None or
                (not fullRow and rect.GetWidth() == 0) or
                rect.GetHeight() == 0 or
                rect.GetBottom() < 0 or
                rect.GetTop() > clientSize.height or
                (not fullRow and (rect.GetRight() < 0 or rect.GetLeft() or clientSize.width))):
             return False

        return True


    def HasChildren(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.HasPlus()


    def IsExpanded(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.IsExpanded()


    def IsSelected(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.IsSelected()


    def IsBold(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.IsBold()


    def GetChildrenCount(self, item, recursively):
        self._checkItem(item)
        tli = self._id2tli(item)
        return tli.GetChildrenCount(recursively)


    def GetRootItem(self): return self._tli2id(self.m_rootItem)
    def GetSelection(self): return self._tli2id(self.m_selectItem)
    def GetSelections(self): pass #TODO


    def GetItemParent(self, item):
        self._checkItem(item)
        tli = self._id2tli(item)
        return self._tli2id(tli.GetItemParent())


    def GetFirstChild(self, item): pass #TODO # --> item, cookie
    def GetNextChild(self, item, cookie): pass #TODO # --> item, cookie
    def GetPrevChild(self, item, cookie): pass #TODO # --> item, cookie
    def GetLastChild(self, item): pass #TODO # --> item, cookie
    def GetNextSibling(self, item): pass #TODO
    def GetPrevSibling(self, item): pass #TODO
    def GetNext(self, item): pass #TODO
    def GetPrev(self, item): pass #TODO

    def GetFirstExpandedItem(self): pass #TODO
    def GetNextExpanded(self, item): pass #TODO
    def GetPrevExpanded(self, item): pass #TODO
    def GetFirstVisibleItem(self, fullRow): pass #TODO
    def GetNextVisible(self, item, fullRow): pass #TODO
    def GetPrevVisible(self, item, fullRow): pass #TODO

    def AddRoot(self, text, image, selectedImage, data): pass #TODO
    def PrependItem(self, parent, text, image, selectedImage, data): pass #TODO
    def InsertItem(self, parent, previous_or_index, text, image, selectedImage, data): pass #TODO
    def AppendItem(self, parent, text, image, selectedImage , data): pass #TODO

    def Delete(self, item): pass #TODO
    def DeleteChildren(self, item): pass #TODO
    def DeleteRoot(self): pass #TODO

    def Expand(self, item): pass #TODO
    def ExpandAll(self, item): pass #TODO
    def Collapse(self, item): pass #TODO
    def CollapseAndReset(self, item): pass #TODO
    def Toggle(self, item): pass #TODO

    def Unselect(self): pass #TODO
    def UnselectAll(self): pass #TODO
    def SelectItem(self, item, prev, unselect_others): pass #TODO
    def SelectAll(self): pass #TODO

    def EnsureVisible(self, item): pass #TODO
    def ScrollTo(self, item): pass #TODO
    def AdjustMyScrollbars(self): pass #TODO

    def HitTest(self, pos): pass #TODO # --> item, flags, column
    def GetBoundingRect(self, item, textOnly): pass #TODO # --> rect or None

    def EditLabel(self, item, column): pass #TODO

    def OnCompareItems(self, item1, item2): pass #TODO
    def SortChildren(self, item): pass #TODO

    def FindItem(self, item, text, mode): pass #TODO

    def SetBackgroundColour(self, colour): pass #TODO
    def SetForegroundColour(self, colour): pass #TODO

    def SetDragItem(self, item): pass #TODO

    def OnPaint( self, event ): pass #TODO
    def OnSetFocus( self, event ): pass #TODO
    def OnKillFocus( self, event ): pass #TODO
    def OnChar( self, event ): pass #TODO
    def OnMouse( self, event ): pass #TODO
    def OnIdle( self, event ): pass #TODO
    def OnScroll(self, event): pass #TODO

    def SendDeleteEvent(self, itemBeingDeleted): pass #TODO

    def GetColumnCount(self):
        return self.m_owner.GetHeaderWindow().GetColumnCount()

    def SetMainColumn(self, column):
        if column >= 0 and column < self.GetColumnCount():
            self.m_main_column = column

    def GetMainColumn(self):
        return self.m_main_column

    def GetBestColumnWidth(self, column, parent=wx.TreeItemId()): pass #TODO
    def GetItemWidth(self, column, item): pass #TODO

    def SetFocus(self): pass #TODO

    def GetCurrentItem(self):
        return self.m_curItem

    def SetCurrentItem(self, newItem):
        oldItem = self.m_curItem
        self.m_curItem = newItem.m_pItem
        if oldItem:
            self._RefreshLine(oldItem)


    def _DoInsertItem(self, parent, previous, text, image, selectedImage, data): pass #TODO
    def _HasButtons(self):
        return self.m_imageListButtons or self.HasFlag(wx.TR_TWIST_BUTTONS|wx.TR_HAS_BUTTONS)

    def _CalculateLineHeight(self): pass #TODO
    def _GetLineHeight(self, item): pass #TODO
    def _PaintLevel(self, item, dc, level, y, x_maincol): pass #TODO # return y?
    def _PaintItem(self, item, dc): pass #TODO

    def _CalculateLevel(self, item, dc, level, y, x_maincol): pass #TODO # return y?
    def _CalculatePositions(self): pass #TODO
    def _CalculateSize(self, item, dc): pass #TODO

    def _RefreshSubtree(self, item): pass #TODO
    def _RefreshLine(self, item): pass #TODO

    def _RefreshSelected(self): pass #TODO
    def _RefreshSelectedUnder(self, item): pass #TODO

    def _OnRenameTimer(self): pass #TODO
    def _OnRenameAccept(self): pass #TODO

    def _FillArray(self, item, items): pass #TODO # return list instead?
    def _TagAllChildrenUntilLast(self, crt_item, last_item): pass #TODO
    def _TagNextChildren(self, crt_item, last_item): pass #TODO
    def _UnselectAllChildren(self, item): pass #TODO

    def _checkItem(self, item):
        assert item.IsOk(), "invalid tree item"

    def _id2tli(self, item):
        return TreeListItem() # TODO

    def _tli2id(self, item):
        return wx.TreeItemId() # TODO

#--------------------------------------------------------------------------

class _TreeListRenameTimer(wx.Timer):
    pass

#--------------------------------------------------------------------------

class _EditTextCtrl(wx.TextCtrl):
    pass


#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
