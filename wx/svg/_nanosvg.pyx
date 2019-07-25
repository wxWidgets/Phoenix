#----------------------------------------------------------------------
# Name:        wx.svg._nanosvg.pyx
# Purpose:     Cython-based wrappers for the nanosvg C code. See
#              https://github.com/memononen/nanosvg
# 
# Author:      Robin Dunn
#
# Created:     23-July-2019
# Copyright:   (c) 2019 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------

import sys

#----------------------------------------------------------------------------
# Replicate the C enums and values for Python, dropping the leading 'N'

cpdef enum SVGpaintType:
    SVG_PAINT_NONE = NSVG_PAINT_NONE
    SVG_PAINT_COLOR = NSVG_PAINT_COLOR
    SVG_PAINT_LINEAR_GRADIENT = NSVG_PAINT_LINEAR_GRADIENT
    SVG_PAINT_RADIAL_GRADIENT = NSVG_PAINT_RADIAL_GRADIENT

cpdef enum SVGspreadType:
    SVG_SPREAD_PAD = NSVG_SPREAD_PAD
    SVG_SPREAD_REFLECT = NSVG_SPREAD_REFLECT
    SVG_SPREAD_REPEAT = NSVG_SPREAD_REPEAT

cpdef enum SVGlineJoin:
    SVG_JOIN_MITER = NSVG_JOIN_MITER
    SVG_JOIN_ROUND = NSVG_JOIN_ROUND
    SVG_JOIN_BEVEL = NSVG_JOIN_BEVEL

cpdef enum SVGlineCap:
    SVG_CAP_BUTT = NSVG_CAP_BUTT
    SVG_CAP_ROUND = NSVG_CAP_ROUND
    SVG_CAP_SQUARE = NSVG_CAP_SQUARE

cpdef enum SVGfillRule:
    SVG_FILLRULE_NONZERO = NSVG_FILLRULE_NONZERO
    SVG_FILLRULE_EVENODD = NSVG_FILLRULE_EVENODD

cpdef enum SVGflags:
    SVG_FLAGS_VISIBLE = NSVG_FLAGS_VISIBLE


#----------------------------------------------------------------------------
# Cython classes for wrapping the nanosvg structs

# SVGimage
cdef class SVGimage:
    """ 
    An SVGimage can be created either from an SVG file or from an in-memory
    buffer containind the SVG XML code. The result is a collection of cubic
    bezier shapes, with fill, stroke, paths and other information.    
    """ 
    cdef NSVGimage *_ptr

    def __cinit__(self):
        self._ptr = NULL
    
    def __dealloc__(self):
        if self._ptr != NULL:
            nsvgDelete(self._ptr)

    def _check_ptr(self):
        if self._ptr == NULL:
            raise ValueError("SVG not yet loaded")

    @staticmethod
    cdef SVGimage from_ptr(NSVGimage *ptr):
        obj = SVGimage()
        obj._ptr = ptr
        return obj

    @staticmethod
    def from_file(str filename, str units='px', float dpi=96) -> SVGimage:
        """ 
        Loads an SVG image from a file.

        :param str `filename`: Name of the file to load the SVG image from
        :param str `units`: One of: 'px', 'pt', 'pc' 'mm', 'cm', or 'in'  
        :param float `dpi`: controls how the unit conversion is done  

        :rtype: SVGimage
        """
        name = filename.encode(sys.getfilesystemencoding())
        img = SVGimage.from_ptr(nsvgParseFromFile(name, bytes(units, 'utf-8'), dpi))
        if img._ptr == NULL:
            raise RuntimeError('Unable to parse SVG file {}'.format(filename))
        return img

    @staticmethod
    def from_buffer(char[:] buff, str units='px', float dpi=96) -> SVGimage:
        """ 
        Loads an SVG image from a buffer object (bytes, bytearray, memoryview, arrary of char, etc.)

        :param buffer `buff`: object containing the SVG data
        :param str `units`: One of: 'px', 'pt', 'pc' 'mm', 'cm', or 'in'  
        :param float `dpi`: controls how the unit conversion is done  

        :rtype: SVGimage
        """
        cdef char *pbuff = &buff[0]
        img = SVGimage.from_ptr(nsvgParse(pbuff, bytes(units, 'utf-8'), dpi))
        if img._ptr == NULL:
            raise RuntimeError('Unable to parse SVG buffer')
        return img
        

    @property
    def width(self) -> float:
        """
        Returns the width of the SVGimage
        """
        self._check_ptr()
        return self._ptr.width

    @property
    def height(self) -> float:
        """
        Returns the height of the SVGimage
        """
        self._check_ptr()
        return self._ptr.height

    @property
    def shapes(self):
        """
        A generator that iterates over the shapes that comprise the SVGimage
        """
        self._check_ptr()
        cdef NSVGshape *shape = self._ptr.shapes
        while shape != NULL:
            yield SVGshape.from_ptr(shape)
            shape = shape.next


