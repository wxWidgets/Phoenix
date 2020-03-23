# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         _canvas.py
# Purpose:      The canvas class
#
# Author:       Pierre Hjälm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# Copyright:    (c) 2004 Pierre Hjälm - 1998 Julian Smart
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, py3-port, documented
#----------------------------------------------------------------------------
"""
The :class:`~lib.ogl.canvas.ShapeCanvas` class.
"""
import wx
from .lines import LineShape
from .composit import *
from .oglmisc import *

NoDragging, StartDraggingLeft, ContinueDraggingLeft, StartDraggingRight, ContinueDraggingRight = 0, 1, 2, 3, 4


def WhollyContains(contains, contained):
    """Helper function.

    :param `contains`: the containing shape
    :param `contained`: the contained shape
    :returns: `True` if 'contains' wholly contains 'contained'

    """
    xp1, yp1 = contains.GetX(), contains.GetY()
    xp2, yp2 = contained.GetX(), contained.GetY()

    w1, h1 = contains.GetBoundingBoxMax()
    w2, h2 = contained.GetBoundingBoxMax()

    left1 = xp1 - w1 / 2.0
    top1 = yp1 - h1 / 2.0
    right1 = xp1 + w1 / 2.0
    bottom1 = yp1 + h1 / 2.0

    left2 = xp2 - w2 / 2.0
    top2 = yp2 - h2 / 2.0
    right2 = xp2 + w2 / 2.0
    bottom2 = yp2 + h2 / 2.0

    return ((left1 <= left2) and (top1 <= top2) and (right1 >= right2) and (bottom1 >= bottom2))


