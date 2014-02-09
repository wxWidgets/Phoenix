# Name:         dcgraphics.py 
# Package:      wx.lib.pdfviewer
#
# Purpose:      A wx.GraphicsContext-like API implemented using wx.DC
#               based on wx.lib.graphics by Robin Dunn
#
# Author:       David Hughes     dfh@forestfield.co.uk
# Copyright:    Forestfield Software Ltd
# Licence:      Same as wxPython host

# History:       8 Aug 2009 - created
#               12 Dec 2011 - amended DrawText
#
# Tags:         phoenix-port, unittest, documented
#
#----------------------------------------------------------------------------
"""
This module implements an API similar to :class:`GraphicsContext` and the
related classes. The implementation is done using :class:`DC`

Why do this?  Neither :class:`GraphicsContext` nor the Cairo-based
GraphicsContext API provided by wx.lib.graphics can be written
directly to a :class:`PrinterDC`. It can be done via an intermediate bitmap in
a :class:`MemoryDC` but transferring this to a :class:`PrinterDC` is an order of
magnitude slower than writing directly.

Why not just use :class:`PrinterDC` directly?  There may be times when you do want
to use :class:`GraphicsContext` for its displayed appearance and for its
clean(er) API, so being able to use the same code for printing as well is nice.

It started out with the intention of being a full implementation of the 
GraphicsContext API but so far only contains the sub-set required to render PDF.
It also contains the co-ordinate twiddles for the PDF origin, which would need
to be separated out if this was ever developed to be more general purpose.
"""
import copy
from math import asin, pi
import bezier
import wx

class dcGraphicsState:
    """
    Each instance holds the current graphics state. It can be
    saved (pushed) and restored (popped) by the owning parent.
    """
    def __init__ (self):
        """
        Default constructor, creates an instance with default values.
        """
        self.Yoffset = 0.0
        self.Xtrans = 0.0
        self.Ytrans = 0.0
        self.Xscale = 1.0
        self.Yscale = 1.0
        self.sinA = 0.0
        self.cosA = 1.0
        self.tanAlpha = 0.0
        self.tanBeta = 0.0
        self.rotDegrees = 0

    def Ytop(self, y):
        """
        Return y co-ordinate wrt top of current page
        
        :param integer `y`: y co-ordinate **TBW** (?)
        """
        return self.Yoffset + y

    def Translate(self, dx, dy):
        """
        Move the origin from the current point to (dx, dy).
        
        :param `dx`: x co-ordinate to move to **TBW** (?)
        :param `dy`: y co-ordinate to move to **TBW** (?)
        
        """
        self.Xtrans += (dx * self.Xscale)
        self.Ytrans += (dy * self.Yscale)

    def Scale(self, sx, sy):
        """
        Scale the current co-ordinates.
        
        :param `sx`: x co-ordinate to scale to **TBW** (?)
        :param `sy`: y co-ordinate to scale to **TBW** (?)

        """
        self.Xscale *= sx
        self.Yscale *= sy

    def Rotate(self, cosA, sinA):
        """
        Compute the (text only) rotation angle
        sinA is inverted to cancel the original inversion in
        pdfviewer.drawfile that was introduced because of the difference
        in y direction between pdf and GraphicsContext co-ordinates.
        
        :param `cosA`: **TBW** (?)
        :param `sinA`: **TBW** (?)
        
        """
        self.cosA = cosA
        self.sinA = sinA
        self.rotDegrees += asin(-self.sinA) * 180 / pi

    def Skew(self, tanAlpha, tanBeta):
        """
        **TBW** (?)
        
        :param `tanAlpha`: **TBW** (?)
        :param `tanBeta`: **TBW** (?)
        """
        self.tanAlpha = tanAlpha
        self.tanBeta = tanBeta

    def Get_x(self, x=0, y=0):
        """
        Return x co-ordinate using graphic states and transforms
        
        :param `x`: current x co-ordinats
        :param `y`: current y co-ordinats

        """
        return ((x*self.cosA*self.Xscale - y*self.sinA*self.Yscale) + self.Xtrans)

    def Get_y(self, x=0, y=0):
        """
        Return y co-ordinate using graphic states and transforms
        
        :param `x`: current x co-ordinats
        :param `y`: current y co-ordinats

        """
        return self.Ytop((x*self.sinA*self.Xscale + y*self.cosA*self.Yscale) + self.Ytrans)

    def Get_angle(self):
        """
        Return rotation angle in degrees.
        """
        return self.rotDegrees

#----------------------------------------------------------------------------

