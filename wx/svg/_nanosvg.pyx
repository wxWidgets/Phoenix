#----------------------------------------------------------------------
# Name:        wx.svg._nanosvg.pyx
# Purpose:     Cython-based wrappers for the nanosvg C code. See
#              https://github.com/memononen/nanosvg
#
# Author:      Robin Dunn
#
# Created:     23-July-2019
# Copyright:   (c) 2019-2020 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------
"""
NanoSVG is a "simple stupid single-header-file SVG parser" from
https://github.com/memononen/nanosvg. The output of the parser is a collection
of data structures representing cubic bezier shapes.

NanoSVG supports a wide range of SVG features. The library is well suited for
anything from rendering scalable icons in your editor application to prototyping
a game. There is not a full coverage of the SVG specification, however the
features needed for typical icons or even more advanced vector images are
present.

The shapes in the SVG images are transformed by the viewBox and converted to
specified units. That is, you should get the same looking data as you designed
in your favorite app.

NanoSVG can return the paths in few different units. For example if you want to
render an image, you may choose to get the paths in pixels, or if you are
feeding the data into a CNC-cutter, you may want to use millimeters.

The units passed to NanoSVG should be one of: 'px', 'pt', 'pc' 'mm', 'cm', or
'in'. DPI (dots-per-inch) controls how the unit conversion is done.

If you don't know or care about the units stuff, "px" and 96 should get you
going.

This module implements a Cython-based wrapper for the NanoSVG code, providing
access to the parsed SVG data as a nested collection of objects and properties.
Note that these classes are essentially read-only. There is no support (yet?)
for manipulating the SVG shape info in memory.
"""

import sys

from cpython.buffer cimport (
    Py_buffer, PyObject_CheckBuffer, PyObject_GetBuffer, PyBUF_SIMPLE,
    PyBuffer_Release)

PY2 = sys.version_info[0] == 2

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

