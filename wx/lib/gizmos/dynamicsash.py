#----------------------------------------------------------------------
# Name:        wx.lib.gizmos.dynamicsash
# Purpose:     A Python port of the C++ wxDynamicSashWindow from the
#              old wxCode library.
#
# Author:      Robin Dunn
#
# Created:     30-Oct-2017
# Copyright:   (c) 2017 by Total Control Software
# Licence:     wxWindows license
# Tags:
#----------------------------------------------------------------------
"""
A window which can be dynamically split to an arbitrary depth and later
reunified through the user interface.
"""

import wx
import wx.siplib

#----------------------------------------------------------------------------
# Styles

# DS_MANAGE_SCROLLBARS is a default style of DynamicSashWindow which
# will cause it to respond to scrollbar events for your application by
# automatically scrolling the child view.
DS_MANAGE_SCROLLBARS = 0x0010

# DS_DRAG_CORNER style indicates that the views can also be resized by
# dragging the corner piece between the scrollbars, and which is reflected up
# to the frame if necessary.
DS_DRAG_CORNER = 0x0020

# Default style
DS_DEFAULT = DS_MANAGE_SCROLLBARS | DS_DRAG_CORNER


#----------------------------------------------------------------------------
# Events

wxEVT_DYNAMIC_SASH_SPLIT = wx.NewEventType()
wxEVT_DYNAMIC_SASH_UNIFY = wx.NewEventType()

EVT_DYNAMIC_SASH_SPLIT = wx.PyEventBinder(wxEVT_DYNAMIC_SASH_SPLIT, 1)
EVT_DYNAMIC_SASH_UNIFY = wx.PyEventBinder(wxEVT_DYNAMIC_SASH_UNIFY, 1)



class DynamicSashSplitEvent(wx.PyCommandEvent):
    """
    DynamicSashSplitEvents are sent to your view by DynamicSashWindow whenever
    your view is being split by the user.  It is your responsibility to handle
    this event by creating a new view window as a child of the
    DynamicSashWindow.  DynamicSashWindow will automatically reparent it to
    the proper place in its window hierarchy.
    """
    def __init__(self, arg=None):
        super(DynamicSashSplitEvent, self).__init__()
        if isinstance(arg, DynamicSashSplitEvent):
            obj = arg.GetEventObject()
        else:
            obj = arg
        self.SetEventObject(obj)
        self.SetEventType(wxEVT_DYNAMIC_SASH_SPLIT)



class DynamicSashUnifyEvent(wx.PyCommandEvent):
    """
    DynamicSashUnifyEvents are sent to your view by DynamicSashWindow whenever
    the sash which splits your view and its sibling is being reunified such
    that your view is expanding to replace its sibling. You needn't do
    anything with this event if you are allowing DynamicSashWindow to manage
    your view's scrollbars, but it is useful if you are managing the
    scrollbars yourself so that you can keep the scrollbars' event handlers
    connected to your view's event handler class.
    """
    def __init__(self, arg=None):
        super(DynamicSashUnifyEvent, self).__init__()
        if isinstance(arg, DynamicSashUnifyEvent):
            obj = arg.GetEventObject()
        else:
            obj = arg
        self.SetEventObject(obj)
        self.SetEventType(wxEVT_DYNAMIC_SASH_UNIFY)


#----------------------------------------------------------------------------
# The public window class

class DynamicSashWindow(wx.Window):
    """
    A DynamicSashWindow widget manages the way other widgets are viewed. When
    a DynamicSashWindow is first shown, it will contain one child view, a
    viewport for that child, and a pair of scrollbars to allow the user to
    navigate the child view area.  Next to each scrollbar is a small tab.  By
    clicking on either tab and dragging to the appropriate spot, a user can
    split the view area into two smaller views separated by a draggable sash.
    Later, when the user wishes to reunify the two subviews, the user simply
    drags the sash to the side of the window. DynamicSashWindow will
    automatically reparent the appropriate child view back up the window
    hierarchy, and the DynamicSashWindow will have only one child view once
    again.

    As an application developer, you will simply create a DynamicSashWindow
    using either the Create() function or the more complex constructor
    provided below, and then create a view window whose parent is the
    DynamicSashWindow.  The child should respond to DynamicSashSplitEvents --
    perhaps with an OnSplit() event handler -- by constructing a new view
    window whose parent is also the DynamicSashWindow.  That's it!  Now your
    users can dynamically split and reunify the view you provided.

    If you wish to handle the scrollbar events for your view, rather than
    allowing DynamicSashWindow to do it for you, things are a bit more
    complex.  (You might want to handle scrollbar events yourself, if, for
    instance, you wish to scroll a subwindow of the view you add to your
    DynamicSashWindow object, rather than scrolling the whole view.) In this
    case, you will need to construct your DynamicSashWindow without the
    wxDS_MANAGE_SCROLLBARS style and  you will need to use the GetHScrollBar()
    and GetVScrollBar() methods to retrieve the scrollbar controls and call
    SetEventHandler() on them to redirect the scrolling events whenever your
    window is reparented by wxDyanmicSashWindow. You will need to set the
    scrollbars' event handler at three times:

        *  When your view is created When your view receives a
        *  DynamicSashSplitEvent When your view receives a
        *  DynamicSashUnifyEvent

    See the dynsash_switch sample application for an example which does this.
    """

    def __init__(self, *args, **kw):
        """
        Create a new DynamicSashWindow.

        Both the normal constructor style with all parameters, or wxWidgets
        2-phase style default constructor is supported. If the default
        constructor is used then the Create method will need to be called
        later before the widget can actually be used.
        """
        if not args and not kw:
            self._init_default()
        else:
            self._init_full(*args, **kw)


    def _init_default(self):
        super(DynamicSashWindow, self).__init__()
        self._init()

    def _init_full(self, parent, id=wx.ID_ANY,
                   pos=wx.DefaultPosition, size=wx.DefaultSize,
                   style=DS_DEFAULT, name='dynamicSashWindow'):
        super(DynamicSashWindow, self).__init__(parent, id, pos, size, style, name=name)
        self._init()
        self._post_create()


    def Create(self, parent, id=wx.ID_ANY,
               pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=DS_DEFAULT, name='dynamicSashWindow'):
        super(DynamicSashWindow, self).Create(parent, id, pos, size, style, name=name)
        self._post_create()


    def _init(self):
        # set default attributes
        self.m_impl = None


    def _post_create(self):
        self.m_impl = _DynamicSashWindowImpl(self)
        if not self.m_impl.Create():
            self.m_impl.Destroy()
            self.m_impl = None
            return False
        return True


    def __dtor__(self):
        # break possible cycles and etc.
        self.SetEventHandler(self)
        self.m_impl.Destroy()
        self.m_impl = None



    def GetHScrollBar(self, child):
        return self.m_impl.FindScrollBar(child, 0)

    def GetVScrollBar(self, child):
        return self.m_impl.FindScrollBar(child, 1)


    def AddChild(self, child):
        super(DynamicSashWindow, self).AddChild(child)
        self.m_impl.AddChild(child)



