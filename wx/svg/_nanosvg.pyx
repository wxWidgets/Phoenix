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
    cdef NSVGrasterizer *_rasterizer

    def __cinit__(self):
        self._ptr = NULL
        self._rasterizer = NULL

    def __dealloc__(self):
        if self._ptr != NULL:
            nsvgDelete(self._ptr)
        if self._rasterizer != NULL:
            nsvgDeleteRasterizer(self._rasterizer)

    def _check_ptr(self):
        if self._ptr == NULL:
            raise ValueError("SVG not yet loaded")


    @staticmethod
    cdef SVGimage from_ptr(NSVGimage *ptr):
        obj = SVGimage()
        obj._ptr = ptr
        return obj


    @staticmethod
    def CreateFromFile(str filename, str units='px', float dpi=96) -> SVGimage:
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
    def CreateFromBytes(bytes buffer, str units='px', float dpi=96) -> SVGimage:
        """
        Loads an SVG image from a bytes object.

        :param bytes `buffer`: object containing the SVG data
        :param str `units`: One of: 'px', 'pt', 'pc' 'mm', 'cm', or 'in'
        :param float `dpi`: controls how the unit conversion is done

        :rtype: SVGimage
        """
        img = SVGimage.from_ptr(nsvgParse(buffer, bytes(units, 'utf-8'), dpi))
        if img._ptr == NULL:
            raise RuntimeError('Unable to parse SVG buffer')
        return img

    def __repr__(self) -> str:
        if self._ptr:
            return "SVGimage: size ({}, {})".format(self.width, self.height)
        else:
            return "SVGimage: <uninitialized>"


    def RasterizeToBytes(self, float tx=0.0, float ty=0.0, float scale=1.0,
                         int width=-1, int height=-1, int stride=-1) -> bytes:
        """
        """
        self._check_ptr()
        if self._rasterizer == NULL:
            self._rasterizer = nsvgCreateRasterizer()

        if width == -1:
            width = self.width
        if height == -1:
            height = self.height
        if stride == -1:
            stride = width * 4;

        buffer = bytes(height * stride)
        nsvgRasterize(self._rasterizer, self._ptr, tx, ty, scale, buffer,
                      width, height, stride)
        return buffer



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

    def __repr__(self):
        if self._ptr:
            return "SVGshape: id:{} bounds:{}".format(self.id, self.bounds)
        else:
            return "SVGshape: <uninitialized>"

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
cdef class SVGpath:
    """
    An SVGpath is essentially just a collection of bezier curves, defined by a
    set of floating point coordinates. A collection of SVGpaths is accessible
    from the `paths` attribute of SVGshape.
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

    def __repr__(self):
        if self._ptr:
            return "SVGpath: bounds:{}".format(self.bounds)
        else:
            return "SVGpath: <uninitialized>"

    @property
    def pts(self) -> list:
        """
        Cubic bezier points: x0,y0, [cpx1,cpx1,cpx2,cpy2,x1,y1], ...
        The return value is a list of floats.
        """
        self._check_ptr()
        return [self._ptr.pts[i] for i in range(self._ptr.npts*2)]

    @property
    def npts(self) -> int:
        """ Number of points """
        self._check_ptr()
        return self._ptr.npts

    @property
    def points(self) -> list:
        """
        Cubic bezier points: (x0,y0), [(cpx1,cpx1), (cpx2,cpy2), (x1,y1)], ...
        The return value is a list of tuples, each containing an x-y pair.
        """
        self._check_ptr()
        return [(self._ptr.pts[i], self._ptr.pts[i+1])
                for i in range(0, self._ptr.npts*2, 2)]

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
    def color_rgba(self) -> tuple:
        """ Returns color as a RGBA tuple """
        c = self.color
        return ( c        & 0xff,
                (c >> 8)  & 0xff,
                (c >> 16) & 0xff,
                (c >> 24) & 0xff)

    @property
    def gradient(self) -> SVGgradient:
        self._check_ptr()
        if self.type not in [SVG_PAINT_LINEAR_GRADIENT, SVG_PAINT_RADIAL_GRADIENT]:
            raise ValueError("Gradient not valid in this paint object")
        return SVGgradient.from_ptr(self._ptr.gradient)


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
        return int(self._ptr.spread)

    @property
    def fx(self) -> float:
        self._check_ptr()
        return self._ptr.fx

    @property
    def fy(self) -> float:
        self._check_ptr()
        return self._ptr.fy

    @property
    def stops(self):
        """
        A generator that iterates over the SVGgradientStops contained in the SVGgradient
        """
        self._check_ptr()
        for i in range(self._ptr.nstops):
            yield SVGgradientStop.from_ptr(&self._ptr.stops[i])

    @property
    def linearPoints(self) -> tuple:
        """
        For linear gradients this returns the start and stop points as tuples
        of the form ((x1,y1), (x2,y2)).
        """
        # nanosvg normalizes the start and stop points to (0,0) and (0,1) and
        # provides the transform used to do so. To get back the original x1,y1
        # and x2,y2 we need to invert the transform.
        # See https://github.com/memononen/nanosvg/issues/26

        cdef float inverse[6]
        cdef float x1, y1, x2, y2
        nsvg__xformInverse(inverse, self._ptr.xform)

        nsvg__xformPoint(&x1, &y1, 0, 0, inverse)
        nsvg__xformPoint(&x2, &y2, 0, 1, inverse)

        return ((x1,y1), (x2,y2))

    @property
    def radialPointRadius(self) -> tuple:
        """
        For radial gradients this returns the center point and the radius as a
        tuple of the form ((cx, cy), radius).
        """
        cdef float inverse[6]
        cdef float cx, cy, radius
        cdef float r1, r2
        nsvg__xformInverse(inverse, self._ptr.xform)

        nsvg__xformPoint(&cx, &cy, 0, 0, inverse)
        nsvg__xformPoint(&r1, &r2, 0, 1, inverse)
        radius = r2 - r1

        return ((cx, cy), radius)



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
    def color_rgba(self) -> tuple:
        """ Returns color as a RGBA tuple """
        c = self.color
        return ( c        & 0xff,
                (c >> 8)  & 0xff,
                (c >> 16) & 0xff,
                (c >> 24) & 0xff)

    @property
    def offset(self) -> float:
        self._check_ptr()
        return self._ptr.offset


#----------------------------------------------------------------------------