#----------------------------------------------------------------------------

cdef class SVGshape:
    """
    SVGshape is a set of attributes describing how to draw one shape in the SVG,
    including stroke and fill styles, line styles, and paths. A collection of 
    SVGshapes is accessible from the `shapes` attribute of SVGimage.
    """
    cdef NSVGshape *_ptr

    def __cinit__(self):
        self._ptr = NULL
    
    def _check_ptr(self):
        if self._ptr == NULL:
            raise ValueError("Invalid SVGshape")

    @staticmethod
    cdef SVGshape from_ptr(NSVGshape *ptr):
        obj = SVGshape()
        obj._ptr = ptr
        return obj

    @property
    def id(self):
        """ Optional 'id' attr of the shape or its group """
        self._check_ptr()
        return self._ptr.id

    @property
    def fill(self) -> SVGpaint:
        """ Fill paint """
        self._check_ptr()
        return SVGpaint.from_ptr(&self._ptr.fill)

    @property
    def stroke(self) -> SVGpaint:
        """ Stroke paint """
        self._check_ptr()
        return SVGpaint.from_ptr(&self._ptr.stroke)

    @property
    def opacity(self) -> float:
        """ Opacity of the shape. """
        self._check_ptr()
        return self._ptr.opacity

    @property
    def strokeWidth(self) -> float:
        """ Stroke width (scaled) """
        self._check_ptr()
        return self._ptr.strokeWidth

    @property
    def strokeDashOffset(self) -> float:
        """ Stroke dash offset (scaled) """
        self._check_ptr()
        return self._ptr.strokeDashOffset

    @property
    def strokeDashArray(self) -> list:
        """ Stroke dash array (scaled) """
        self._check_ptr()
        return [self._ptr.strokeDashArray[i] 
                for i in range(self._ptr.strokeDashCount)]

    @property
    def strokeLineJoin(self) -> SVGlineJoin:
        """ Stroke join type """
        self._check_ptr()
        return SVGlineJoin(self._ptr.strokeLineJoin)

    @property
    def strokeLineCap(self) -> SVGlineCap:
        """ Stroke cap type """
        self._check_ptr()
        return SVGlineCap(self._ptr.strokeLineCap)

    @property
    def fillRule(self) -> SVGfillRule:
        """ Fill rule """
        self._check_ptr()
        return SVGfillRule(self._ptr.fillRule)

    @property
    def miterLimit(self) -> float:
        """ Miter limit """
        self._check_ptr()
        return self._ptr.miterLimit

    @property
    def flags(self) -> int:
        """ Logical OR of SVG_FLAGS_* flags """
        self._check_ptr()
        return int(self._ptr.flags)

    @property
    def bounds(self) -> list:
        """ Tight bounding box of the shape [minx,miny,maxx,maxy] """
        self._check_ptr()
        return [self._ptr.bounds[i] for i in range(4)]

    @property
    def minx(self) -> float:
        self._check_ptr()
        return self._ptr.bounds[0]
        
    @property
    def miny(self) -> float:
        self._check_ptr()
        return self._ptr.bounds[1]
        
    @property
    def maxx(self) -> float:
        self._check_ptr()
        return self._ptr.bounds[2]
        
    @property
    def maxy(self) -> float:
        self._check_ptr()
        return self._ptr.bounds[3]
        
    @property
    def paths(self):
        """
        A generator that iterates over the paths contained in the SVGshape
        """
        self._check_ptr()
        cdef NSVGpath *path = self._ptr.paths
        while path != NULL:
            yield SVGpath.from_ptr(path)
            path = path.next