class ShapeCanvas(wx.ScrolledWindow):
    """The :class:`ShapeCanvas` class."""
    def __init__(self, parent = None, id = -1, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.BORDER, name = "ShapeCanvas"):
        """Default class constructor.

        Default class constructor.

        :param `parent`: parent window
        :param integer `id`: window identifier. A value of -1 indicates a default value
        :param `pos`: the control position. A value of (-1, -1) indicates a default position,
         chosen by either the windowing system or wxPython, depending on platform
        :param `size`: the control size. A value of (-1, -1) indicates a default size,
         chosen by either the windowing system or wxPython, depending on platform
        :param integer `style`: the underlying :class:`wx.Window` style
        :param str `name`: the window name

        :type parent: :class:`wx.Window`
        :type pos: tuple or :class:`wx.Point`
        :type size: tuple or :class:`wx.Size`

        """
        wx.ScrolledWindow.__init__(self, parent, id, pos, size, style, name)

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

        self._shapeDiagram = None
        self._dragState = NoDragging
        self._draggedShape = None
        self._oldDragX = 0
        self._oldDragY = 0
        self._firstDragX = 0
        self._firstDragY = 0
        self._checkTolerance = True

        self._buffer = wx.Bitmap(1, 1)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)

    def Draw(self):
        """
        Update the buffer with the background and redraw the full diagram.
        """
        dc = wx.MemoryDC(self._buffer)

        dc.SetBackground(wx.Brush(self.GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        dc.Clear() # make sure you clear the bitmap!

        if self.GetDiagram():
            self.GetDiagram().Redraw(dc)

    def OnSize(self, evt):
        """
        The size handler, it initializes the buffer to the size of the window.
        """
        size  = self.GetVirtualSize()

        # Make sure we don't try to create a 0 size bitmap
        size = wx.Size(max(size.x, 1), max(size.y, 1))
        self._buffer = wx.Bitmap(size.x, size.y)
        self.Draw()

    def GetBuffer(self):
        return self._buffer

    def SetDiagram(self, diag):
        """Set the diagram associated with this canvas.

        :param `diag`: an instance of :class:`~lib.ogl.Diagram`

        """
        self._shapeDiagram = diag

    def GetDiagram(self):
        """Get the diagram associated with this canvas."""
        return self._shapeDiagram

    def OnPaint(self, evt):
        """
        The paint handler, uses :class:`BufferedPaintDC` to draw the
        buffer to the screen.
        """
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)
        dc.DrawBitmap(self._buffer, 0, 0)

    def OnMouseEvent(self, evt):
        """The mouse event handler."""
        x, y = self.CalcUnscrolledPosition(evt.GetPosition())
        keys = 0
        if evt.ShiftDown():
            keys |= KEY_SHIFT
        if evt.ControlDown():
            keys |= KEY_CTRL

        dragging = evt.Dragging()

        # Check if we're within the tolerance for mouse movements.
        # If we're very close to the position we started dragging
        # from, this may not be an intentional drag at all.
        if dragging:
            if self._checkTolerance:
                # the difference between two logical coordinates is a logical coordinate
                dx = abs(x - self._firstDragX)
                dy = abs(y - self._firstDragY)
                toler = self.GetDiagram().GetMouseTolerance()
                if (dx <= toler) and (dy <= toler):
                    return
            # If we've ignored the tolerance once, then ALWAYS ignore
            # tolerance in this drag, even if we come back within
            # the tolerance range.
            self._checkTolerance = False

        # Dragging - note that the effect of dragging is left entirely up
        # to the object, so no movement is done unless explicitly done by
        # object.
        if dragging and self._draggedShape and self._dragState == StartDraggingLeft:
            self._dragState = ContinueDraggingLeft

            # If the object isn't m_draggable, transfer message to canvas
            if self._draggedShape.Draggable():
                self._draggedShape.GetEventHandler().OnBeginDragLeft(x, y, keys, self._draggedAttachment)
            else:
                self._draggedShape = None
                self.OnBeginDragLeft(x, y, keys)

            self._oldDragX, self._oldDragY = x, y

        elif dragging and self._draggedShape and self._dragState == ContinueDraggingLeft:
            # Continue dragging
            self._draggedShape.GetEventHandler().OnDragLeft(False, self._oldDragX, self._oldDragY, keys, self._draggedAttachment)
            self._draggedShape.GetEventHandler().OnDragLeft(True, x, y, keys, self._draggedAttachment)
            self._oldDragX, self._oldDragY = x, y

        elif evt.LeftUp() and self._draggedShape and self._dragState == ContinueDraggingLeft:
            self._dragState = NoDragging
            self._checkTolerance = True

            self._draggedShape.GetEventHandler().OnDragLeft(False, self._oldDragX, self._oldDragY, keys, self._draggedAttachment)
            self._draggedShape.GetEventHandler().OnEndDragLeft(x, y, keys, self._draggedAttachment)
            self._draggedShape = None

        elif dragging and self._draggedShape and self._dragState == StartDraggingRight:
            self._dragState = ContinueDraggingRight
            if self._draggedShape.Draggable:
                self._draggedShape.GetEventHandler().OnBeginDragRight(x, y, keys, self._draggedAttachment)
            else:
                self._draggedShape = None
                self.OnBeginDragRight(x, y, keys)
            self._oldDragX, self._oldDragY = x, y

        elif dragging and self._draggedShape and self._dragState == ContinueDraggingRight:
            # Continue dragging
            self._draggedShape.GetEventHandler().OnDragRight(False, self._oldDragX, self._oldDragY, keys, self._draggedAttachment)
            self._draggedShape.GetEventHandler().OnDragRight(True, x, y, keys, self._draggedAttachment)
            self._oldDragX, self._oldDragY = x, y

        elif evt.RightUp() and self._draggedShape and self._dragState == ContinueDraggingRight:
            self._dragState = NoDragging
            self._checkTolerance = True

            self._draggedShape.GetEventHandler().OnDragRight(False, self._oldDragX, self._oldDragY, keys, self._draggedAttachment)
            self._draggedShape.GetEventHandler().OnEndDragRight(x, y, keys, self._draggedAttachment)
            self._draggedShape = None

        # All following events sent to canvas, not object
        elif dragging and not self._draggedShape and self._dragState == StartDraggingLeft:
            self._dragState = ContinueDraggingLeft
            self.OnBeginDragLeft(x, y, keys)
            self._oldDragX, self._oldDragY = x, y

        elif dragging and not self._draggedShape and self._dragState == ContinueDraggingLeft:
            # Continue dragging
            self.OnDragLeft(False, self._oldDragX, self._oldDragY, keys)
            self.OnDragLeft(True, x, y, keys)
            self._oldDragX, self._oldDragY = x, y

        elif evt.LeftUp() and not self._draggedShape and self._dragState == ContinueDraggingLeft:
            self._dragState = NoDragging
            self._checkTolerance = True

            self.OnDragLeft(False, self._oldDragX, self._oldDragY, keys)
            self.OnEndDragLeft(x, y, keys)
            self._draggedShape = None

        elif dragging and not self._draggedShape and self._dragState == StartDraggingRight:
            self._dragState = ContinueDraggingRight
            self.OnBeginDragRight(x, y, keys)
            self._oldDragX, self._oldDragY = x, y

        elif dragging and not self._draggedShape and self._dragState == ContinueDraggingRight:
            # Continue dragging
            self.OnDragRight(False, self._oldDragX, self._oldDragY, keys)
            self.OnDragRight(True, x, y, keys)
            self._oldDragX, self._oldDragY = x, y

        elif evt.RightUp() and not self._draggedShape and self._dragState == ContinueDraggingRight:
            self._dragState = NoDragging
            self._checkTolerance = True

            self.OnDragRight(False, self._oldDragX, self._oldDragY, keys)
            self.OnEndDragRight(x, y, keys)
            self._draggedShape = None

        # Non-dragging events
        elif evt.IsButton():
            self._checkTolerance = True

            # Find the nearest object
            attachment = 0

            nearest_object, attachment = self.FindShape(x, y)
            if nearest_object: # Object event
                if evt.LeftDown():
                    self._draggedShape = nearest_object
                    self._draggedAttachment = attachment
                    self._dragState = StartDraggingLeft
                    self._firstDragX = x
                    self._firstDragY = y

                elif evt.LeftUp():
                    # N.B. Only register a click if the same object was
                    # identified for down *and* up.
                    if nearest_object == self._draggedShape:
                        nearest_object.GetEventHandler().OnLeftClick(x, y, keys, attachment)
                    self._draggedShape = None
                    self._dragState = NoDragging

                elif evt.LeftDClick():
                    nearest_object.GetEventHandler().OnLeftDoubleClick(x, y, keys, attachment)
                    self._draggedShape = None
                    self._dragState = NoDragging

                elif evt.RightDown():
                    self._draggedShape = nearest_object
                    self._draggedAttachment = attachment
                    self._dragState = StartDraggingRight
                    self._firstDragX = x
                    self._firstDragY = y

                elif evt.RightUp():
                    if nearest_object == self._draggedShape:
                        nearest_object.GetEventHandler().OnRightClick(x, y, keys, attachment)
                    self._draggedShape = None
                    self._dragState = NoDragging

            else: # Canvas event
                if evt.LeftDown():
                    self._draggedShape = None
                    self._dragState = StartDraggingLeft
                    self._firstDragX = x
                    self._firstDragY = y

                elif evt.LeftUp():
                    self.OnLeftClick(x, y, keys)
                    self._draggedShape = None
                    self._dragState = NoDragging

                elif evt.RightDown():
                    self._draggedShape = None
                    self._dragState = StartDraggingRight
                    self._firstDragX = x
                    self._firstDragY = y

                elif evt.RightUp():
                    self.OnRightClick(x, y, keys)
                    self._draggedShape = None
                    self._dragState = NoDragging

        self.Draw()

    def FindShape(self, x, y, info = None, notObject = None):
        """
        Find shape at given position.

        :param `x`: the x position
        :param `y`: the y position
        :param `info`: ???
        :param `notObject`: ???

        """
        nearest = 100000.0
        nearest_attachment = 0
        nearest_object = None

        # Go backward through the object list, since we want:
        # (a) to have the control points drawn LAST to overlay
        #     the other objects
        # (b) to find the control points FIRST if they exist

        rl = self.GetDiagram().GetShapeList()[:]
        rl.reverse()
        for object in rl:
            # First pass for lines, which might be inside a container, so we
            # want lines to take priority over containers. This first loop
            # could fail if we clickout side a line, so then we'll
            # try other shapes.
            if object.IsShown() and \
               isinstance(object, LineShape) and \
               object.HitTest(x, y) and \
               ((info is None) or isinstance(object, info)) and \
               (not notObject or not notObject.HasDescendant(object)):
                temp_attachment, dist = object.HitTest(x, y)
                # A line is trickier to spot than a normal object.
                # For a line, since it's the diagonal of the box
                # we use for the hit test, we may have several
                # lines in the box and therefore we need to be able
                # to specify the nearest point to the centre of the line
                # as our hit criterion, to give the user some room for
                # manouevre.
                if dist < nearest:
                    nearest = dist
                    nearest_object = object
                    nearest_attachment = temp_attachment

        for object in rl:
            # On second pass, only ever consider non-composites or
            # divisions. If children want to pass up control to
            # the composite, that's up to them.
            if (object.IsShown() and
                   (isinstance(object, DivisionShape) or
                    not isinstance(object, CompositeShape)) and
                    object.HitTest(x, y) and
                    (info is None or isinstance(object, info)) and
                    (not notObject or not notObject.HasDescendant(object))):
                temp_attachment, dist = object.HitTest(x, y)
                if not isinstance(object, LineShape):
                    # If we've hit a container, and we have already
                    # found a line in the first pass, then ignore
                    # the container in case the line is in the container.
                    # Check for division in case line straddles divisions
                    # (i.e. is not wholly contained).
                    if not nearest_object or not (isinstance(object, DivisionShape) or WhollyContains(object, nearest_object)):
                        nearest_object = object
                        nearest_attachment = temp_attachment
                        break

        return nearest_object, nearest_attachment

    def AddShape(self, object, addAfter = None):
        """
        Add a shape to canvas.

        :param `object`: the :class:`~lib.ogl.Shape` instance to add
        :param `addAfter`: None or the :class:`~lib.ogl.Shape` after which
         above shape is to be added.

        """
        self.GetDiagram().AddShape(object, addAfter)

    def InsertShape(self, object):
        """
        Insert a shape to canvas.

        :param `object`: the :class:`~lib.ogl.Shape` instance to insert

        """
        self.GetDiagram().InsertShape(object)

    def RemoveShape(self, object):
        """
        Remove a shape from canvas.

        :param `object`: the :class:`~lib.ogl.Shape` instance to be removed

        """
        self.GetDiagram().RemoveShape(object)

    def GetQuickEditMode(self):
        """Get quick edit mode."""
        return self.GetDiagram().GetQuickEditMode()

    def Redraw(self, dc):
        """Redraw the diagram."""
        self.GetDiagram().Redraw(dc)

    def Snap(self, x, y):
        """Snap ???

        :param `x`: the x position
        :param `y`: the y position

        """
        return self.GetDiagram().Snap(x, y)

    def OnLeftClick(self, x, y, keys = 0):
        """not implemented???"""
        pass

    def OnRightClick(self, x, y, keys = 0):
        """not implemented???"""
        pass

    def OnDragLeft(self, draw, x, y, keys = 0):
        """not implemented???"""
        pass

    def OnBeginDragLeft(self, x, y, keys = 0):
        """not implemented???"""
        pass

    def OnEndDragLeft(self, x, y, keys = 0):
        """not implemented???"""
        pass

    def OnDragRight(self, draw, x, y, keys = 0):
        """not implemented???"""
        pass

    def OnBeginDragRight(self, x, y, keys = 0):
        """not implemented???"""
        pass

    def OnEndDragRight(self, x, y, keys = 0):
        """not implemented???"""
        pass
