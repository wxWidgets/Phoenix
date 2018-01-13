# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         composit.py
# Purpose:      Composite class
#
# Author:       Pierre Hjälm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# Copyright:    (c) 2004 Pierre Hjälm - 1998 Julian Smart
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, py3-port, documented
#----------------------------------------------------------------------------
"""
The :class:`~lib.ogl.composit.CompositeShape` class.
"""
import sys
import wx

from .basic import RectangleShape, Shape, ControlPoint
from .oglmisc import *

_objectStartX = 0.0
_objectStartY = 0.0

CONSTRAINT_CENTRED_VERTICALLY   = 1
CONSTRAINT_CENTRED_HORIZONTALLY = 2
CONSTRAINT_CENTRED_BOTH         = 3
CONSTRAINT_LEFT_OF              = 4
CONSTRAINT_RIGHT_OF             = 5
CONSTRAINT_ABOVE                = 6
CONSTRAINT_BELOW                = 7
CONSTRAINT_ALIGNED_TOP          = 8
CONSTRAINT_ALIGNED_BOTTOM       = 9
CONSTRAINT_ALIGNED_LEFT         = 10
CONSTRAINT_ALIGNED_RIGHT        = 11

# Like aligned, but with the objects centred on the respective edge
# of the reference object.
CONSTRAINT_MIDALIGNED_TOP       = 12
CONSTRAINT_MIDALIGNED_BOTTOM    = 13
CONSTRAINT_MIDALIGNED_LEFT      = 14
CONSTRAINT_MIDALIGNED_RIGHT     = 15


class ConstraintType(object):
    """The :class:`ConstraintType` class."""
    def __init__(self, theType, theName, thePhrase):
        """
        Default class constructor.

        :param `theType`: one of the folowing
         ====================================== ================================
         Constraint type                        Description
         ====================================== ================================
         `CONSTRAINT_CENTRED_VERTICALLY`        Centered vertically
         `CONSTRAINT_CENTRED_HORIZONTALLY`      Centered horizontally
         `CONSTRAINT_CENTRED_BOTH`              Centered in both directions
         `CONSTRAINT_LEFT_OF`                   Center left of
         `CONSTRAINT_RIGHT_OF`                  Center right of
         `CONSTRAINT_ABOVE`                     Center above
         `CONSTRAINT_BELOW`                     Center below
         `CONSTRAINT_ALIGNED_TOP`               Align top
         `CONSTRAINT_ALIGNED_BOTTOM`            Align bottom
         `CONSTRAINT_ALIGNED_LEFT`              Align left
         `CONSTRAINT_ALIGNED_RIGHT`             Align right
         `CONSTRAINT_MIDALIGNED_TOP`            Middle align top
         `CONSTRAINT_MIDALIGNED_BOTTOM`         Middle align bottom
         `CONSTRAINT_MIDALIGNED_LEFT`           Middle align left
         `CONSTRAINT_MIDALIGNED_RIGHT`          Middle align right
         ====================================== ================================

        :param `theName`: the name for the constraint
        :param `thePhrase`: the descriptive phrase

        """
        self._type = theType
        self._name = theName
        self._phrase = thePhrase



ConstraintTypes = [
    [CONSTRAINT_CENTRED_VERTICALLY,
        ConstraintType(CONSTRAINT_CENTRED_VERTICALLY, "Centre vertically", "centred vertically w.r.t.")],

    [CONSTRAINT_CENTRED_HORIZONTALLY,
        ConstraintType(CONSTRAINT_CENTRED_HORIZONTALLY, "Centre horizontally", "centred horizontally w.r.t.")],

    [CONSTRAINT_CENTRED_BOTH,
        ConstraintType(CONSTRAINT_CENTRED_BOTH, "Centre", "centred w.r.t.")],

    [CONSTRAINT_LEFT_OF,
        ConstraintType(CONSTRAINT_LEFT_OF, "Left of", "left of")],

    [CONSTRAINT_RIGHT_OF,
        ConstraintType(CONSTRAINT_RIGHT_OF, "Right of", "right of")],

    [CONSTRAINT_ABOVE,
        ConstraintType(CONSTRAINT_ABOVE, "Above", "above")],

    [CONSTRAINT_BELOW,
        ConstraintType(CONSTRAINT_BELOW, "Below", "below")],

    # Alignment
    [CONSTRAINT_ALIGNED_TOP,
        ConstraintType(CONSTRAINT_ALIGNED_TOP, "Top-aligned", "aligned to the top of")],

    [CONSTRAINT_ALIGNED_BOTTOM,
        ConstraintType(CONSTRAINT_ALIGNED_BOTTOM, "Bottom-aligned", "aligned to the bottom of")],

    [CONSTRAINT_ALIGNED_LEFT,
        ConstraintType(CONSTRAINT_ALIGNED_LEFT, "Left-aligned", "aligned to the left of")],

    [CONSTRAINT_ALIGNED_RIGHT,
        ConstraintType(CONSTRAINT_ALIGNED_RIGHT, "Right-aligned", "aligned to the right of")],

    # Mid-alignment
    [CONSTRAINT_MIDALIGNED_TOP,
        ConstraintType(CONSTRAINT_MIDALIGNED_TOP, "Top-midaligned", "centred on the top of")],

    [CONSTRAINT_MIDALIGNED_BOTTOM,
        ConstraintType(CONSTRAINT_MIDALIGNED_BOTTOM, "Bottom-midaligned", "centred on the bottom of")],

    [CONSTRAINT_MIDALIGNED_LEFT,
        ConstraintType(CONSTRAINT_MIDALIGNED_LEFT, "Left-midaligned", "centred on the left of")],

    [CONSTRAINT_MIDALIGNED_RIGHT,
        ConstraintType(CONSTRAINT_MIDALIGNED_RIGHT, "Right-midaligned", "centred on the right of")]
    ]