#==========================================================================
# Just internal "implementation details" from here down


# DynamicSashWindow works by internally storing a tree of Implementation
# objects (_DynamicSsahWindowImpl) and Leaf objects (_DynamicSashWindowLeaf).
# The DynamicSashWindow has a pointer to one implementation, and each
# implementation either has a pointer to a one leaf (_leaf) or a pointer to
# two children implementation objects (_child[]).  The leaves each are
# responsible for drawing the frame and decorations around one user-provided
# views and for responding to mouse and scrollbar events.
#
# A resulting tree might look something like this:
#
# DynamicSashWindow
#  |
#  +- _DynamicSashWindowImpl
#      |
#      +- _DynamicSashWindowLeaf
#      |   |
#      |   +- user view window
#      |
#      +- _DynamicSashWindowImpl
#          |
#          +- _DynamicSashWindowLeaf
#          |   |
#          |   +- user view window
#          |
#          +- _DynamicSashWindowLeaf
#              |
#              +- user view window
#
# Each time a split occurs, one of the implementation objects removes its
# leaf, generates two new implementation object children, each with a new
# leaf, and reparents the user view which was connected to its old leaf to be
# one of the new leaf's user view, and sends a Split event to the user view in
# the hopes that it will generate a new user view for the other new leaf.
#
# When a unification occurs, an implementation object is replaced by one of
# its children, and the tree of its other child is pruned.
#
# One quirk is that the top-level implementation object (m_top) always keeps a
# pointer to the implementation object where a new child is needed.
# (_add_child_target).  This is so that when a new user view is added to the
# hierarchy, AddChild() is able to reparent the new user view to the correct
# implementation object's leaf.



_wxEVT_DYNAMIC_SASH_REPARENT = wx.NewEventType()
_EVT_DYNAMIC_SASH_REPARENT = wx.PyEventBinder(_wxEVT_DYNAMIC_SASH_REPARENT, 1)


class _DynamicSashReparentEvent(wx.PyEvent):
    def __init__(self, arg=None):
        super(_DynamicSashReparentEvent, self).__init__()
        if isinstance(arg, _DynamicSashReparentEvent):
            obj = arg.GetEventObject()
        else:
            obj = arg
        self.SetEventObject(obj)
        self.SetEventType(_wxEVT_DYNAMIC_SASH_REPARENT)


# enum DynamicSashRegion
_DSR_NONE = 0
_DSR_VERTICAL_TAB = 1
_DSR_HORIZONTAL_TAB = 2
_DSR_CORNER = 3
_DSR_LEFT_EDGE = 4
_DSR_TOP_EDGE = 5
_DSR_RIGHT_EDGE = 6
_DSR_BOTTOM_EDGE = 7

_isMac = 'wxMac' in wx.PlatformInfo

#----------------------------------------------------------------------------

