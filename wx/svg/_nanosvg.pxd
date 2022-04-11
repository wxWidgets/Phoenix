#----------------------------------------------------------------------
# Name:        _nanosvg.pdx
# Purpose:     Cython decarlations for the items in the nanosvg code
#              we're wrapping. See https://github.com/memononen/nanosvg and
#              {Phoenix}/ext/nanosvg/src
#
# Author:      Robin Dunn
#
# Created:     23-July-2019
# Copyright:   (c) 2019-2020 by Total Control Software
# Licence:     wxWindows license
#----------------------------------------------------------------------

# Declare all the C stuff in the nanosvg header files that we'll be using.

cdef extern from 'nanosvg.h':

    enum NSVGpaintType:
        NSVG_PAINT_NONE
        NSVG_PAINT_COLOR
        NSVG_PAINT_LINEAR_GRADIENT
        NSVG_PAINT_RADIAL_GRADIENT

    enum NSVGspreadType:
        NSVG_SPREAD_PAD
        NSVG_SPREAD_REFLECT
        NSVG_SPREAD_REPEAT

    enum NSVGlineJoin:
        NSVG_JOIN_MITER
        NSVG_JOIN_ROUND
        NSVG_JOIN_BEVEL

    enum NSVGlineCap:
        NSVG_CAP_BUTT
        NSVG_CAP_ROUND
        NSVG_CAP_SQUARE

    enum NSVGfillRule:
        NSVG_FILLRULE_NONZERO
        NSVG_FILLRULE_EVENODD

    enum NSVGflags:
        NSVG_FLAGS_VISIBLE


    ctypedef struct NSVGgradientStop:
        unsigned int color
        float offset

    ctypedef struct NSVGgradient:
        float xform[6]
        char spread
        float fx
        float fy
        int nstops
        NSVGgradientStop *stops

    ctypedef struct NSVGpaint:
        char type
        unsigned int color
        NSVGgradient* gradient


    ctypedef struct NSVGpath:
        float *pts
        int npts
        char closed
        float bounds[4]
        NSVGpath *next

    ctypedef struct NSVGshape:
        char id[64]
        NSVGpaint fill
        NSVGpaint stroke
        float opacity
        float strokeWidth
        float strokeDashOffset
        float strokeDashArray[8]
        char strokeDashCount
        char strokeLineJoin
        char strokeLineCap
        char fillRule
        float miterLimit
        unsigned char flags
        float bounds[4]
        NSVGpath *paths
        NSVGshape *next

    ctypedef struct NSVGimage:
        float width
        float height
        NSVGshape *shapes

    cdef NSVGimage *nsvgParseFromFile(const char *filename, const char *units, float dpi)
    cdef NSVGimage *nsvgParse(char *input, const char *units, float dpi)
    cdef void nsvgDelete(NSVGimage *image)

    cdef NSVGpath* nsvgDuplicatePath(NSVGpath* p);

    cdef void nsvg__xformInverse(float* inv, float* t);
    cdef void nsvg__xformPoint(float* dx, float* dy, float x, float y, float* t)



cdef extern from 'nanosvgrast.h':
    ctypedef struct NSVGrasterizer

    cdef NSVGrasterizer* nsvgCreateRasterizer()
    cdef void nsvgDeleteRasterizer(NSVGrasterizer*)

    cdef void nsvgRasterize(
            NSVGrasterizer* r,
            NSVGimage* image, float tx, float ty, float scale,
            unsigned char* dst, int w, int h, int stride)