class dcGraphicsContext(object):

    def __init__(self, context=None, yoffset=0, have_cairo=False):
        """
        The incoming co-ordinates have a bottom left origin with increasing
        y downwards (so y values are all negative). The DC origin is top left
        also with increasing y down.
        :class:`DC` and :class:`GraphicsContext` fonts are too big in the ratio
        of pixels per inch to points per inch. If screen rendering used Cairo,
        printed fonts need to be scaled but if :class:`GCDC` was used, they are
        already scaled.
        
        :param `context`: **TBW** (?)
        :param integer `yoffset`: informs us of the page height
        :param boolean `have_cairo`: is Cairo used
        
        """
        self._context = context
        self.gstate = dcGraphicsState()
        self.saved_state = []
        self.gstate.Yoffset = yoffset
        self.fontscale = 1.0
        if have_cairo and wx.PlatformInfo[1] == 'wxMSW':
            self.fontscale =  72.0 / 96.0


    @staticmethod
    def Create(dc, yoffset, have_cairo):
        """
        The created pGraphicsContext instance uses the dc itself.
        """
        assert isinstance(dc, wx.DC)
        return dcGraphicsContext(dc, yoffset, have_cairo)
      
    def CreateMatrix(self, a=1.0, b=0, c=0, d=1.0, tx=0, ty=0):
        """
        Create a new matrix object.
        """
        m = dcGraphicsMatrix()
        m.Set(a, b, c, d, tx, ty)
        return m
    
    def CreatePath(self):
        """
        Create a new path obejct.
        """
        return dcGraphicsPath(parent=self)

    def PushState(self):
        """
        Makes a copy of the current state of the context and saves it
        on an internal stack of saved states.  The saved state will be
        restored when PopState is called.
        """
        self.saved_state.append(copy.deepcopy(self.gstate))

    def PopState(self):
        """
        Restore the most recently saved state which was saved with PushState.
        """
        self.gstate = self.saved_state.pop()

    def Scale(self, xScale, yScale):
        """
        Sets the dc userscale factor.
        
        :param `xScale`: **TBW** (?)
        :param `yScale`: **TBW** (?)
        
        """
        self._context.SetUserScale(xScale, yScale)
       
    def ConcatTransform(self, matrix):
        """
        Modifies the current transformation matrix by applying matrix
        as an additional transformation.
        """
        g = self.gstate
        a, b, c, d, e, f = map(float, matrix.Get())
        g.Translate(e, f)
        if d == a and c == -b and b != 0:
            g.Rotate(a, b)
        else:    
            g.Scale(a, d)
            g.Skew(b,c)

    def SetPen(self, pen):
        """
        Set the :class:`Pen` to be used for stroking lines in future drawing
        operations.
        
        :param `pen`: the :class:`Pen` to be used from now on.
        
        """
        self._context.SetPen(pen)

    def SetBrush(self, brush):
        """
        Set the :class:`Brush` to be used for filling shapes in future drawing
        operations.  

        :param `brush`: the :class:`Brush` to be used from now on.

        """
        self._context.SetBrush(brush)

    def SetFont(self, font, colour=None):
        """
        Sets the :class:`Font` to be used for drawing text.
        Don't set the dc font yet as it may need to be scaled
        
        :param `font`: the :class:`Font` for drawing text
        :param `colour`: the colour to be used
        
        """
        self._font = font
        if colour is not None:
            self._context.SetTextForeground(colour)

    def StrokePath(self, path):
        """
        Strokes the path (draws the lines) using the current pen.
        
        :param `path`: path to draw line on
        """
        raise NotImplementedError("TODO")
            
                                      
    def FillPath(self, path, fillStyle=wx.ODDEVEN_RULE):
        """
        Fills the path using the current brush.
        
        :param `path`: path to draw line on
        :param `fillStyle`: the fill style to use
        """
        raise NotImplementedError("TODO")
            

    def DrawPath(self, path, fillStyle=wx.ODDEVEN_RULE):
        """
        Draws the path using current pen and brush.

        :param `path`: path to draw line on
        :param `fillStyle`: the fill style to use

        """
        pathdict = {'SetPen': self._context.SetPen,
                    'DrawLine': self._context.DrawLine,
                    'DrawRectangle': self._context.DrawRectangle,
                    'DrawSpline': self._context.DrawSpline}
        for pathcmd, args, kwargs in path.commands:
            pathdict[pathcmd](*args, **kwargs)
        if path.allpoints:    
            self._context.DrawPolygon(path.allpoints, 0, 0, fillStyle)
        

    def DrawText(self, text, x, y, backgroundBrush=None):
        """
        Set the dc font at the required size.
        Ensure original font is not altered
        Draw the text at (x, y) using the current font.
        
        :param `text`: the text to draw
        :param `x`: x co-ordinates for text
        :param `y`: y co-ordinates for text
        :param `backgroundBrush`: curently ignored
        
        """
        g = self.gstate
        orgsize = self._font.GetPointSize()
        newsize = orgsize * (g.Xscale * self.fontscale)

        self._font.SetPointSize(newsize)
        self._context.SetFont(self._font)
        self._context.DrawRotatedText(text, g.Get_x(x, y), g.Get_y(x, y), g.Get_angle())
        self._font.SetPointSize(orgsize)
           

    def DrawBitmap(self, bmp, x, y, w=-1, h=-1):
        """
        Draw the bitmap
        
        :param `bmp`: the bitmap to draw
        :param `x`: the x co-ordinate for the bitmap
        :param `y`: the y co-ordinate for the bitmap
        :param `w`: currently ignored
        :param `h`: currently ignored
        
        """
        g = self.gstate
        self._context.DrawBitmap(bmp, g.Get_x(x, y), g.Get_y(x, y))