class _DynamicSashWindowImpl(wx.EvtHandler):
    def __init__(self, window):
        super(_DynamicSashWindowImpl, self).__init__()
        self.m_window = window
        self.m_add_child_target = self
        self.m_container = None
        self.m_parent = None
        self.m_top = self
        self.m_child = [None, None]
        self.m_leaf = None
        self.m_dragging = _DSR_NONE
        self.m_split = _DSR_NONE
        self.m_drag_x = -1
        self.m_drag_y = -1
        if _isMac:
            self.m_overlay = wx.Overlay()
            self.DrawSash = self.DrawSash_overlay


    def __dtor__(self):
        # break possible cycles and other cleanup
        if self.m_leaf:
            self.m_leaf.Destroy()
            self.m_leaf = None
        if self.m_child[0]:
            self.m_child[0].Destroy()
            self.m_child[0] = None
        if self.m_child[1]:
            self.m_child[1].Destroy()
            self.m_child[1] = None

        if self.m_container != self.m_window and self.m_container:
            self.m_container.SetEventHandler(self.m_container)
            self.m_container.Destroy()

        self.m_add_child_target = None
        self.m_top = None
        self.m_window = None


    def Create(self):
        if not self.m_container:
            self.m_container = self.m_window

        self.m_container.SetCursor(wx.Cursor(wx.CURSOR_ARROW))

        self.m_leaf = _DynamicSashWindowLeaf(self)
        if not self.m_leaf.Create():
            self.m_leaf.Destroy()
            self.m_leaf = None
            return False

        self.m_container.SetEventHandler(self)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseMove)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnPress)
        self.Bind(wx.EVT_LEFT_UP, self.OnRelease)

        return True


    def AddChild(self, window):
        if self.m_add_child_target and self.m_add_child_target.m_leaf:
            self.m_add_child_target.m_leaf.AddChild(window)


    def DrawSash_overlay(self, x, y, mode):
        if mode in ['press', 'move--']:
            # these are not needed for this implementation
            return

        if mode == 'release':
            dc = wx.ClientDC(self.m_container)
            odc = wx.DCOverlay(self.m_overlay, dc)
            odc.Clear()
            del odc
            self.m_overlay.Reset()

        if mode == 'move':
            dc = wx.ClientDC(self.m_container)
            odc = wx.DCOverlay(self.m_overlay, dc)
            odc.Clear()

            penclr = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DDKSHADOW)
            dc.SetPen(wx.Pen(penclr, 1))
            bshclr = penclr.Get(False) + (0x80,)
            bshclr = wx.Colour(*bshclr)
            dc.SetBrush(wx.Brush(bshclr))

            self._doDrawSash(dc, x, y, False)


    def DrawSash(self, x, y, mode):
        dc = wx.ScreenDC()
        dc.StartDrawingOnTop(self.m_container)

        bmp = wx.Bitmap(8, 8)
        bdc = wx.MemoryDC(bmp)
        bdc.DrawRectangle(-1, -1, 10, 10)
        for i in range(8):
            for j in range(8):
                if (i + j) & 1:
                    bdc.DrawPoint(i, j)
        bdc.SelectObject(wx.NullBitmap)

        brush = wx.Brush(bmp)
        dc.SetBrush(brush)
        dc.SetLogicalFunction(wx.XOR)

        self._doDrawSash(dc, x, y, True)

        dc.EndDrawingOnTop()


    def _doDrawSash(self, dc, x, y, useScreenCoords):
        if (self.m_dragging == _DSR_CORNER
                and (self.m_window.GetWindowStyle() & DS_DRAG_CORNER) != 0):

            cx = cy = 0
            if useScreenCoords:
                cx, cy = self.m_container.ClientToScreen((cx, cy))
                x, y = self.m_container.ClientToScreen((x, y))

            if cx < x and cy < y:
                dc.DrawRectangle(cx - 2, cy - 2, x - cx + 4, 4)
                dc.DrawRectangle(x - 2, cy + 2, 4, y - cy)
                dc.DrawRectangle(cx - 2, cy + 2, 4, y - cy)
                dc.DrawRectangle(cx + 2, y - 2, x - cx - 4, 4)

        else:
            body_w, body_h = self.m_container.GetClientSize()

            if y < 0:
                y = 0
            if y > body_h:
                y = body_h
            if x < 0:
                x = 0
            if x > body_w:
                x = body_w

            if self.m_dragging == _DSR_HORIZONTAL_TAB:
                x = 0
            else:
                y = 0

            if useScreenCoords:
                x, y = self.m_container.ClientToScreen(x, y)

            w = body_w
            h = body_h

            if self.m_dragging == _DSR_HORIZONTAL_TAB:
                dc.DrawRectangle(x, y - 2, w, 4)
            else:
                dc.DrawRectangle(x - 2, y, 4, h)


    def ConstrainChildren(self, px, py):
        layout = wx.LayoutConstraints()
        layout.left.SameAs(self.m_container, wx.Left)
        layout.top.SameAs(self.m_container, wx.Top)

        if self.m_split == _DSR_HORIZONTAL_TAB:
            layout.right.SameAs(self.m_container, wx.Right)
            layout.height.PercentOf(self.m_container, wx.Height, py)
        else:
            layout.bottom.SameAs(self.m_container, wx.Bottom)
            layout.width.PercentOf(self.m_container, wx.Width, px)

        self.m_child[0].m_container.SetConstraints(layout)

        layout = wx.LayoutConstraints()
        layout.right.SameAs(self.m_container, wx.Right)
        layout.bottom.SameAs(self.m_container, wx.Bottom)

        if self.m_split == _DSR_HORIZONTAL_TAB:
            layout.top.Below(self.m_child[0].m_container, 1)
            layout.left.SameAs(self.m_container, wx.Left)
        else:
            layout.left.RightOf(self.m_child[0].m_container, 1)
            layout.top.SameAs(self.m_container, wx.Top)

        self.m_child[1].m_container.SetConstraints(layout)


    def Split(self, px, py):
        self.m_add_child_target = None

        self.m_child[0] = _DynamicSashWindowImpl(self.m_window)
        self.m_child[0].m_container = wx.Window(self.m_container)
        self.m_child[0].m_parent = self
        self.m_child[0].m_top = self.m_top
        self.m_child[0].Create()
        if self.m_leaf.m_child:
            self.m_leaf.m_child.Reparent(self.m_container)
            self.m_child[0].AddChild(self.m_leaf.m_child)

        self.m_child[1] = _DynamicSashWindowImpl(self.m_window)
        self.m_child[1].m_container = wx.Window(self.m_container)
        self.m_child[1].m_parent = self
        self.m_child[1].m_top = self.m_top
        self.m_child[1].Create()

        self.m_split = self.m_dragging
        self.ConstrainChildren(px, py)

        self.m_top.m_add_child_target = self.m_child[1]
        split = DynamicSashSplitEvent(self.m_child[0].m_leaf.m_child)
        self.m_child[0].m_leaf._checkPendingChild()
        self.m_child[0].m_leaf.m_child.GetEventHandler().ProcessEvent(split)

        self.m_child[0].m_leaf.m_vscroll.SetScrollbar(self.m_leaf.m_vscroll.GetThumbPosition(),
                                                      self.m_leaf.m_vscroll.GetThumbSize(),
                                                      self.m_leaf.m_vscroll.GetRange(),
                                                      self.m_leaf.m_vscroll.GetPageSize())
        self.m_child[0].m_leaf.m_hscroll.SetScrollbar(self.m_leaf.m_hscroll.GetThumbPosition(),
                                                      self.m_leaf.m_hscroll.GetThumbSize(),
                                                      self.m_leaf.m_hscroll.GetRange(),
                                                      self.m_leaf.m_hscroll.GetPageSize())
        self.m_child[1].m_leaf.m_vscroll.SetScrollbar(self.m_leaf.m_vscroll.GetThumbPosition(),
                                                      self.m_leaf.m_vscroll.GetThumbSize(),
                                                      self.m_leaf.m_vscroll.GetRange(),
                                                      self.m_leaf.m_vscroll.GetPageSize())
        self.m_child[1].m_leaf.m_hscroll.SetScrollbar(self.m_leaf.m_hscroll.GetThumbPosition(),
                                                      self.m_leaf.m_hscroll.GetThumbSize(),
                                                      self.m_leaf.m_hscroll.GetRange(),
                                                      self.m_leaf.m_hscroll.GetPageSize())
        self.m_leaf.Destroy()
        self.m_leaf = None

        self.m_container.Layout()


    def Unify(self, panel):
        other = 1 if panel == 0 else 0

        if self.m_child[panel].m_leaf:
            child = self.m_child[:]

            self.m_child[0] = self.m_child[1] = None

            self.m_leaf = _DynamicSashWindowLeaf(self)
            self.m_leaf.Create()
            self.m_leaf.m_child = child[panel].m_leaf.m_child

            self.m_leaf.m_vscroll.SetScrollbar(child[panel].m_leaf.m_vscroll.GetThumbPosition(),
                                              child[panel].m_leaf.m_vscroll.GetThumbSize(),
                                              child[panel].m_leaf.m_vscroll.GetRange(),
                                              child[panel].m_leaf.m_vscroll.GetPageSize())
            self.m_leaf.m_hscroll.SetScrollbar(child[panel].m_leaf.m_hscroll.GetThumbPosition(),
                                              child[panel].m_leaf.m_hscroll.GetThumbSize(),
                                              child[panel].m_leaf.m_hscroll.GetRange(),
                                              child[panel].m_leaf.m_hscroll.GetPageSize())
            self.m_add_child_target = None

            event = _DynamicSashReparentEvent(self.m_leaf)
            self.m_leaf.ProcessEvent(event)

            for i in range(2):
                child[i].Destroy()

            self.m_split = _DSR_NONE

            unify = DynamicSashUnifyEvent(self.m_leaf.m_child)
            self.m_leaf.m_child.GetEventHandler().ProcessEvent(unify)

        else:
            self.m_split = self.m_child[panel].m_split

            self.m_child[other].Destroy()

            child_panel = self.m_child[panel]
            self.m_child[0] = child_panel.m_child[0]
            self.m_child[1] = child_panel.m_child[1]

            self.m_child[0].m_parent = self
            self.m_child[1].m_parent = self

            self.m_add_child_target = None
            self.m_child[0].m_container.Reparent(self.m_container)
            self.m_child[1].m_container.Reparent(self.m_container)

            child_panel.m_child[0] = child_panel.m_child[1] = None
            child_panel.Destroy()

            size = self.m_container.GetSize()
            child_size = self.m_child[0].m_container.GetSize()

            self.ConstrainChildren(child_size.GetWidth() * 100.0 / size.GetWidth(),
                                   child_size.GetHeight() * 100.0 / size.GetHeight())

            self.m_container.Layout()


    def Resize(self, x, y):
        h_parent = self.FindParent(_DSR_BOTTOM_EDGE)
        v_parent = self.FindParent(_DSR_RIGHT_EDGE)
        h_unify = -1
        v_unify = -1
        frame = self.FindFrame()

        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if h_parent:
            _, y = self.m_container.ClientToScreen(0, y)
            _, y = h_parent.m_container.ScreenToClient(0, y)

            py = int((y * 100.0) / h_parent.m_container.GetSize().GetHeight() + 0.5)

            if py < 10:
                ho_parent = self.FindParent(_DSR_TOP_EDGE)
                if ho_parent:
                    if self.FindUpperParent(h_parent, ho_parent) == ho_parent:
                        h_unify = 1

                    else:
                        py = int((ho_parent.m_child[0].m_container.GetSize().GetHeight() * 100.0)
                                    / h_parent.m_container.GetSize().GetHeight() + 0.5)
                        h_parent.m_child[0].m_container.GetConstraints().height.PercentOf(
                                h_parent.m_container, wx.Height, py)

                        h_parent = ho_parent
                        h_unify = 0
                else:
                    h_unify = 1

            elif py > 90:
                h_unify = 0
            else:
                h_parent.m_child[0].m_container.GetConstraints().height.PercentOf(
                        h_parent.m_container, wx.Height, py)
                h_parent.m_container.Layout()
        else:
            do_resize = 1
            h_parent = self.FindParent(_DSR_TOP_EDGE)
            if h_parent:
                py = int((y * 100.0) /
                         (h_parent.m_container.GetSize().GetHeight() +
                          y - self.m_container.GetSize().GetHeight()) + 0.5)

                if py < 10:
                    h_unify = 0
            elif y < 64:
                do_resize = 0

            if do_resize:
                size = frame.GetSize()
                frame.SetSize(size.GetWidth(), size.GetHeight() + y - self.m_container.GetSize().GetHeight())

        if v_parent:
            x, _ = self.m_container.ClientToScreen(x, 0)
            x, _ = v_parent.m_container.ScreenToClient(x, 0)

            px = int((x * 100.0) / v_parent.m_container.GetSize().GetWidth() + 0.5)

            if px < 10:
                vo_parent = self.FindParent(_DSR_LEFT_EDGE)
                if vo_parent:
                    if self.FindUpperParent(v_parent, vo_parent) == vo_parent:
                        v_unify = 1
                    else:
                        px = int((vo_parent.m_child[0].m_container.GetSize().GetWidth() * 100.0)
                                    / v_parent.m_container.GetSize().GetWidth() + 0.5)
                        v_parent.m_child[0].m_container.GetConstraints().width.PercentOf(
                                v_parent.m_container, wx.Width, px)

                        v_parent = vo_parent
                        v_unify = 0
                else:
                    v_unify = 1

            elif px > 90:
                v_unify = 0
            else:
                v_parent.m_child[0].m_container.GetConstraints().width.PercentOf(
                        v_parent.m_container, wx.Width, px)
                v_parent.m_container.Layout()
        else:
            do_resize = 1
            v_parent = self.FindParent(_DSR_LEFT_EDGE)
            if v_parent:
                px = int((x * 100.0) /
                         (v_parent.m_container.GetSize().GetWidth() +
                          x - self.m_container.GetSize().GetWidth()) + 0.5)

                if px < 10:
                    v_unify = 0
            elif x < 64:
                do_resize = 0

            if do_resize:
                size = frame.GetSize()
                frame.SetSize(size.GetWidth() + x - self.m_container.GetSize().GetWidth(), size.GetHeight())

        if h_unify != -1 and v_unify != -1:
            parent = self.FindUpperParent(h_parent, v_parent)
            if parent == h_parent:
                h_parent.Unify(h_unify)
            else:
                v_parent.Unify(v_unify)

        elif h_unify != -1:
            h_parent.Unify(h_unify)

        elif v_unify != -1:
            v_parent.Unify(v_unify)


    def FindParent(self, side):
        if self.m_parent is None:
            return None

        if self.m_parent.m_split == _DSR_HORIZONTAL_TAB:
            if side == _DSR_TOP_EDGE and self.m_parent.m_child[1] == self:
                return self.m_parent
            if side == _DSR_BOTTOM_EDGE and self.m_parent.m_child[0] == self:
                return self.m_parent

        elif self.m_parent.m_split == _DSR_VERTICAL_TAB:
            if side == _DSR_LEFT_EDGE and self.m_parent.m_child[1] == self:
                return self.m_parent
            if side == _DSR_RIGHT_EDGE and self.m_parent.m_child[0] == self:
                return self.m_parent

        return self.m_parent.FindParent(side)


    def FindUpperParent(self, sash_a, sash_b):
        win = sash_a.m_container.GetParent()
        while win and not win.IsTopLevel():
            if win == sash_b.m_container:
                return sash_b
            win = win.GetParent()
        return sash_a


    def FindFrame(self):
        win = self.m_window.GetParent()
        while win and not win.IsTopLevel():
            win = win.GetParent()
        return win


    def FindScrollBar(self, child, vert):
        if self.m_child[0] is None and self.m_leaf is None:
            return None

        if not self.m_child[0]:
            return self.m_leaf.FindScrollBar(child, vert)

        ret = self.m_child[0].FindScrollBar(child, vert)
        if not ret:
            ret = self.m_child[1].FindScrollBar(child, vert)

        return ret


    def OnSize(self, event):
        self.m_container.Layout()
        if self.m_leaf:
            self.m_leaf.OnSize(event)


    def OnPaint(self, event):
        if self.m_leaf:
            self.m_leaf.OnPaint(event)
        else:
            dc = wx.PaintDC(self.m_container)
            dc.SetBackground(wx.Brush(self.m_container.GetBackgroundColour(), wx.SOLID))
            dc.Clear()


    def OnMouseMove(self, event):
        if self.m_dragging:
            self.DrawSash(self.m_drag_x, self.m_drag_y, "move--")
            self.m_drag_x = event.x
            self.m_drag_y = event.y
            self.DrawSash(self.m_drag_x, self.m_drag_y, "move")
        elif self.m_leaf:
            self.m_leaf.OnMouseMove(event)


    def OnLeave(self, event):
        if self.m_leaf:
            self.m_leaf.OnLeave(event)


    def OnPress(self, event):
        if self.m_leaf:
            self.m_leaf.OnPress(event)
        else:
            self.m_dragging = self.m_split
            self.m_drag_x = event.x
            self.m_drag_y = event.y
            self.DrawSash(self.m_drag_x, self.m_drag_y, "press")
            self.m_container.CaptureMouse()


    def OnRelease(self, event):
        if ((self.m_dragging == _DSR_CORNER) and
            (self.m_window.GetWindowStyle() & DS_DRAG_CORNER) != 0):

            self.DrawSash(self.m_drag_x, self.m_drag_y, "release")
            self.m_container.ReleaseMouse()

            self.Resize(event.x, event.y)

            self.m_dragging = _DSR_NONE

        elif self.m_dragging:
            self.DrawSash(self.m_drag_x, self.m_drag_y, "release")
            self.m_container.ReleaseMouse()

            size = self.m_container.GetSize()
            px = int((event.x * 100.0) / size.GetWidth() + 0.5)
            py = int((event.y * 100.0) / size.GetHeight() + 0.5)

            if ((self.m_dragging == _DSR_HORIZONTAL_TAB and py >= 10 and py <= 90)
                        or (self.m_dragging == _DSR_VERTICAL_TAB and px >= 10 and px <= 90)):
                if self.m_child[0] == None:
                    self.Split(px, py)
                else:
                    # It would be nice if moving *this* sash didn't implicitly move
                    # the sashes of our children (if any).  But this will do.
                    layout = self.m_child[0].m_container.GetConstraints()
                    if self.m_split == _DSR_HORIZONTAL_TAB:
                        layout.height.PercentOf(self.m_container, wx.Height, py)
                    else:
                        layout.width.PercentOf(self.m_container, wx.Width, px)
                    self.m_container.Layout()
            else:
                if self.m_child[0] != None:
                    if ((self.m_dragging == _DSR_HORIZONTAL_TAB and py <= 10)
                            or (self.m_dragging == _DSR_VERTICAL_TAB and px <= 10)):
                        self.Unify(1)
                    else:
                        self.Unify(0)


            if self.m_split == _DSR_HORIZONTAL_TAB:
                cursor = wx.Cursor(wx.CURSOR_SIZENS)
            elif self.m_split == _DSR_VERTICAL_TAB:
                cursor = wx.Cursor(wx.CURSOR_SIZEWE)
            else:
                cursor = wx.Cursor(wx.CURSOR_ARROW)
            self.m_container.SetCursor(cursor)

            self.m_dragging = _DSR_NONE

        elif self.m_leaf:
            self.m_leaf.OnRelease(event)



