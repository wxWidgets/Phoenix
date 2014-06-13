# -*- coding: utf-8 -*-
#!/usr/bin/env python
#----------------------------------------------------------------------------
# Name:         _canvas.py
# Purpose:      The canvas class
#
# Author:       Pierre Hjälm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# Copyright:    (c) 2004 Pierre Hjälm - 1998 Julian Smart
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, py3-port
#----------------------------------------------------------------------------
"""
The OGL canvas class
"""
import wx
from .lines import LineShape
from .composit import *

NoDragging, StartDraggingLeft, ContinueDraggingLeft, StartDraggingRight, ContinueDraggingRight = 0, 1, 2, 3, 4

KEY_SHIFT, KEY_CTRL = 1, 2



# Helper function: True if 'contains' wholly contains 'contained'.
def WhollyContains(contains, contained):
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
    def __init__(self, parent = None, id = -1, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.BORDER, name = "ShapeCanvas"):
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
        
        self._Overlay = wx.Overlay()
        self._Buffer = wx.Bitmap(10, 10)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouseEvent)

    def Draw(self):
        """
        Update the buffer with the background and redraw the full diagram.
        """
        # update the buffer
        dc = wx.MemoryDC()
        dc.SelectObject(self._Buffer)

        dc.SetBackground(wx.Brush(self.GetBackgroundColour(), wx.BRUSHSTYLE_SOLID))
        dc.Clear() # make sure you clear the bitmap!

        if self.GetDiagram():
            self.GetDiagram().Redraw(dc)
    
    def OnSize(self, evt):
        """
        Initialize the buffer to the size of the window.
        """
        Size  = self.GetClientSize()

        # Make sure we don't try to create a 0 size bitmap
        Size = (max(Size[0], 1), max(Size[1], 1))
        self._Buffer = wx.Bitmap(Size[0], Size[1])
        self.Draw()
        
    def SetDiagram(self, diag):
        self._shapeDiagram = diag

    def GetDiagram(self):
        return self._shapeDiagram
    
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self._Buffer, 0, 0)

    def OnMouseEvent(self, evt):
        # we just get position, so is using ClientDC fine here?
        dc = wx.ClientDC(self)
        x, y = evt.GetLogicalPosition(dc)
        # del it so we don't get tempted to use it for something else
        del dc
        ## result seems to be the same using either here, but not sure which is correct
        #dc = wx.MemoryDC()
        #dc.SelectObject(self._Buffer)
        #x, y = evt.GetLogicalPosition(dc)

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
               ((info == None) or isinstance(object, info)) and \
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
                    (info == None or isinstance(object, info)) and 
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
        self.GetDiagram().AddShape(object, addAfter)

    def InsertShape(self, object):
        self.GetDiagram().InsertShape(object)

    def RemoveShape(self, object):
        self.GetDiagram().RemoveShape(object)

    def GetQuickEditMode(self):
        return self.GetDiagram().GetQuickEditMode()
    
    def Redraw(self, dc):
        self.GetDiagram().Redraw(dc)

    def Snap(self, x, y):
        return self.GetDiagram().Snap(x, y)

    def OnLeftClick(self, x, y, keys = 0):
        pass

    def OnRightClick(self, x, y, keys = 0):
        pass

    def OnDragLeft(self, draw, x, y, keys = 0):
        pass

    def OnBeginDragLeft(self, x, y, keys = 0):
        pass

    def OnEndDragLeft(self, x, y, keys = 0):
        pass

    def OnDragRight(self, draw, x, y, keys = 0):
        pass

    def OnBeginDragRight(self, x, y, keys = 0):
        pass

    def OnEndDragRight(self, x, y, keys = 0):
        pass