cdef class SVGimageBase:
    """
    A SVGimageBase can be created either from an SVG file or from an in-memory
    buffer containing the SVG XML code. The result is a collection of cubic
    bezier shapes, with fill, stroke, gradients, paths and other information.

    This class is a Cython-based wrapper around the nanosvg ``NSVGimage`` structure,
    providing just the basic wrapped functionality from nanosvg. Please see the
    :class:`wx.svg.SVGimage` class for a derived implementation that adds
    functionality for integrating with wxPython.
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

    cdef _check_ptr(self):
        if self._ptr == NULL:
            raise ValueError("SVG not yet loaded")

    cdef _set_ptr(self, NSVGimage *ptr, str errmsg='Unable to parse SVG'):
        if self._ptr != NULL:
            nsvgDelete(self._ptr)
        if self._rasterizer != NULL:
            nsvgDeleteRasterizer(self._rasterizer)
            self._rasterizer = NULL
        if ptr == NULL:
            raise ValueError(errmsg)
        self._ptr = ptr


    @staticmethod
    cdef SVGimageBase from_ptr(NSVGimage *ptr):
        obj = SVGimageBase()
        obj._ptr = ptr
        return obj


    @classmethod
    def CreateFromFile(cls, str filename, str units='px', float dpi=96):
        """
        Loads an SVG image from a file.

        :param str `filename`: Name of the file to load the SVG image from
        :param str `units`: One of: 'px', 'pt', 'pc' 'mm', 'cm', or 'in'
        :param float `dpi`: controls how the unit conversion is done

        :rtype: An instance of ``cls`` (usually a :class:`SVGimage`)
        """
        name = filename.encode(sys.getfilesystemencoding())
        units_b = units.encode('utf-8')
        cdef SVGimageBase img = cls()
        img._set_ptr(nsvgParseFromFile(name, units_b, dpi),
                     'Unable to parse SVG file {}'.format(filename))
        return img


    @classmethod
    def CreateFromBytes(cls, bytes buffer, str units='px', float dpi=96, bint do_copy=True):
        """
        Loads an SVG image from a bytes object.

        :param bytes `buffer`: object containing the SVG data
        :param str `units`: One of: 'px', 'pt', 'pc' 'mm', 'cm', or 'in'
        :param float `dpi`: controls how the unit conversion is done
        :param bool `do_copy`: indicates if the given bytes object should be
            copied to avoid in-place modification. This should be set to True
            if the given `buffer` object may ever be reused in any capacity.
            If the given `buffer` will only be used once, and the cost of copying
            it is problematic, then `do_copy` can be set to False.

        :rtype: An instance of ``cls`` (usually a :class:`SVGimage`)
        """

        if do_copy:
            # `nsvgParse` will end up modifying the char-array passed to it in-place
            # which will violate the immutability of python `bytes` objects.
            # To avoid this we're going to copy the given `buffer` object into
            # an entirely separate portion of memory. Unfortunately, python is a
            # step ahead of the game and optimizes copying byte strings into just
            # returning the same object (because they're immutable!), so to truly
            # get a different byte string we'll copy it via converting to a bytearray
            # and back:
            buffer = bytes(bytearray(buffer))

        units_b = units.encode('utf-8')
        cdef SVGimageBase img = cls()
        img._set_ptr(nsvgParse(buffer, units_b, dpi),
                     'Unable to parse SVG buffer')
        return img


    def __repr__(self) -> str:
        if self._ptr:
            return "SVGimageBase: size ({}, {})".format(self.width, self.height)
        else:
            return "SVGimageBase: <uninitialized>"


    def RasterizeToBuffer(self, object buf, float tx=0.0, float ty=0.0, float scale=1.0,
                         int width=-1, int height=-1, int stride=-1) -> bytes:
        """
        Renders the SVG image to an existing buffer as a series of RGBA values.

        The buffer object must support the Python buffer-protocol, be writable,
        and be at least ``width * height * 4`` bytes long. Possibilities include
        bytearrays, memoryviews, numpy arrays, etc.

        :param `buf`: An object supporting the buffer protocol where the RGBA bytes will be written
        :param float `tx`: Image horizontal offset (applied after scaling)
        :param float `ty`: Image vertical offset (applied after scaling)
        :param float `scale`: Image scale
        :param int `width`: width of the image to render, defaults to width from the SVG file
        :param int `height`: height of the image to render, defaults to height from the SVG file
        :param int `stride`: number of bytes per scan line in the destination buffer, typically ``width * 4``
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

        if not PyObject_CheckBuffer(buf):
            raise ValueError("Object does not support the python buffer protocol")

        cdef Py_buffer view
        if PyObject_GetBuffer(buf, &view, PyBUF_SIMPLE) != 0:
            raise ValueError("PyObject_GetBuffer failed")
        if view.len < height * stride:
            PyBuffer_Release(&view)
            raise ValueError("Buffer object is smaller than height * stride")

        nsvgRasterize(self._rasterizer, self._ptr, tx, ty, scale, <unsigned char*>view.buf,
                      width, height, stride)
        PyBuffer_Release(&view)


    def Rasterize(self, float tx=0.0, float ty=0.0, float scale=1.0,
                  int width=-1, int height=-1, int stride=-1) -> bytes:
        """
        Renders the SVG image to a ``bytes`` object as a series of RGBA values.

        :param float `tx`: Image horizontal offset (applied after scaling)
        :param float `ty`: Image vertical offset (applied after scaling)
        :param float `scale`: Image scale
        :param int `width`: width of the image to render, defaults to width from the SVG file
        :param int `height`: height of the image to render, defaults to height from the SVG file
        :param int `stride`: number of bytes per scan line in the destination buffer, typically ``width * 4``

        :returns: A bytearray object containing the raw RGBA pixel color values
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

        buf = bytes(bytearray(height * stride))
        nsvgRasterize(self._rasterizer, self._ptr, tx, ty, scale, buf,
                      width, height, stride)
        return buf

    @property
    def width(self) -> float:
        """
        Returns the width of the SVG image
        """
        self._check_ptr()
        return self._ptr.width

    @property
    def height(self) -> float:
        """
        Returns the height of the SVG image
        """
        self._check_ptr()
        return self._ptr.height

    @property
    def shapes(self):
        """
        A generator that iterates over the :class:`SVGshape` objects that comprise the SVG image
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
    SVGshapes is accessible from the ``shapes`` attribute of :class:`SVGimage`.
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
            return "SVGshape: id:{} bounds:{}".format(self.id.decode('utf-8'), self.bounds)
        else:
            return "SVGshape: <uninitialized>"

    @property
    def id(self):
        """Optional 'id' attr of the shape or its group"""
        self._check_ptr()
        return self._ptr.id

    @property
    def fill(self) -> SVGpaint:
        """:class:`SVGpaint` for the fill"""
        self._check_ptr()
        return SVGpaint.from_ptr(&self._ptr.fill)

    @property
    def stroke(self) -> SVGpaint:
        """:class:`SVGpaint` for the stroke"""
        self._check_ptr()
        return SVGpaint.from_ptr(&self._ptr.stroke)

    @property
    def opacity(self) -> float:
        """Opacity of the shape"""
        self._check_ptr()
        return self._ptr.opacity

    @property
    def strokeWidth(self) -> float:
        """Stroke width (scaled)"""
        self._check_ptr()
        return self._ptr.strokeWidth

    @property
    def strokeDashOffset(self) -> float:
        """Stroke dash offset (scaled)"""
        self._check_ptr()
        return self._ptr.strokeDashOffset

    @property
    def strokeDashArray(self) -> list:
        """Stroke dash array (scaled)"""
        self._check_ptr()
        return [self._ptr.strokeDashArray[i]
                for i in range(self._ptr.strokeDashCount)]

    @property
    def strokeLineJoin(self) -> SVGlineJoin:
        """Stroke join type"""
        self._check_ptr()
        return SVGlineJoin(self._ptr.strokeLineJoin)

    @property
    def strokeLineCap(self) -> SVGlineCap:
        """Stroke cap type"""
        self._check_ptr()
        return SVGlineCap(self._ptr.strokeLineCap)

    @property
    def fillRule(self) -> SVGfillRule:
        """Fill rule"""
        self._check_ptr()
        return SVGfillRule(self._ptr.fillRule)

    @property
    def miterLimit(self) -> float:
        """Miter limit"""
        self._check_ptr()
        return self._ptr.miterLimit

    @property
    def flags(self) -> int:
        """Logical OR of SVG_FLAGS_* flags"""
        self._check_ptr()
        return int(self._ptr.flags)

    @property
    def bounds(self) -> list:
        """Tight bounding box of the shape [minx,miny,maxx,maxy]"""
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
        A generator that iterates over the :class:`SVGpath` objects contained in the SVGshape
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
        """Number of points"""
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
        """Flag indicating if shapes should be treated as closed"""
        self._check_ptr()
        return bool(self._ptr.closed)

    @property
    def bounds(self) -> list:
        """Tight bounding box of the shape [minx,miny,maxx,maxy]"""
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
    This class defines how to fill or stroke a shape when rendering the SVG
    image. In other words, how to create the pen or brush. It can be a solid
    color, linear or radial gradients, etc.
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
        """Flag indicating the type of paint info, solid color or type of gradient"""
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
        """Returns color as a RGBA tuple"""
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
    A gradient is a method used to fade from one color to another, either
    linearly or radially.
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
        """The gradient's transform"""
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
        A generator that iterates over the :class:`SVGgradientStop` objects contained in the SVGgradient
        """
        self._check_ptr()
        for i in range(self._ptr.nstops):
            yield SVGgradientStop.from_ptr(&self._ptr.stops[i])


#----------------------------------------------------------------------------
cdef class SVGgradientStop:
    """
    A Gradient stop is an offset and a color, which is used when drawing gradients.
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