#----------------------------------------------------------------------------


class _DynamicSashWindowLeaf(wx.EvtHandler):
    def __init__(self, impl):
        super(_DynamicSashWindowLeaf, self).__init__()
        self.m_impl = impl
        self.m_hscroll = None
        self.m_vscroll = None
        self.m_child = None
        self.m_viewport = None


    def __dtor__(self):
        if self.m_hscroll:
            self.m_hscroll.SetEventHandler(self.m_hscroll)
            self.m_hscroll.Destroy()
        if self.m_vscroll:
            self.m_vscroll.SetEventHandler(self.m_vscroll)
            self.m_vscroll.Destroy()
        if self.m_viewport:
            self.m_viewport.Destroy()


    def Create(self):
        self.m_hscroll = wx.ScrollBar()
        self.m_vscroll = wx.ScrollBar()
        self.m_viewport = wx.Window()

        add_child_target = self.m_impl.m_add_child_target
        self.m_impl.m_add_child_target = None

        success = self.m_hscroll.Create(self.m_impl.m_container, style=wx.SB_HORIZONTAL)
        if success:
            success = self.m_vscroll.Create(self.m_impl.m_container, style=wx.SB_VERTICAL)
        if success:
            success = self.m_viewport.Create(self.m_impl.m_container)

        if not success:
            return False

        self.m_impl.m_add_child_target = add_child_target

        cursor = wx.Cursor(wx.CURSOR_ARROW)
        self.m_hscroll.SetCursor(cursor)
        self.m_vscroll.SetCursor(cursor)
        self.m_viewport.SetCursor(cursor)

        self.m_viewport.Bind(wx.EVT_SIZE, self.OnViewSize)
        self.Bind(_EVT_DYNAMIC_SASH_REPARENT, self.OnReparent)

        if self.m_impl.m_window.GetWindowStyle() & DS_MANAGE_SCROLLBARS:
            for sbar in [self.m_hscroll, self.m_vscroll]:
                sbar.Bind(wx.EVT_SET_FOCUS, self.OnFocus)
                sbar.Bind(wx.EVT_SCROLL_TOP, self.OnScroll)
                sbar.Bind(wx.EVT_SCROLL_BOTTOM, self.OnScroll)
                sbar.Bind(wx.EVT_SCROLL_LINEUP, self.OnScroll)
                sbar.Bind(wx.EVT_SCROLL_LINEDOWN, self.OnScroll)
                sbar.Bind(wx.EVT_SCROLL_PAGEUP, self.OnScroll)
                sbar.Bind(wx.EVT_SCROLL_PAGEDOWN, self.OnScroll)
                sbar.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnScroll)
                sbar.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.OnScroll)

        layout = wx.LayoutConstraints()
        size = self.m_hscroll.GetBestSize()

        layout.left.SameAs(self.m_impl.m_container, wx.Left, 10)
        layout.right.LeftOf(self.m_vscroll)
        layout.bottom.SameAs(self.m_impl.m_container, wx.Bottom, 3)
        layout.height.Absolute(size.GetHeight())
        self.m_hscroll.SetConstraints(layout)

        layout = wx.LayoutConstraints()
        size = self.m_vscroll.GetBestSize()

        layout.top.SameAs(self.m_impl.m_container, wx.Top, 10)
        layout.bottom.Above(self.m_hscroll)
        layout.right.SameAs(self.m_impl.m_container, wx.Right, 3)
        layout.width.Absolute(size.GetWidth())
        self.m_vscroll.SetConstraints(layout)

        layout = wx.LayoutConstraints()
        layout.left.SameAs(self.m_impl.m_container, wx.Left, 3)
        layout.right.LeftOf(self.m_vscroll)
        layout.top.SameAs(self.m_impl.m_container, wx.Top, 3)
        layout.bottom.Above(self.m_hscroll)
        self.m_viewport.SetConstraints(layout)

        self.m_impl.m_container.Layout()
        return True


    def AddChild(self, window):
        if self.m_child:
            self.m_child.Destroy()

        # Since the parent's AddWindow is called during the construction of
        # the C++ part of the child, there isn't a proxy object created for
        # the child window yet. When we later try to use the widget object
        # given here then it will come up as being already deleted (because
        # the real proxy exists now.) So instead of saving the `window` here
        # we'll just save the object's address instead, and then use that to
        # fetch the real proxy object when it's needed later.
        self.m_child = None
        self.m_child_ptr = wx.siplib.unwrapinstance(window)

        # Delay the reparenting until after the AddChild has finished.
        event = _DynamicSashReparentEvent(self)
        self.AddPendingEvent(event)


    def _checkPendingChild(self):
        if hasattr(self, 'm_child_ptr'):
            self.m_child = wx.siplib.wrapinstance(self.m_child_ptr, wx.Object)
            del self.m_child_ptr


    def OnReparent(self, event):
        self._checkPendingChild()
        if self.m_child:
            self.m_child.Reparent(self.m_viewport)
        self.ResizeChild(self.m_viewport.GetSize())


    def GetRegion(self,  x, y):
        size = self.m_impl.m_container.GetSize()
        w = size.GetWidth()
        h = size.GetHeight()
        size = self.m_hscroll.GetSize()
        sh = size.GetHeight()
        size = self.m_vscroll.GetSize()
        sw = size.GetWidth()

        if x >= w - sw - 3 and x < w and y >= h - sh - 3 and y < h:
            return _DSR_CORNER
        if x >= 3 and x < 10 and y >= h - sh - 3 and y < h - 2:
            return _DSR_VERTICAL_TAB
        if x >= w - sw - 3 and x < w - 2 and y >= 3 and y < 10:
            return _DSR_HORIZONTAL_TAB
        if x < 3:
            return _DSR_LEFT_EDGE
        if y < 3:
            return _DSR_TOP_EDGE
        if x >= w - 2:
            return _DSR_RIGHT_EDGE
        if y >= h - 2:
            return _DSR_BOTTOM_EDGE

        return _DSR_NONE


    def ResizeChild(self, size):
        self._checkPendingChild()
        if self.m_child:
            if self.m_impl.m_window.HasFlag(DS_MANAGE_SCROLLBARS):
                best_size = self.m_child.GetBestSize()
                if best_size.GetWidth() < size.GetWidth():
                    best_size.SetWidth(size.GetWidth())
                if best_size.GetHeight() < size.GetHeight():
                    best_size.SetHeight(size.GetHeight())
                self.m_child.SetSize(best_size)

                hpos = self.m_hscroll.GetThumbPosition()
                vpos = self.m_vscroll.GetThumbPosition()

                if hpos < 0:
                    hpos = 0
                if vpos < 0:
                    vpos = 0
                if hpos > best_size.GetWidth() - size.GetWidth():
                    hpos = best_size.GetWidth() - size.GetWidth()
                if vpos > best_size.GetHeight() - size.GetHeight():
                    vpos = best_size.GetHeight() - size.GetHeight()

                self.m_hscroll.SetScrollbar(hpos, size.GetWidth(),
                                            best_size.GetWidth(), size.GetWidth())
                self.m_vscroll.SetScrollbar(vpos, size.GetHeight(),
                                            best_size.GetHeight(), size.GetHeight())

                #  Umm, the scrollbars are doing something insane under GTK+ and subtracting
                #  one from the position I pass in.  This works around that.
                self.m_hscroll.SetThumbPosition(hpos + hpos - self.m_hscroll.GetThumbPosition())
                self.m_vscroll.SetThumbPosition(vpos + vpos - self.m_vscroll.GetThumbPosition())

                pos = self.m_child.GetPosition()
                self.m_viewport.ScrollWindow(-hpos - pos.x, -vpos - pos.y)

            else: # not DS_MANAGE_SCROLLBARS
                self.m_child.SetSize(size)


    def FindScrollBar(self, child, vert):
        self._checkPendingChild()
        if self.m_child == child:
            return self.m_vscroll if vert else self.m_hscroll
        return None


    def OnSize(self, event):
        self.m_impl.m_container.Refresh()


    def OnViewSize(self, event):
        if self.m_viewport is not None:
            self.ResizeChild(self.m_viewport.GetSize())


    def OnPaint(self, event):
        dc = wx.PaintDC(self.m_impl.m_container)
        dc.SetBackground(wx.Brush(self.m_impl.m_container.GetBackgroundColour()))
        dc.Clear()

        highlight = wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT), 1)
        shadow = wx.Pen(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNSHADOW), 1)
        black = wx.Pen(wx.BLACK, 1)

        size = self.m_impl.m_container.GetSize()
        w = size.GetWidth()
        h = size.GetHeight()
        size = self.m_hscroll.GetSize()
        sh = size.GetHeight()
        size = self.m_vscroll.GetSize()
        sw = size.GetWidth()

        dc.SetPen(shadow)
        dc.DrawLine(1, 1, 1, h - 2)
        dc.DrawLine(1, 1, w - 2, 1)
        dc.SetPen(black)
        dc.DrawLine(2, 2, 2, h - 3)
        dc.DrawLine(2, 2, w - 3, 2)
        dc.SetPen(highlight)
        dc.DrawLine(w - 2, 2, w - 2, h - sh - 2)
        dc.DrawLine(w - 2, h - sh - 2, w - sw - 2, h - sh - 2)
        dc.DrawLine(w - sw - 2, h - sh - 2, w - sw - 2, h - 2)
        dc.DrawLine(w - sw - 2, h - 2, 2, h - 2)

        dc.SetPen(highlight)
        dc.DrawLine(w - sw - 2, 8, w - sw - 2, 4)
        dc.DrawLine(w - sw - 2, 4, w - 5, 4)
        dc.SetPen(shadow)
        dc.DrawLine(w - 5, 4, w - 5, 8)
        dc.DrawLine(w - 5, 8, w - sw - 2, 8)
        dc.SetPen(black)
        dc.DrawLine(w - 4, 3, w - 4, 9)
        dc.DrawLine(w - 4, 9, w - sw - 3, 9)

        dc.SetPen(highlight)
        dc.DrawLine(4, h - 5, 4, h - sh - 2)
        dc.DrawLine(4, h - sh - 2, 8, h - sh - 2)
        dc.SetPen(shadow)
        dc.DrawLine(8, h - sh - 2, 8, h - 5)
        dc.DrawLine(8, h - 5, 4, h - 5)
        dc.SetPen(black)
        dc.DrawLine(9, h - sh - 3, 9, h - 4)
        dc.DrawLine(9, h - 4, 3, h - 4)

        cy = (h - sh + h - 6) / 2.0 + 1
        cx = (w - sw + w - 6) / 2.0 + 1
        sy = cy
        while sy > h - sh:
            sy -= 4
        sx = cx
        while sx > w - sw:
            sx -= 4

        for y in range(int(sy), h-2, 4):       #(y = sy; y < h - 2; y += 4)
            for x in range(int(sx), w-2, 4):   #(x = sx; x < w - 2; x += 4)
                if x - cx >= -(y - cy):
                    dc.SetPen(highlight)
                    dc.DrawPoint(x, y)
                    dc.SetPen(shadow)
                    dc.DrawPoint(x + 1, y + 1)



    def OnScroll(self, event):
        self._checkPendingChild()
        nx = -self.m_hscroll.GetThumbPosition()
        ny = -self.m_vscroll.GetThumbPosition()

        if self.m_child:
            pos = self.m_child.GetPosition()
            self.m_viewport.ScrollWindow(nx - pos.x, ny - pos.y)


    def OnFocus(self, event):
        self._checkPendingChild()
        if (event.GetEventObject() == self.m_hscroll or
                event.GetEventObject() == self.m_vscroll):
            self.m_child.SetFocus()


    def OnMouseMove(self, event):
        if self.m_impl.m_dragging:
            return

        region = self.GetRegion(event.x, event.y)

        cursor = wx.Cursor(wx.CURSOR_ARROW)
        if region == _DSR_HORIZONTAL_TAB:
            cursor = wx.Cursor(wx.CURSOR_SIZENS)
        elif region == _DSR_VERTICAL_TAB:
            cursor = wx.Cursor(wx.CURSOR_SIZEWE)
        elif (region == _DSR_CORNER and
              self.m_impl.m_window.GetWindowStyle() & DS_DRAG_CORNER != 0):
            cursor = wx.Cursor(wx.CURSOR_SIZENWSE)

        elif (region == _DSR_LEFT_EDGE or region == _DSR_TOP_EDGE
                    or region == _DSR_RIGHT_EDGE or region == _DSR_BOTTOM_EDGE):
            if self.m_impl.FindParent(region):
                if region == _DSR_LEFT_EDGE or region == _DSR_RIGHT_EDGE:
                    cursor = wx.Cursor(wx.CURSOR_SIZEWE)
                else:
                    cursor = wx.Cursor(wx.CURSOR_SIZENS)

        self.m_impl.m_container.SetCursor(cursor)



    def OnLeave(self, event):
        cursor = wx.Cursor(wx.CURSOR_ARROW)
        self.m_impl.m_container.SetCursor(cursor)



    def OnPress(self, event):
        region = self.GetRegion(event.x, event.y)

        if region == _DSR_CORNER and (self.m_impl.m_window.GetWindowStyle() & DS_DRAG_CORNER) == 0:
            return

        if region == _DSR_HORIZONTAL_TAB or region == _DSR_VERTICAL_TAB or region == _DSR_CORNER:
            self.m_impl.m_dragging = region
            self.m_impl.m_drag_x = event.x
            self.m_impl.m_drag_y = event.y
            self.m_impl.DrawSash(event.x, event.y, "press")
            self.m_impl.m_container.CaptureMouse()

        elif (region == _DSR_LEFT_EDGE or region == _DSR_TOP_EDGE
                    or region == _DSR_RIGHT_EDGE or region == _DSR_BOTTOM_EDGE):
            parent = self.m_impl.FindParent(region)

            if parent:
                x = event.x
                y = event.y

                x, y = self.m_impl.m_container.ClientToScreen(x, y)
                x, y = parent.m_container.ScreenToClient(x, y)

                parent.m_dragging = parent.m_split
                parent.m_drag_x = x
                parent.m_drag_y = y
                parent.DrawSash(x, y, "press")
                parent.m_container.CaptureMouse()


    def OnRelease(self, event):
        pass




