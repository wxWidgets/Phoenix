# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         diagram.py
# Purpose:      Diagram class
#
# Author:       Pierre Hjälm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# Copyright:    (c) 2004 Pierre Hjälm - 1998 Julian Smart
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, py3-port, documented
#----------------------------------------------------------------------------
"""
The :class:`~lib.ogl.diagram.Diagram` class.
"""
import wx

DEFAULT_MOUSE_TOLERANCE = 3


class Diagram(object):
    """
    The :class:`Diagram` encapsulates an entire diagram, with methods for
    drawing. A diagram has an associated :class:`ShapeCanvas`.

    """
    def __init__(self):
        """
        Default class constructor.
        """
        self._diagramCanvas = None
        self._quickEditMode = False
        self._snapToGrid = True
        self._gridSpacing = 5.0
        self._shapeList = []
        self._mouseTolerance = DEFAULT_MOUSE_TOLERANCE

    def Redraw(self, dc):
        """Redraw the shapes in the diagram on the specified device context."""
        if self._shapeList:
            for object in self._shapeList:
                object.Draw(dc)

    def Clear(self, dc):
        """Clear the specified device context."""
        dc.Clear()

    def AddShape(self, object, addAfter = None):
        """
        Add a shape to the diagram. If addAfter is not None, the shape
        will be added after addAfter.

        :param `object`: an instance of :class:`~lib.ogl.Shape`
        :param `addAfter`: an instance of :class:`~lib.ogl.Shape`

        """
        if not object in self._shapeList:
            if addAfter:
                self._shapeList.insert(self._shapeList.index(addAfter) + 1, object)
            else:
                self._shapeList.append(object)

            object.SetCanvas(self.GetCanvas())

    def InsertShape(self, object):
        """
        Insert a shape at the front of the shape list.

        :param `object`: an instance of :class:`~lib.ogl.Shape`

        """
        self._shapeList.insert(0, object)

    def RemoveShape(self, object):
        """
        Remove the shape from the diagram (non-recursively) but do not
        delete it.

        :param `object`: an instance of :class:`~lib.ogl.Shape`

        """
        if object in self._shapeList:
            self._shapeList.remove(object)

    def RemoveAllShapes(self):
        """Remove all shapes from the diagram but do not delete the shapes."""
        self._shapeList = []

    def DeleteAllShapes(self):
        """Remove and delete all shapes in the diagram."""
        for shape in self._shapeList[:]:
            if not shape.GetParent():
                self.RemoveShape(shape)
                shape.Delete()

    def ShowAll(self, show):
        """Call Show for each shape in the diagram.

        :param `show`: True or False

        """
        for shape in self._shapeList:
            shape.Show(show)

    def DrawOutline(self, dc, x1, y1, x2, y2):
        """
        Draw an outline rectangle on the current device context.

        :param `dc`: the :class:`wx.MemoryDC` device context
        :param `x1`: the x1 position
        :param `y2`: the y2 position
        :param `x1`: the x1 position
        :param `y2`: the y2 position

        """
        dc.SetPen(wx.Pen(wx.BLACK, 1, wx.PENSTYLE_DOT))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)

        dc.DrawLines([[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]])

    def RecentreAll(self, dc):
        """Recentre all the text that should be centred.

        :param `dc`: the :class:`wx.MemoryDC` device context

        """
        for shape in self._shapeList:
            shape.Recentre(dc)

    def SetCanvas(self, canvas):
        """
        Set the canvas associated with this diagram.

        :param `canvas`: an instance of :class:`~lib.ogl.Canvas`

        """
        self._diagramCanvas = canvas

    def GetCanvas(self):
        """Return the shape canvas associated with this diagram."""
        return self._diagramCanvas

    def FindShape(self, id):
        """
        Return the shape for the given identifier.

        :param `id`: the shape id to find

        """
        for shape in self._shapeList:
            if shape.GetId() == id:
                return shape
        return None

    def Snap(self, x, y):
        """
        'Snaps' the coordinate to the nearest grid position, if
        snap-to-grid is on.

        :param `x`: the x position
        :param `y`: the y position

        """
        if self._snapToGrid:
            return self._gridSpacing * int(x / self._gridSpacing + 0.5), self._gridSpacing * int(y / self._gridSpacing + 0.5)
        return x, y

    def SetGridSpacing(self, spacing):
        """
        Sets grid spacing.

        :param `spacing`: the spacing

        """
        self._gridSpacing = spacing

    def SetSnapToGrid(self, snap):
        """
        Sets snap-to-grid mode.

        :param `snap`: `True` to snap to grid or `False` not to snap

        """
        self._snapToGrid = snap

    def GetGridSpacing(self):
        """Return the grid spacing."""
        return self._gridSpacing

    def GetSnapToGrid(self):
        """Return snap-to-grid mode."""
        return self._snapToGrid

    def SetQuickEditMode(self, mode):
        """
        Set quick-edit-mode on of off.

        In this mode, refreshes are minimized, but the diagram may need
        manual refreshing occasionally.

        :param `mode`: `True` to quick edit or `False` for normal edit

        """
        self._quickEditMode = mode

    def GetQuickEditMode(self):
        """Return quick edit mode."""
        return self._quickEditMode

    def SetMouseTolerance(self, tolerance):
        """Set the tolerance within which a mouse move is ignored.

        The default is 3 pixels.

        :param `tolerance`: the tolerance level

        """
        self._mouseTolerance = tolerance

    def GetMouseTolerance(self):
        """Return the tolerance within which a mouse move is ignored."""
        return self._mouseTolerance

    def GetShapeList(self):
        """Return the internal shape list."""
        return self._shapeList

    def GetCount(self):
        """Return the number of shapes in the diagram."""
        return len(self._shapeList)