#---------------------------------------------------------------------------

class dcGraphicsMatrix(object):
    """
    A matrix holds an affine transformations, such as a scale,
    rotation, shear, or a combination of these, and is used to convert
    between different coordinante spaces.
    """
    def __init__(self):
        """
        The default constructor
        """
        self._matrix = ()


    def Set(self, a=1.0, b=0.0, c=0.0, d=1.0, tx=0.0, ty=0.0):
        """
        Set the componenets of the matrix by value, default values
        are the identity matrix.
        
        :param `a`: **TBW** (?)
        :param `b`: **TBW** (?)
        :param `c`: **TBW** (?)
        :param `d`: **TBW** (?)
        :param `tx`: **TBW** (?)
        :param `ty`: **TBW** (?)
        
        
        """
        self._matrix = (a, b, c, d, tx, ty)


    def Get(self):
        """
        Return the component values of the matrix as a tuple.
        """
        return tuple(self._matrix)

#---------------------------------------------------------------------------

class dcGraphicsPath(object):
    """
    A GraphicsPath is a representaion of a geometric path, essentially
    a collection of lines and curves.  Paths can be used to define
    areas to be stroked and filled on a GraphicsContext.
    """
    def __init__(self, parent=None):
        """
        A path is essentially an object that we use just for
        collecting path moves, lines, and curves in order to apply
        them to the real context using DrawPath.
        """
        self.commands = []
        self.allpoints = []
        if parent:
            self.gstate = parent.gstate
        self.fillcolour = parent._context.GetBrush().GetColour()
        self.isfilled = parent._context.GetBrush().GetStyle() != wx.BRUSHSTYLE_TRANSPARENT

    def AddCurveToPoint(self, cx1, cy1, cx2, cy2, x, y):
        """
        Adds a cubic Bezier curve from the current point, using two
        control points and an end point.

        :param `cx1`: **TBW** (?)
        :param `cy1`: **TBW** (?)
        :param `cx2`: **TBW** (?)
        :param `cy2`: **TBW** (?)
        :param `x`: **TBW** (?)
        :param `y`: **TBW** (?)
        
        """
        g = self.gstate
        clist = []
        clist.append(wx.RealPoint(self.xc, self.yc))
        clist.append(wx.RealPoint(g.Get_x(cx1, cy1), g.Get_y(cx1, cy1))) 
        clist.append(wx.RealPoint(g.Get_x(cx2, cy2), g.Get_y(cx2, cy2))) 
        clist.append(wx.RealPoint(g.Get_x(x, y), g.Get_y(x, y))) 
        self.xc, self.yc = clist[-1]
        plist = bezier.compute_points(clist, 64)
        if self.isfilled:
            self.allpoints.extend(plist)
        else:
            self.commands.append(['DrawSpline', (plist,), {}])

    def AddLineToPoint(self, x, y):
        """
        Adds a straight line from the current point to (x, y)
        
        :param `x`: **TBW** (?)
        :param `y`: **TBW** (?)

        """
        x2 = self.gstate.Get_x(x, y)
        y2 = self.gstate.Get_y(x, y)
        if self.isfilled:
            self.allpoints.extend([wx.Point(self.xc, self.yc), wx.Point(x2, y2)])
        else: 
            self.commands.append(['DrawLine', (self.xc, self.yc, x2, y2), {}])
        self.xc = x2
        self.yc = y2

    def AddRectangle(self, x, y, w, h):
        """
        Adds a new rectangle as a closed sub-path.
        
        :param `x`: **TBW** (?)
        :param `y`: **TBW** (?)
        :param `w`: **TBW** (?)
        :param `h`: **TBW** (?)
        
        """
        g = self.gstate
        xr = g.Get_x(x, y)
        yr = g.Get_y(x, y)
        wr = w*g.Xscale*g.cosA - h*g.Yscale*g.sinA
        hr = w*g.Xscale*g.sinA + h*g.Yscale*g.cosA
        if round(wr) == 1 or round(hr) == 1:    # draw thin rectangles as lines
            self.commands.append(['SetPen', (wx.Pen(self.fillcolour, 1.0),), {}])
            self.commands.append(['DrawLine', (xr, yr, xr+wr-1, yr+hr), {}])
        else:
            self.commands.append(['DrawRectangle', (xr, yr, wr, hr), {}])

    def CloseSubpath(self):
        """
        Adds a line segment to the path from the current point to the
        beginning of the current sub-path, and closes this sub-path.
        """
        if self.isfilled:
            self.allpoints.extend([wx.Point(self.xc, self.yc), wx.Point(self.x0, self.y0)])

    def MoveToPoint(self, x, y):
        """
        Begins a new sub-path at (x,y) by moving the "current point" there.
        """
        self.x0 = self.xc = self.gstate.Get_x(x, y)
        self.y0 = self.yc = self.gstate.Get_y(x, y)
    