class Constraint(object):
    """
    The :class:`Constraint` class helps specify how child shapes are laid out
    with respect to siblings and parents.
    """
    def __init__(self, type, constraining, constrained):
        """
        Default class constructor.

        :param `type`: see :class:`ConstraintType` for valid types
        :param `constraining`: the constraining :class:`Shape`
        :param `constrained`: the constrained :class:`Shape`

        """
        self._xSpacing = 0.0
        self._ySpacing = 0.0

        self._constraintType = type
        self._constrainingObject = constraining

        self._constraintId = 0
        self._constraintName = "noname"

        self._constrainedObjects = constrained[:]

    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__module__, self.__class__.__name__)

    def SetSpacing(self, x, y):
        """
        Sets the horizontal and vertical spacing for the constraint.

        :param `x`: the x position
        :param `y`: the y position

        """
        self._xSpacing = x
        self._ySpacing = y

    def Equals(self, a, b):
        """
        Return `True` if a and b are approximately equal (for the purposes
        of evaluating the constraint).

        :param `a`: ???
        :param `b`: ???

        """
        marg = 0.5

        return b <= a + marg and b >= a - marg

    def Evaluate(self):
        """Evaluate this constraint and return `True` if anything changed."""
        maxWidth, maxHeight = self._constrainingObject.GetBoundingBoxMax()
        minWidth, minHeight = self._constrainingObject.GetBoundingBoxMin()
        x = self._constrainingObject.GetX()
        y = self._constrainingObject.GetY()

        dc = wx.MemoryDC()
        dc.SelectObject(self._constrainingObject.GetCanvas().GetBuffer())
        self._constrainingObject.GetCanvas().PrepareDC(dc)

        if self._constraintType == CONSTRAINT_CENTRED_VERTICALLY:
            n = len(self._constrainedObjects)
            totalObjectHeight = 0.0
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                totalObjectHeight += height2

            # Check if within the constraining object...
            if totalObjectHeight + (n + 1) * self._ySpacing <= minHeight:
                spacingY = (minHeight - totalObjectHeight) / (n + 1.0)
                startY = y - minHeight / 2.0
            else: # Otherwise, use default spacing
                spacingY = self._ySpacing
                startY = y - (totalObjectHeight + (n + 1) * spacingY) / 2.0

            # Now position the objects
            changed = False
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                startY += spacingY + height2 / 2.0
                if not self.Equals(startY, constrainedObject.GetY()):
                    constrainedObject.Move(dc, constrainedObject.GetX(), startY, False)
                    changed = True
                startY += height2 / 2.0
            return changed
        elif self._constraintType == CONSTRAINT_CENTRED_HORIZONTALLY:
            n = len(self._constrainedObjects)
            totalObjectWidth = 0.0
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                totalObjectWidth += width2

            # Check if within the constraining object...
            if totalObjectWidth + (n + 1) * self._xSpacing <= minWidth:
                spacingX = (minWidth - totalObjectWidth) / (n + 1.0)
                startX = x - minWidth / 2.0
            else: # Otherwise, use default spacing
                spacingX = self._xSpacing
                startX = x - (totalObjectWidth + (n + 1) * spacingX) / 2.0

            # Now position the objects
            changed = False
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                startX += spacingX + width2 / 2.0
                if not self.Equals(startX, constrainedObject.GetX()):
                    constrainedObject.Move(dc, startX, constrainedObject.GetY(), False)
                    changed = True
                startX += width2 / 2.0
            return changed
        elif self._constraintType == CONSTRAINT_CENTRED_BOTH:
            n = len(self._constrainedObjects)
            totalObjectWidth = 0.0
            totalObjectHeight = 0.0

            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                totalObjectWidth += width2
                totalObjectHeight += height2

            # Check if within the constraining object...
            if totalObjectHeight + (n + 1) * self._xSpacing <= minWidth:
                spacingX = (minWidth - totalObjectWidth) / (n + 1.0)
                startX = x - minWidth / 2.0
            else: # Otherwise, use default spacing
                spacingX = self._xSpacing
                startX = x - (totalObjectWidth + (n + 1) * spacingX) / 2.0

            # Check if within the constraining object...
            if totalObjectHeight + (n + 1) * self._ySpacing <= minHeight:
                spacingY = (minHeight - totalObjectHeight) / (n + 1.0)
                startY = y - minHeight / 2.0
            else: # Otherwise, use default spacing
                spacingY = self._ySpacing
                startY = y - (totalObjectHeight + (n + 1) * spacingY) / 2.0

            # Now position the objects
            changed = False
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                startX += spacingX + width2 / 2.0
                startY += spacingY + height2 / 2.0

                if not self.Equals(startX, constrainedObject.GetX()) or not self.Equals(startY, constrainedObject.GetY()):
                    constrainedObject.Move(dc, startX, startY, False)
                    changed = True

                startX += width2 / 2.0
                startY += height2 / 2.0
            return changed
        elif self._constraintType == CONSTRAINT_LEFT_OF:
            changed = False
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()

                x3 = x - minWidth / 2.0 - width2 / 2.0 - self._xSpacing
                if not self.Equals(x3, constrainedObject.GetX()):
                    changed = True
                    constrainedObject.Move(dc, x3, constrainedObject.GetY(), False)
            return changed
        elif self._constraintType == CONSTRAINT_RIGHT_OF:
            changed = False

            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                x3 = x + minWidth / 2.0 + width2 / 2.0 + self._xSpacing
                if not self.Equals(x3, constrainedObject.GetX()):
                    constrainedObject.Move(dc, x3, constrainedObject.GetY(), False)
                    changed = True
            return changed
        elif self._constraintType == CONSTRAINT_ABOVE:
            changed = False

            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()

                y3 = y - minHeight / 2.0 - height2 / 2.0 - self._ySpacing
                if not self.Equals(y3, constrainedObject.GetY()):
                    changed = True
                    constrainedObject.Move(dc, constrainedObject.GetX(), y3, False)
            return changed
        elif self._constraintType == CONSTRAINT_BELOW:
            changed = False

            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()

                y3 = y + minHeight / 2.0 + height2 / 2.0 + self._ySpacing
                if not self.Equals(y3, constrainedObject.GetY()):
                    changed = True
                    constrainedObject.Move(dc, constrainedObject.GetX(), y3, False)
            return changed
        elif self._constraintType == CONSTRAINT_ALIGNED_LEFT:
            changed = False
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                x3 = x - minWidth / 2.0 + width2 / 2.0 + self._xSpacing
                if not self.Equals(x3, constrainedObject.GetX()):
                    changed = True
                    constrainedObject.Move(dc, x3, constrainedObject.GetY(), False)
            return changed
        elif self._constraintType == CONSTRAINT_ALIGNED_RIGHT:
            changed = False
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                x3 = x + minWidth / 2.0 - width2 / 2.0 - self._xSpacing
                if not self.Equals(x3, constrainedObject.GetX()):
                    changed = True
                    constrainedObject.Move(dc, x3, constrainedObject.GetY(), False)
            return changed
        elif self._constraintType == CONSTRAINT_ALIGNED_TOP:
            changed = False
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                y3 = y -  minHeight / 2.0 + height2 / 2.0 + self._ySpacing
                if not self.Equals(y3, constrainedObject.GetY()):
                    changed = True
                    constrainedObject.Move(dc, constrainedObject.GetX(), y3, False)
            return changed
        elif self._constraintType == CONSTRAINT_ALIGNED_BOTTOM:
            changed = False
            for constrainedObject in self._constrainedObjects:
                width2, height2 = constrainedObject.GetBoundingBoxMax()
                y3 = y + minHeight / 2.0 - height2 / 2.0 - self._ySpacing
                if not self.Equals(y3, constrainedObject.GetY()):
                    changed = True
                    constrainedObject.Move(dc, constrainedObject.GetX(), y3, False)
            return changed
        elif self._constraintType == CONSTRAINT_MIDALIGNED_LEFT:
            changed = False
            for constrainedObject in self._constrainedObjects:
                x3 = x - minWidth / 2.0
                if not self.Equals(x3, constrainedObject.GetX()):
                    changed = True
                    constrainedObject.Move(dc, x3, constrainedObject.GetY(), False)
            return changed
        elif self._constraintType == CONSTRAINT_MIDALIGNED_RIGHT:
            changed = False
            for constrainedObject in self._constrainedObjects:
                x3 = x + minWidth / 2.0
                if not self.Equals(x3, constrainedObject.GetX()):
                    changed = True
                    constrainedObject.Move(dc, x3, constrainedObject.GetY(), False)
            return changed
        elif self._constraintType == CONSTRAINT_MIDALIGNED_TOP:
            changed = False
            for constrainedObject in self._constrainedObjects:
                y3 = y - minHeight / 2.0
                if not self.Equals(y3, constrainedObject.GetY()):
                    changed = True
                    constrainedObject.Move(dc, constrainedObject.GetX(), y3, False)
            return changed
        elif self._constraintType == CONSTRAINT_MIDALIGNED_BOTTOM:
            changed = False
            for constrainedObject in self._constrainedObjects:
                y3 = y + minHeight / 2.0
                if not self.Equals(y3, constrainedObject.GetY()):
                    changed = True
                    constrainedObject.Move(dc, constrainedObject.GetX(), y3, False)
            return changed

        return False

