# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:         bmpshape.py
# Purpose:      Bitmap shape
#
# Author:       Pierre Hjälm (from C++ original by Julian Smart)
#
# Created:      2004-05-08
# Copyright:    (c) 2004 Pierre Hjälm - 1998 Julian Smart
# Licence:      wxWindows license
# Tags:         phoenix-port, unittest, py3-port, documented
#----------------------------------------------------------------------------
"""
The :class:`~lib.ogl.bmpshape.BitmapShape` class.
"""
from .basic import RectangleShape


class BitmapShape(RectangleShape):
    """The :class:`BitmapShape` class draws a bitmap (non-resizable)."""
    def __init__(self):
        """
        Default class constructor.
        """
        RectangleShape.__init__(self, 100, 50)
        self._filename = ""

    def OnDraw(self, dc):
        """The draw handler."""
        if not self._bitmap.IsOk():
            return

        x = self._xpos - self._bitmap.GetWidth() / 2.0
        y = self._ypos - self._bitmap.GetHeight() / 2.0
        dc.DrawBitmap(self._bitmap, x, y, True)

    def SetSize(self, w, h, recursive = True):
        """
        Set the size.
        
        :param `w`: the width
        :param `h`: the heigth
        :param `recursive`: not used
        
        """

        if self._bitmap.IsOk():
            w = self._bitmap.GetWidth()
            h = self._bitmap.GetHeight()

        self.SetAttachmentSize(w, h)

        self._width = w
        self._height = h

        self.SetDefaultRegionSize()

    def GetBitmap(self):
        """Get the associated bitmap."""
        return self._bitmap
    
    def SetBitmap(self, bitmap):
        """Set the associated bitmap.
        
        :param `bitmap`: a :class:`wx.Bitmap` instance

        :note: You can delete the bitmap from the calling application, since
         reference counting will take care of holding on to the internal bitmap
         data.

        """
        self._bitmap = bitmap
        if self._bitmap.IsOk():
            self.SetSize(self._bitmap.GetWidth(), self._bitmap.GetHeight())
            
    def SetFilename(self, f):
        """Set the bitmap filename.
        
        :param str `f`: the bitmap file name
        
        """
        self._filename = f

    def GetFilename(self):
        """Return the bitmap filename."""
        return self._filename