#----------------------------------------------------------------------------
cdef class SVGpaint:
    """
    """
    cdef NSVGpaint *_ptr

    def __cinit__(self):
        self._ptr = NULL
    
    @staticmethod
    cdef SVGpaint from_ptr(NSVGpaint *ptr):
        obj = SVGpaint()
        obj._ptr = ptr
        return obj

    def _check_ptr(self):
        if self._ptr == NULL:
            raise ValueError("Invalid SVGpaint")

    @property
    def type(self) -> SVGpaintType:
        """ Flag indicating the type of paint info, solid color or type of gradient """
        self._check_ptr()
        return SVGpaintType(self._ptr.type)

    @property
    def color(self) -> uint:
        self._check_ptr()
        if self.type != SVG_PAINT_COLOR:
            raise ValueError("Color not valid in this paint object")
        return self._ptr.color

    @property
    def gradient(self) -> SVGgradient:
        self._check_ptr()
        if self.type not in [SVG_PAINT_LINEAR_GRADIENT, SVG_PAINT_RADIAL_GRADIENT]:
            raise ValueError("Gradient not valid in this paint object")
        return SVGgradient.from_ptr(self._ptr.gradient)


#----------------------------------------------------------------------------
cdef class SVGgradientStop:
    """
    """
    cdef NSVGgradientStop *_ptr

    def __cinit__(self):
        self._ptr = NULL
    
    @staticmethod
    cdef SVGgradientStop from_ptr(NSVGgradientStop *ptr):
        obj = SVGgradientStop()
        obj._ptr = ptr
        return obj

    def _check_ptr(self):
        if self._ptr == NULL:
            raise ValueError("Invalid SVGgradientStop")

    @property
    def color(self) -> uint:
        self._check_ptr()
        return self._ptr.color

    @property
    def offset(self) -> float:
        self._check_ptr()
        return self._ptr.offset


#----------------------------------------------------------------------------
cdef class SVGgradient:
    """
    """
    cdef NSVGgradient *_ptr

    def __cinit__(self):
        self._ptr = NULL
    
    @staticmethod
    cdef SVGgradient from_ptr(NSVGgradient *ptr):
        obj = SVGgradient()
        obj._ptr = ptr
        return obj

    def _check_ptr(self):
        if self._ptr == NULL:
            raise ValueError("Invalid SVGgradient")

    @property
    def xform(self) -> list:
        self._check_ptr()
        return [self._ptr.xform[i] for i in range(6)]

    @property
    def spread(self) -> int:
        self._check_ptr()
        return int(self._pre.spread)

    @property
    def spread(self) -> int:
        self._check_ptr()
        return int(self._pre.spread)

    @property
    def fx(self) -> float:
        self._check_ptr()
        return self._pre.fx

    @property
    def fy(self) -> float:
        self._check_ptr()
        return self._pre.fy

    @property
    def stops(self):
        """
        A generator that iterates over the SVGgradientStops contained in the SVGgradient
        """
        self._check_ptr()
        for i in range(self._ptr.nstops):
            yield self._ptr.stops[i]

#----------------------------------------------------------------------------
cdef class SVGpath:
    """
    """
    cdef NSVGpath *_ptr

    def __cinit__(self):
        self._ptr = NULL
    
    @staticmethod
    cdef SVGpath from_ptr(NSVGpath *ptr):
        obj = SVGpath()
        obj._ptr = ptr
        return obj

    def _check_ptr(self):
        if self._ptr == NULL:
            raise ValueError("Invalid SVGpath")

    @property
    def pts(self) -> list:
        """ Cubic bezier points: x0,y0, [cpx1,cpx1,cpx2,cpy2,x1,y1], ... """
        self._check_ptr()
        return [self._ptr.pts[i] for i in range(self._ptr.npts)]

    @property
    def closed(self) -> bool:
        """ Flag indicating if shapes should be treated as closed """
        self._check_ptr()
        return bool(self._ptr.closed)

    @property
    def bounds(self) -> list:
        """ Tight bounding box of the shape [minx,miny,maxx,maxy] """
        self._check_ptr()
        return [self._ptr.bounds[i] for i in range(4)]

    @property
    def minx(self) -> float:
        self._check_ptr()
        return self._ptr.bounds[0]
        
    @property
    def miny(self) -> float:
        self._check_ptr()
        return self._ptr.bounds[1]
        
    @property
    def maxx(self) -> float:
        self._check_ptr()
        return self._ptr.bounds[2]
        
    @property
    def maxy(self) -> float:
        self._check_ptr()
        return self._ptr.bounds[3]
        

#----------------------------------------------------------------------------