OGLConstraint = wx.deprecated(Constraint,
                     "The OGLConstraint name is deprecated, use `ogl.Constraint` instead.")


class CompositeShape(RectangleShape):
    """
    The :class:`CompositeShape` is a shape with a list of child objects, and a
    list of size and positioning constraints between the children.
    """
    def __init__(self):
        """
        Default class constructor.

        """
        RectangleShape.__init__(self, 100.0, 100.0)

        self._oldX = self._xpos
        self._oldY = self._ypos

        self._constraints = []
        self._divisions = [] # In case it's a container

    def OnDraw(self, dc):
        """The draw handler."""
        x1 = self._xpos - self._width / 2.0
        y1 = self._ypos - self._height / 2.0

        if self._shadowMode != SHADOW_NONE:
            if self._shadowBrush:
                dc.SetBrush(self._shadowBrush)
            dc.SetPen(wx.Pen(wx.WHITE, 1, wx.PENSTYLE_TRANSPARENT))

            if self._cornerRadius:
                dc.DrawRoundedRectangle(x1 + self._shadowOffsetX, y1 + self._shadowOffsetY, self._width, self._height, self._cornerRadius)
            else:
                dc.DrawRectangle(x1 + self._shadowOffsetX, y1 + self._shadowOffsetY, self._width, self._height)

        # For debug purposes /pi
        #dc.DrawRectangle(x1, y1, self._width, self._height)

    def OnDrawContents(self, dc):
        """The draw contents handler."""
        for object in self._children:
            object.Draw(dc)
            object.DrawLinks(dc)

        Shape.OnDrawContents(self, dc)

    def OnMovePre(self, dc, x, y, old_x, old_y, display = True):
        """The move 'pre' handler."""
        diffX = x - old_x
        diffY = y - old_y

        for object in self._children:
            object.Erase(dc)
            object.Move(dc, object.GetX() + diffX, object.GetY() + diffY, display)

        return True

    def OnErase(self, dc):
        """The erase handler."""
        RectangleShape.OnErase(self, dc)
        for object in self._children:
            object.Erase(dc)

    def OnDragLeft(self, draw, x, y, keys = 0, attachment = 0):
        """The drag left handler."""
        xx, yy = self._canvas.Snap(x, y)
        offsetX = xx - _objectStartX
        offsetY = yy - _objectStartY

        dc = wx.ClientDC(self.GetCanvas())
        self.GetCanvas().PrepareDC(dc)
        dc.SetLogicalFunction(OGLRBLF)

        dottedPen = wx.Pen(wx.Colour(0, 0, 0), 1, wx.PENSTYLE_DOT)
        dc.SetPen(dottedPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        self.GetEventHandler().OnDrawOutline(dc, self.GetX() + offsetX, self.GetY() + offsetY, self.GetWidth(), self.GetHeight())

    def OnBeginDragLeft(self, x, y, keys = 0, attachment = 0):
        """The begin drag left handler."""
        global _objectStartX, _objectStartY

        _objectStartX = x
        _objectStartY = y

        dc = wx.ClientDC(self.GetCanvas())
        self.GetCanvas().PrepareDC(dc)
        dc.SetLogicalFunction(OGLRBLF)

        dottedPen = wx.Pen(wx.Colour(0, 0, 0), 1, wx.PENSTYLE_DOT)
        dc.SetPen(dottedPen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        self._canvas.CaptureMouse()

        xx, yy = self._canvas.Snap(x, y)
        offsetX = xx - _objectStartX
        offsetY = yy - _objectStartY

        self.GetEventHandler().OnDrawOutline(dc, self.GetX() + offsetX, self.GetY() + offsetY, self.GetWidth(), self.GetHeight())

    def OnEndDragLeft(self, x, y, keys = 0, attachment = 0):
        """The end drag left handler."""
        if self._canvas.HasCapture():
            self._canvas.ReleaseMouse()

        if not self._draggable:
            if self._parent:
                self._parent.GetEventHandler().OnEndDragLeft(x, y, keys, 0)
            return

        dc = wx.ClientDC(self.GetCanvas())
        self.GetCanvas().PrepareDC(dc)
        dc.SetLogicalFunction(wx.COPY)

        self.Erase(dc)

        xx, yy = self._canvas.Snap(x, y)
        offsetX = xx - _objectStartX
        offsetY = yy - _objectStartY

        self.Move(dc, self.GetX() + offsetX, self.GetY() + offsetY)

        if self._canvas and not self._canvas.GetQuickEditMode():
            self._canvas.Redraw(dc)

    def OnRightClick(self, x, y, keys = 0, attachment = 0):
        """The right click handler.

        :note: If we get a ctrl-right click, this means send the message to
         the division, so we can invoke a user interface for dealing
         with regions.
        """
        if keys & KEY_CTRL:
            for division in self._divisions:
                hit = division.HitTest(x, y)
                if hit:
                    division.GetEventHandler().OnRightClick(x, y, keys, hit[0])
                    break

    def SetSize(self, w, h, recursive = True):
        """
        Set the size.

        :param `w`: the width
        :param `h`: the heigth
        :param `recursive`: size the children recursively

        """
        self.SetAttachmentSize(w, h)

        xScale = float(w) / max(1, self.GetWidth())
        yScale = float(h) / max(1, self.GetHeight())

        self._width = w
        self._height = h

        if not recursive:
            return

        dc = wx.MemoryDC()
        dc.SelectObject(self.GetCanvas().GetBuffer())
        self.GetCanvas().PrepareDC(dc)

        for object in self._children:
            # Scale the position first
            newX = (object.GetX() - self.GetX()) * xScale + self.GetX()
            newY = (object.GetY() - self.GetY()) * yScale + self.GetY()
            object.Show(False)
            object.Move(dc, newX, newY)
            object.Show(True)

            # Now set the scaled size
            xbound, ybound = object.GetBoundingBoxMax()
            if not object.GetFixedWidth():
                xbound *= xScale
            if not object.GetFixedHeight():
                ybound *= yScale
            object.SetSize(xbound, ybound)

        self.SetDefaultRegionSize()

    def AddChild(self, child, addAfter = None):
        """
        Add a shape to the composite. If addAfter is not None, the shape
        will be added after addAfter.

        :param `child`: an instance of :class:`~lib.ogl.Shape`
        :param `addAfter`: an instance of :class:`~lib.ogl.Shape`

        """
        self._children.append(child)
        child.SetParent(self)
        if self._canvas:
            # Ensure we add at the right position
            if addAfter:
                child.RemoveFromCanvas(self._canvas)
            child.AddToCanvas(self._canvas, addAfter)

    def RemoveChild(self, child):
        """
        Removes the child from the composite and any constraint
        relationships, but does not delete the child.

        :param `child`: an instance of :class:`~lib.ogl.Shape`

        """
        if child in self._children:
            self._children.remove(child)
        if child in self._divisions:
            self._divisions.remove(child)
        self.RemoveChildFromConstraints(child)
        child.SetParent(None)

    def Delete(self):
        """
        Fully disconnect this shape from parents, children, the
        canvas, etc.
        """
        for child in self.GetChildren():
            self.RemoveChild(child)
            child.Delete()
        RectangleShape.Delete(self)
        self._constraints = []
        self._divisions = []

    def DeleteConstraintsInvolvingChild(self, child):
        """
        This function deletes constraints which mention the given child.

        Used when deleting a child from the composite.

        :param `child`: an instance of :class:`~lib.ogl.Shape`

        """
        for constraint in self._constraints:
            if constraint._constrainingObject == child or child in constraint._constrainedObjects:
                self._constraints.remove(constraint)

    def RemoveChildFromConstraints(self, child):
        """
        Removes the child from the constraints.

        :param `child`: an instance of :class:`~lib.ogl.Shape`

        """

        for constraint in self._constraints:
            if child in constraint._constrainedObjects:
                constraint._constrainedObjects.remove(child)
            if constraint._constrainingObject == child:
                constraint._constrainingObject = None

            # Delete the constraint if no participants left
            if not constraint._constrainingObject:
                self._constraints.remove(constraint)

    def AddConstraint(self, constraint):
        """
        Adds a constraint to the composite.

        :param `constraint`: an instance of :class:`~lib.ogl.Shape`

        """
        self._constraints.append(constraint)
        if constraint._constraintId == 0:
            constraint._constraintId = wx.NewId()
        return constraint

    def AddSimpleConstraint(self, type, constraining, constrained):
        """
        Add a constraint of the given type to the composite.

        :param `type`: see :class:`ConstraintType` for valid types
        :param `constraining`: the constraining :class:`Shape`
        :param `constrained`: the constrained :class:`Shape`

        """
        constraint = Constraint(type, constraining, constrained)
        if constraint._constraintId == 0:
            constraint._constraintId = wx.NewId()
        self._constraints.append(constraint)
        return constraint

    def FindConstraint(self, cId):
        """
        Finds the constraint with the given id.

        :param `cId`: The constraint id to find.

        :returns: None or a tuple of the constraint and the actual composite the
         constraint was in, in case that composite was a descendant of
         this composit.

        """
        for constraint in self._constraints:
            if constraint._constraintId == cId:
                return constraint, self

        # If not found, try children
        for child in self._children:
            if isinstance(child, CompositeShape):
                constraint = child.FindConstraint(cId)
                if constraint:
                    return constraint[0], child

        return None

    def DeleteConstraint(self, constraint):
        """
        Deletes constraint from composite.

        :param `constraint`: the constraint to delete

        """
        self._constraints.remove(constraint)

    def CalculateSize(self):
        """
        Calculates the size and position of the composite based on
        child sizes and positions.

        """
        maxX = -999999.9
        maxY = -999999.9
        minX = 999999.9
        minY = 999999.9

        for child in self._children:
            # Recalculate size of composite objects because may not conform
            # to size it was set to - depends on the children.
            if isinstance(child, CompositeShape):
                child.CalculateSize()

            w, h = child.GetBoundingBoxMax()
            if child.GetX() + w / 2.0 > maxX:
                maxX = child.GetX() + w / 2.0
            if child.GetX() - w / 2.0 < minX:
                minX = child.GetX() - w / 2.0
            if child.GetY() + h / 2.0 > maxY:
                maxY = child.GetY() + h / 2.0
            if child.GetY() - h / 2.0 < minY:
                minY = child.GetY() - h / 2.0

        self._width = maxX - minX
        self._height = maxY - minY
        self._xpos = self._width / 2.0 + minX
        self._ypos = self._height / 2.0 + minY

    def Recompute(self):
        """
        Recomputes any constraints associated with the object. If `False` is
        returned, the constraints could not be satisfied (there was an
        inconsistency).

        """
        noIterations = 0
        changed = True
        while changed and noIterations < 500:
            changed = self.Constrain()
            noIterations += 1

        return not changed

    def Constrain(self):
        """
        Constrain the children.

        :returns: True if constained otherwise False

        """
        self.CalculateSize()

        changed = False
        for child in self._children:
            if isinstance(child, CompositeShape) and child.Constrain():
                changed = True

        for constraint in self._constraints:
            if constraint.Evaluate():
                changed = True

        return changed

    def MakeContainer(self):
        """
        Makes this composite into a container by creating one child
        DivisionShape.
        """
        division = self.OnCreateDivision()
        self._divisions.append(division)
        self.AddChild(division)

        division.SetSize(self._width, self._height)

        dc = wx.MemoryDC()
        dc.SelectObject(self.GetCanvas().GetBuffer())
        self.GetCanvas().PrepareDC(dc)

        division.Move(dc, self.GetX(), self.GetY())
        self.Recompute()
        division.Show(True)

    def OnCreateDivision(self):
        """Create division handler."""
        return DivisionShape()

    def FindContainerImage(self):
        """
        Finds the image used to visualize a container. This is any child of
        the composite that is not in the divisions list.

        """
        for child in self._children:
            if child in self._divisions:
                return child

        return None

    def ContainsDivision(self, division):
        """
        Check if division is descendant.

        :param `division`: divison to check
        :returns: `True` if division is a descendant of this container.

        """
        if division in self._divisions:
            return True

        for child in self._children:
            if isinstance(child, CompositeShape):
                return child.ContainsDivision(division)

        return False

    def GetDivisions(self):
        """Return the list of divisions."""
        return self._divisions

    def GetConstraints(self):
        """Return the list of constraints."""
        return self._constraints


DIVISION_SIDE_NONE      =0
DIVISION_SIDE_LEFT      =1
DIVISION_SIDE_TOP       =2
DIVISION_SIDE_RIGHT     =3
DIVISION_SIDE_BOTTOM    =4

originalX = 0.0
originalY = 0.0
originalW = 0.0
originalH = 0.0



class DivisionControlPoint(ControlPoint):
    def __init__(self, the_canvas, object, size, the_xoffset, the_yoffset, the_type):
        ControlPoint.__init__(self, the_canvas, object, size, the_xoffset, the_yoffset, the_type)
        self.SetEraseObject(False)

    # Implement resizing of canvas object
    def OnDragLeft(self, draw, x, y, keys = 0, attachment = 0):
        ControlPoint.OnDragLeft(self, draw, x, y, keys, attachment)

    def OnBeginDragLeft(self, x, y, keys = 0, attachment = 0):
        global originalX, originalY, originalW, originalH

        originalX = self._shape.GetX()
        originalY = self._shape.GetY()
        originalW = self._shape.GetWidth()
        originalH = self._shape.GetHeight()

        ControlPoint.OnBeginDragLeft(self, x, y, keys, attachment)

    def OnEndDragLeft(self, x, y, keys = 0, attachment = 0):
        ControlPoint.OnEndDragLeft(self, x, y, keys, attachment)

        dc = wx.MemoryDC()
        dc.SelectObject(self.GetCanvas().GetBuffer())
        self.GetCanvas().PrepareDC(dc)

        division = self._shape
        divisionParent = division.GetParent()

        # Need to check it's within the bounds of the parent composite
        x1 = divisionParent.GetX() - divisionParent.GetWidth() / 2.0
        y1 = divisionParent.GetY() - divisionParent.GetHeight() / 2.0
        x2 = divisionParent.GetX() + divisionParent.GetWidth() / 2.0
        y2 = divisionParent.GetY() + divisionParent.GetHeight() / 2.0

        # Need to check it has not made the division zero or negative
        # width / height
        dx1 = division.GetX() - division.GetWidth() / 2.0
        dy1 = division.GetY() - division.GetHeight() / 2.0
        dx2 = division.GetX() + division.GetWidth() / 2.0
        dy2 = division.GetY() + division.GetHeight() / 2.0

        success = True
        if division.GetHandleSide() == DIVISION_SIDE_LEFT:
            if x <= x1 or x >= x2 or x >= dx2:
                success = False
            # Try it out first...
            elif not division.ResizeAdjoining(DIVISION_SIDE_LEFT, x, True):
                success = False
            else:
                division.ResizeAdjoining(DIVISION_SIDE_LEFT, x, False)
        elif division.GetHandleSide() == DIVISION_SIDE_TOP:
            if y <= y1 or y >= y2 or y >= dy2:
                success = False
            elif not division.ResizeAdjoining(DIVISION_SIDE_TOP, y, True):
                success = False
            else:
                division.ResizingAdjoining(DIVISION_SIDE_TOP, y, False)
        elif division.GetHandleSide() == DIVISION_SIDE_RIGHT:
            if x <= x1 or x >= x2 or x <= dx1:
                success = False
            elif not division.ResizeAdjoining(DIVISION_SIDE_RIGHT, x, True):
                success = False
            else:
                division.ResizeAdjoining(DIVISION_SIDE_RIGHT, x, False)
        elif division.GetHandleSide() == DIVISION_SIDE_BOTTOM:
            if y <= y1 or y >= y2 or y <= dy1:
                success = False
            elif not division.ResizeAdjoining(DIVISION_SIDE_BOTTOM, y, True):
                success = False
            else:
                division.ResizeAdjoining(DIVISION_SIDE_BOTTOM, y, False)

        if not success:
            division.SetSize(originalW, originalH)
            division.Move(dc, originalX, originalY)

        divisionParent.Draw(dc)
        division.GetEventHandler().OnDrawControlPoints(dc)



DIVISION_MENU_SPLIT_HORIZONTALLY    =1
DIVISION_MENU_SPLIT_VERTICALLY      =2
DIVISION_MENU_EDIT_LEFT_EDGE        =3
DIVISION_MENU_EDIT_TOP_EDGE         =4
DIVISION_MENU_EDIT_RIGHT_EDGE       =5
DIVISION_MENU_EDIT_BOTTOM_EDGE      =6
DIVISION_MENU_DELETE_ALL            =7



class PopupDivisionMenu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)
        self.Append(DIVISION_MENU_SPLIT_HORIZONTALLY,"Split horizontally")
        self.Append(DIVISION_MENU_SPLIT_VERTICALLY,"Split vertically")
        self.AppendSeparator()
        self.Append(DIVISION_MENU_EDIT_LEFT_EDGE,"Edit left edge")
        self.Append(DIVISION_MENU_EDIT_TOP_EDGE,"Edit top edge")

        wx.EVT_MENU_RANGE(self, DIVISION_MENU_SPLIT_HORIZONTALLY, DIVISION_MENU_EDIT_BOTTOM_EDGE, self.OnMenu)

    def SetClientData(self, data):
        self._clientData = data

    def GetClientData(self):
        return self._clientData

    def OnMenu(self, event):
        division = self.GetClientData()
        if event.GetId() == DIVISION_MENU_SPLIT_HORIZONTALLY:
            division.Divide(wx.HORIZONTAL)
        elif event.GetId() == DIVISION_MENU_SPLIT_VERTICALLY:
            division.Divide(wx.VERTICAL)
        elif event.GetId() == DIVISION_MENU_EDIT_LEFT_EDGE:
            division.EditEdge(DIVISION_SIDE_LEFT)
        elif event.GetId() == DIVISION_MENU_EDIT_TOP_EDGE:
            division.EditEdge(DIVISION_SIDE_TOP)



class DivisionShape(CompositeShape):
    """
    A :class:`DivisionShape` class is a composite with special properties,
    to be used for containment. It's a subdivision of a container.
    A containing node image consists of a composite with a main child shape
    such as rounded rectangle, plus a list of division objects.
    It needs to be a composite because a division contains pieces
    of diagram.

    :note: A container has at least one wxDivisionShape for consistency.
     This can be subdivided, so it turns into two objects, then each of
     these can be subdivided, etc.

    """
    def __init__(self):
        """
        Default class constructor.
        """
        CompositeShape.__init__(self)
        self.SetSensitivityFilter(OP_CLICK_LEFT | OP_CLICK_RIGHT | OP_DRAG_RIGHT)
        self.SetCentreResize(False)
        self.SetAttachmentMode(True)
        self._leftSide = None
        self._rightSide = None
        self._topSide = None
        self._bottomSide = None
        self._handleSide = DIVISION_SIDE_NONE
        self._leftSidePen = wx.BLACK_PEN
        self._topSidePen = wx.BLACK_PEN
        self._leftSideColour = "BLACK"
        self._topSideColour = "BLACK"
        self._leftSideStyle = "Solid"
        self._topSideStyle = "Solid"
        self.ClearRegions()

    def SetLeftSide(self, shape):
        """Set the the division on the left side of this division."""
        self._leftSide = shape

    def SetTopSide(self, shape):
        """Set the the division on the top side of this division."""
        self._topSide = shape

    def SetRightSide(self, shape):
        """Set the the division on the right side of this division."""
        self._rightSide = shape

    def SetBottomSide(self, shape):
        """Set the the division on the bottom side of this division."""
        self._bottomSide = shape

    def GetLeftSide(self):
        """Return the division on the left side of this division."""
        return self._leftSide

    def GetTopSide(self):
        """Return the division on the top side of this division."""
        return self._topSide

    def GetRightSide(self):
        """Return the division on the right side of this division."""
        return self._rightSide

    def GetBottomSide(self):
        """Return the division on the bottom side of this division."""
        return self._bottomSide

    def SetHandleSide(self, side):
        """
        Sets the side which the handle appears on.

        :param `side`: Either DIVISION_SIDE_LEFT or DIVISION_SIDE_TOP.

        """
        self._handleSide = side

    def GetHandleSide(self):
        """Return the side which the handle appears on."""
        return self._handleSide

    def SetLeftSidePen(self, pen):
        """Set the colour for drawing the left side of the division."""
        self._leftSidePen = pen

    def SetTopSidePen(self, pen):
        """Set the colour for drawing the top side of the division."""
        self._topSidePen = pen

    def GetLeftSidePen(self):
        """Return the pen used for drawing the left side of the division."""
        return self._leftSidePen

    def GetTopSidePen(self):
        """Return the pen used for drawing the top side of the division."""
        return self._topSidePen

    def GetLeftSideColour(self):
        """Return the colour used for drawing the left side of the division."""
        return self._leftSideColour

    def GetTopSideColour(self):
        """Return the colour used for drawing the top side of the division."""
        return self._topSideColour

    def SetLeftSideColour(self, colour):
        """Set the colour for drawing the left side of the division."""
        self._leftSideColour = colour

    def SetTopSideColour(self, colour):
        """Set the colour for drawing the top side of the division."""
        self._topSideColour = colour

    def GetLeftSideStyle(self):
        """Return the style used for the left side of the division."""
        return self._leftSideStyle

    def GetTopSideStyle(self):
        """Return the style used for the top side of the division."""
        return self._topSideStyle

    def SetLeftSideStyle(self, style):
        """
        Set the left side style.

        :param `style`: valid values ???

        """
        self._leftSideStyle = style

    def SetTopSideStyle(self, style):
        """
        Set the top side style.

        :param `style`: valid values ???

        """
        self._lefttopStyle = style

    def OnDraw(self, dc):
        """The draw handler."""
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetBackgroundMode(wx.TRANSPARENT)

        x1 = self.GetX() - self.GetWidth() / 2.0
        y1 = self.GetY() - self.GetHeight() / 2.0
        x2 = self.GetX() + self.GetWidth() / 2.0
        y2 = self.GetY() + self.GetHeight() / 2.0

        # Should subtract 1 pixel if drawing under Windows
        if sys.platform[:3] == "win":
            y2 -= 1

        if self._leftSide:
            dc.SetPen(self._leftSidePen)
            dc.DrawLine(x1, y2, x1, y1)

        if self._topSide:
            dc.SetPen(self._topSidePen)
            dc.DrawLine(x1, y1, x2, y1)

        # For testing purposes, draw a rectangle so we know
        # how big the division is.
        #dc.SetBrush(wx.RED_BRUSH)
        #dc.DrawRectangle(x1, y1, self.GetWidth(), self.GetHeight())

    def OnDrawContents(self, dc):
        """The draw contens handler."""
        CompositeShape.OnDrawContents(self, dc)

    def OnMovePre(self, dc, x, y, oldx, oldy, display = True):
        """The move 'pre' handler."""
        diffX = x - oldx
        diffY = y - oldy
        for object in self._children:
            object.Erase(dc)
            object.Move(dc, object.GetX() + diffX, object.GetY() + diffY, display)
        return True

    def OnDragLeft(self, draw, x, y, keys = 0, attachment = 0):
        """The drag left handler."""
        if self._sensitivity & OP_DRAG_LEFT != OP_DRAG_LEFT:
            if self._parent:
                hit = self._parent.HitTest(x, y)
                if hit:
                    attachment, dist = hit
                self._parent.GetEventHandler().OnDragLeft(draw, x, y, keys, attachment)
            return
        Shape.OnDragLeft(self, draw, x, y, keys, attachment)

    def OnBeginDragLeft(self, x, y, keys = 0, attachment = 0):
        """The begin drag left handler."""
        if self._sensitivity & OP_DRAG_LEFT != OP_DRAG_LEFT:
            if self._parent:
                hit = self._parent.HitTest(x, y)
                if hit:
                    attachment, dist = hit
                self._parent.GetEventHandler().OnBeginDragLeft(x, y, keys, attachment)
            return
        Shape.OnBeginDragLeft(x, y, keys, attachment)

    def OnEndDragLeft(self, x, y, keys = 0, attachment = 0):
        """The end drag left handler."""
        if self._canvas.HasCapture():
            self._canvas.ReleaseMouse()
        if self._sensitivity & OP_DRAG_LEFT != OP_DRAG_LEFT:
            if self._parent:
                hit = self._parent.HitTest(x, y)
                if hit:
                    attachment, dist = hit
                self._parent.GetEventHandler().OnEndDragLeft(x, y, keys, attachment)
            return

        dc = wx.MemoryDC()
        dc.SelectObject(self.GetCanvas().GetBuffer())
        self.GetCanvas().PrepareDC(dc)
        dc.SetLogicalFunction(wx.COPY)

        self._xpos, self._ypos = self._canvas.Snap(self._xpos, self._ypos)
        self.GetEventHandler().OnMovePre(dc, x, y, self._oldX, self._oldY)

        self.ResetControlPoints()
        self.Draw(dc)
        self.MoveLinks(dc)
        self.GetEventHandler().OnDrawControlPoints(dc)

        if self._canvas and not self._canvas.GetQuickEditMode():
            self._canvas.Redraw(dc)

    def SetSize(self, w, h, recursive = True):
        """
        Set the size.

        :param `w`: the width
        :param `h`: the heigth
        :param `recursive`: `True` recurse all children

        """
        self._width = w
        self._height = h
        RectangleShape.SetSize(self, w, h, recursive)

    def CalculateSize(self):
        """not implemented???"""
        pass

    # Experimental
    def OnRightClick(self, x, y, keys = 0, attachment = 0):
        """The right click handler."""
        if keys & KEY_CTRL:
            self.PopupMenu(x, y)
        else:
            if self._parent:
                hit = self._parent.HitTest(x, y)
                if hit:
                    attachment, dist = hit
                self._parent.GetEventHandler().OnRightClick(x, y, keys, attachment)

    def Divide(self, direction):
        """Divide this division into two further divisions.

        :param `direction`: `wx.HORIZONTAL` for horizontal or `wx.VERTICAL` for
         vertical division.

        """
        # Calculate existing top-left, bottom-right
        x1 = self.GetX() - self.GetWidth() / 2.0
        y1 = self.GetY() - self.GetHeight() / 2.0

        compositeParent = self.GetParent()
        oldWidth = self.GetWidth()
        oldHeight = self.GetHeight()
        if self.Selected():
            self.Select(False)

        dc = wx.MemoryDC()
        dc.SelectObject(self.GetCanvas().GetBuffer())
        self.GetCanvas().PrepareDC(dc)

        if direction == wx.VERTICAL:
            # Dividing vertically means notionally putting a horizontal
            # line through it.
            # Break existing piece into two.
            newXPos1 = self.GetX()
            newYPos1 = y1 + self.GetHeight() / 4.0
            newXPos2 = self.GetX()
            newYPos2 = y1 + 3 * self.GetHeight() / 4.0
            newDivision = compositeParent.OnCreateDivision()
            newDivision.Show(True)

            self.Erase(dc)

            # Anything adjoining the bottom of this division now adjoins the
            # bottom of the new division.
            for obj in compositeParent.GetDivisions():
                if obj.GetTopSide() == self:
                    obj.SetTopSide(newDivision)

            newDivision.SetTopSide(self)
            newDivision.SetBottomSide(self._bottomSide)
            newDivision.SetLeftSide(self._leftSide)
            newDivision.SetRightSide(self._rightSide)
            self._bottomSide = newDivision

            compositeParent.GetDivisions().append(newDivision)

            # CHANGE: Need to insert this division at start of divisions in the
            # object list, because e.g.:
            # 1) Add division
            # 2) Add contained object
            # 3) Add division
            # Division is now receiving mouse events _before_ the contained
            # object, because it was added last (on top of all others)

            # Add after the image that visualizes the container
            compositeParent.AddChild(newDivision, compositeParent.FindContainerImage())

            self._handleSide = DIVISION_SIDE_BOTTOM
            newDivision.SetHandleSide(DIVISION_SIDE_TOP)

            self.SetSize(oldWidth, oldHeight / 2.0)
            self.Move(dc, newXPos1, newYPos1)

            newDivision.SetSize(oldWidth, oldHeight / 2.0)
            newDivision.Move(dc, newXPos2, newYPos2)
        else:
            # Dividing horizontally means notionally putting a vertical line
            # through it.
            # Break existing piece into two.
            newXPos1 = x1 + self.GetWidth() / 4.0
            newYPos1 = self.GetY()
            newXPos2 = x1 + 3 * self.GetWidth() / 4.0
            newYPos2 = self.GetY()
            newDivision = compositeParent.OnCreateDivision()
            newDivision.Show(True)

            self.Erase(dc)

            # Anything adjoining the left of this division now adjoins the
            # left of the new division.
            for obj in compositeParent.GetDivisions():
                if obj.GetLeftSide() == self:
                    obj.SetLeftSide(newDivision)

            newDivision.SetTopSide(self._topSide)
            newDivision.SetBottomSide(self._bottomSide)
            newDivision.SetLeftSide(self)
            newDivision.SetRightSide(self._rightSide)
            self._rightSide = newDivision

            compositeParent.GetDivisions().append(newDivision)
            compositeParent.AddChild(newDivision, compositeParent.FindContainerImage())

            self._handleSide = DIVISION_SIDE_RIGHT
            newDivision.SetHandleSide(DIVISION_SIDE_LEFT)

            self.SetSize(oldWidth / 2.0, oldHeight)
            self.Move(dc, newXPos1, newYPos1)

            newDivision.SetSize(oldWidth / 2.0, oldHeight)
            newDivision.Move(dc, newXPos2, newYPos2)

        if compositeParent.Selected():
            compositeParent.DeleteControlPoints(dc)
            compositeParent.MakeControlPoints()
            compositeParent.MakeMandatoryControlPoints()

        compositeParent.Draw(dc)
        return True

    def MakeControlPoints(self):
        """Make control points."""
        self.MakeMandatoryControlPoints()

    def MakeMandatoryControlPoints(self):
        """Make mandatory control points."""
        maxX, maxY = self.GetBoundingBoxMax()
        x = y = 0.0
        direction = 0

        if self._handleSide == DIVISION_SIDE_LEFT:
            x = -maxX / 2.0
            direction = CONTROL_POINT_HORIZONTAL
        elif self._handleSide == DIVISION_SIDE_TOP:
            y = -maxY / 2.0
            direction = CONTROL_POINT_VERTICAL
        elif self._handleSide == DIVISION_SIDE_RIGHT:
            x = maxX / 2.0
            direction = CONTROL_POINT_HORIZONTAL
        elif self._handleSide == DIVISION_SIDE_BOTTOM:
            y = maxY / 2.0
            direction = CONTROL_POINT_VERTICAL

        if self._handleSide != DIVISION_SIDE_NONE:
            control = DivisionControlPoint(self._canvas, self, CONTROL_POINT_SIZE, x, y, direction)
            self._canvas.AddShape(control)
            self._controlPoints.append(control)

    def ResetControlPoints(self):
        """Reset control points."""
        self.ResetMandatoryControlPoints()

    def ResetMandatoryControlPoints(self):
        """Reset mandatory control points."""
        if not self._controlPoints:
            return

        maxX, maxY = self.GetBoundingBoxMax()

        node = self._controlPoints[0]

        if self._handleSide == DIVISION_SIDE_LEFT and node:
            node._xoffset = -maxX / 2.0
            node._yoffset = 0.0

        if self._handleSide == DIVISION_SIDE_TOP and node:
            node._xoffset = 0.0
            node._yoffset = -maxY / 2.0

        if self._handleSide == DIVISION_SIDE_RIGHT and node:
            node._xoffset = maxX / 2.0
            node._yoffset = 0.0

        if self._handleSide == DIVISION_SIDE_BOTTOM and node:
            node._xoffset = 0.0
            node._yoffset = maxY / 2.0

    def AdjustLeft(self, left, test):
        """
        Adjust a side.

        :param `left`: desired left position ???
        :param `test`: if `True` just a test
        :returns: `False` if it's not physically possible to adjust it to
         this point.
        """
        x2 = self.GetX() + self.GetWidth() / 2.0

        if left >= x2:
            return False

        if test:
            return True

        newW = x2 - left
        newX = left + newW / 2.0
        self.SetSize(newW, self.GetHeight())

        dc = wx.MemoryDC()
        dc.SelectObject(self.GetCanvas().GetBuffer())
        self.GetCanvas().PrepareDC(dc)

        self.Move(dc, newX, self.GetY())
        return True

    def AdjustRight(self, right, test):
        """
        Adjust a side.

        :param `right`: desired right position ???
        :param `test`: if `True` just a test
        :returns: `False` if it's not physically possible to adjust it to
         this point.

        """
        x1 = self.GetX() - self.GetWidth() / 2.0

        if right <= x1:
            return False

        if test:
            return True

        newW = right - x1
        newX = x1 + newW / 2.0
        self.SetSize(newW, self.GetHeight())

        dc = wx.MemoryDC()
        dc.SelectObject(self.GetCanvas().GetBuffer())
        self.GetCanvas().PrepareDC(dc)

        self.Move(dc, newX, self.GetY())
        return True

    def AdjustTop(self, top, test):
        """
        Adjust a side.

        :param `top`: desired top position ???
        :param `test`: if `True` just a test
        :returns: `False` if it's not physically possible to adjust it to
         this point.

        """
        y1 = self.GetY() - self.GetHeight() / 2.0

        if top <= y1:
            return False

        if test:
            return True

        newH = top - y1
        newY = y1 + newH / 2.0
        self.SetSize(self.GetWidth(), newH)

        dc = wx.MemoryDC()
        dc.SelectObject(self.GetCanvas().GetBuffer())
        self.GetCanvas().PrepareDC(dc)

        self.Move(dc, self.GetX(), newY)
        return True

    # Resize adjoining divisions.

    # Behaviour should be as follows:
    # If right edge moves, find all objects whose left edge
    # adjoins this object, and move left edge accordingly.
    # If left..., move ... right.
    # If top..., move ... bottom.
    # If bottom..., move top.
    # If size goes to zero or end position is other side of start position,
    # resize to original size and return.
    #
    def ResizeAdjoining(self, side, newPos, test):
        """
        Resize adjoining divisions at the given side.

        :param `side`: can be one of

        ======================= =======================
        Side option             Description
        ======================= =======================
        `DIVISION_SIDE_NONE`    no side
        `DIVISION_SIDE_LEFT`    Left side
        `DIVISION_SIDE_TOP`     Top side
        `DIVISION_SIDE_RIGHT`   Right side
        `DIVISION_SIDE_BOTTOM`  Bottom side
        ======================= =======================

        :param `newPos`: new position
        :param `test`: if `True`, just see whether it's possible for each
         adjoining region, returning `False` if it's not.

        """
        divisionParent = self.GetParent()
        for division in divisionParent.GetDivisions():
            if side == DIVISION_SIDE_LEFT:
                if division._rightSide == self:
                    success = division.AdjustRight(newPos, test)
                    if not success and test:
                        return False
            elif side == DIVISION_SIDE_TOP:
                if division._bottomSide == self:
                    success = division.AdjustBottom(newPos, test)
                    if not success and test:
                        return False
            elif side == DIVISION_SIDE_RIGHT:
                if division._leftSide == self:
                    success = division.AdjustLeft(newPos, test)
                    if not success and test:
                        return False
            elif side == DIVISION_SIDE_BOTTOM:
                if division._topSide == self:
                    success = division.AdjustTop(newPos, test)
                    if not success and test:
                        return False
        return True

    def EditEdge(self, side):
        print("EditEdge() not implemented.")

    def PopupMenu(self, x, y):
        """Popup menu handler."""
        menu = PopupDivisionMenu()
        menu.SetClientData(self)
        if self._leftSide:
            menu.Enable(DIVISION_MENU_EDIT_LEFT_EDGE, True)
        else:
            menu.Enable(DIVISION_MENU_EDIT_LEFT_EDGE, False)
        if self._topSide:
            menu.Enable(DIVISION_MENU_EDIT_TOP_EDGE, True)
        else:
            menu.Enable(DIVISION_MENU_EDIT_TOP_EDGE, False)

        x1, y1 = self._canvas.GetViewStart()
        unit_x, unit_y = self._canvas.GetScrollPixelsPerUnit()

        dc = wx.MemoryDC()
        dc.SelectObject(self.GetCanvas().GetBuffer())
        self.GetCanvas().PrepareDC(dc)

        mouse_x = dc.LogicalToDeviceX(x - x1 * unit_x)
        mouse_y = dc.LogicalToDeviceY(y - y1 * unit_y)

        self._canvas.PopupMenu(menu, (mouse_x, mouse_y))


