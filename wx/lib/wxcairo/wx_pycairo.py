#----------------------------------------------------------------------
# Name:        wx_pycairo
# Purpose:     wx.lib.wxcairo implementation functions for PyCairo
#
# Author:      Robin Dunn
#
# Created:     3-Sept-2008
# Copyright:   (c) 2008-2018 by Total Control Software
# Licence:     wxWindows license
#
# Tags:        phoenix-port, py3-port
#----------------------------------------------------------------------

"""
wx.lib.wxcairo implementation functions using PyCairo.
"""

import wx
from six import PY3

import cairo
import ctypes
import ctypes.util


#----------------------------------------------------------------------------

# A reference to the cairo shared lib via ctypes.CDLL
cairoLib = None

# A reference to the pycairo C API structure
pycairoAPI = None


# a convenience function, just to save a bit of typing below
def voidp(ptr):
    """Convert a SIP void* type to a ctypes c_void_p"""
    return ctypes.c_void_p(int(ptr))

#----------------------------------------------------------------------------

def _ContextFromDC(dc):
    """
    Creates and returns a Cairo context object using the wxDC as the
    surface.  (Only window, client, paint and memory DC's are allowed
    at this time.)
    """
    if not isinstance(dc, wx.WindowDC) and not isinstance(dc, wx.MemoryDC):
        raise TypeError("Only window and memory DC's are supported at this time.")

    if 'wxMac' in wx.PlatformInfo:
        width, height = dc.GetSize()

        # use the CGContextRef of the DC to make the cairo surface
        cgc = dc.GetHandle()
        assert cgc is not None, "Unable to get CGContext from DC."
        cgref = voidp( cgc )
        surfaceptr = voidp(surface_create(cgref, width, height))

        # create a cairo context for that surface
        ctxptr = voidp(cairo_create(surfaceptr))

        # Turn it into a pycairo context object
        ctx = pycairoAPI.Context_FromContext(ctxptr, pycairoAPI.Context_Type, None)

        # The context keeps its own reference to the surface
        cairoLib.cairo_surface_destroy(surfaceptr)

    elif 'wxMSW' in wx.PlatformInfo:
        # This one is easy, just fetch the HDC and use PyCairo to make
        # the surface and context.
        hdc = dc.GetHandle()
        # Ensure the pointer value is clampped into the range of a C signed long
        hdc = ctypes.c_long(hdc)
        surface = cairo.Win32Surface(hdc.value)
        ctx = cairo.Context(surface)

    elif 'wxGTK' in wx.PlatformInfo:
        if 'gtk3' in wx.PlatformInfo:
            # With wxGTK3, GetHandle() returns a cairo context directly
            ctxptr = voidp( dc.GetHandle() )

            # pyCairo will try to destroy it so we need to increase ref count
            cairoLib.cairo_reference(ctxptr)
        else:
            # Get the GdkDrawable from the dc
            drawable = voidp( dc.GetHandle() )

            # Call a GDK API to create a cairo context
            ctxptr = gdkLib.gdk_cairo_create(drawable)

        # Turn it into a pycairo context object
        ctx = pycairoAPI.Context_FromContext(ctxptr, pycairoAPI.Context_Type, None)

    else:
        raise NotImplementedError("Help  me, I'm lost...")

    return ctx


#----------------------------------------------------------------------------

def _FontFaceFromFont(font):
    """
    Creates and returns a cairo.FontFace object from the native
    information in a wx.Font.
    """

    if 'wxMac' in wx.PlatformInfo:
        fontfaceptr = font_face_create(voidp(font.OSXGetCGFont()))
        fontface = pycairoAPI.FontFace_FromFontFace(fontfaceptr)

    elif 'wxMSW' in wx.PlatformInfo:
        fontfaceptr = voidp( cairoLib.cairo_win32_font_face_create_for_hfont(
            ctypes.c_ulong(font.GetHFONT())) )
        fontface = pycairoAPI.FontFace_FromFontFace(fontfaceptr)

    elif 'wxGTK' in wx.PlatformInfo:
        # wow, this is a hell of a lot of steps...
        desc = voidp( font.GetPangoFontDescription() )

        pcfm = voidp(pcLib.pango_cairo_font_map_get_default())

        pctx = voidp(gdkLib.gdk_pango_context_get())

        pfnt = voidp( pcLib.pango_font_map_load_font(pcfm, pctx, desc) )

        scaledfontptr = voidp( pcLib.pango_cairo_font_get_scaled_font(pfnt) )

        fontfaceptr = voidp(cairoLib.cairo_scaled_font_get_font_face(scaledfontptr))
        cairoLib.cairo_font_face_reference(fontfaceptr)

        fontface = pycairoAPI.FontFace_FromFontFace(fontfaceptr)

        gdkLib.g_object_unref(pctx)

    else:
        raise NotImplementedError("Help  me, I'm lost...")

    return fontface


#----------------------------------------------------------------------------
# Only implementation helpers after this point
#----------------------------------------------------------------------------

def _findCairoLib():
    """
    Try to locate the Cairo shared library and make a CDLL for it.
    """
    global cairoLib
    if cairoLib is not None:
        return

    names = ['cairo', 'cairo-2', 'libcairo', 'libcairo-2']

    # first look using just the base name
    for name in names:
        try:
            cairoLib = ctypes.CDLL(name)
            return
        except:
            pass

    # if that didn't work then use the ctypes util to search the paths
    # appropriate for the system
    for name in names:
        location = ctypes.util.find_library(name)
        if location:
            try:
                cairoLib = ctypes.CDLL(location)
                return
            except:
                pass

    # If the above didn't find it on OS X then we still have a
    # trick up our sleeve...
    if 'wxMac' in wx.PlatformInfo:
        # look at the libs linked to by the pycairo extension module
        import macholib.MachO
        m = macholib.MachO.MachO(cairo._cairo.__file__)
        for h in m.headers:
            for idx, name, path in h.walkRelocatables():
                if 'libcairo' in path:
                    try:
                        cairoLib = ctypes.CDLL(path)
                        return
                    except:
                        pass

    if not cairoLib:
        raise RuntimeError("Unable to find the Cairo shared library")



#----------------------------------------------------------------------------

# For other DLLs we'll just use a dictionary to track them, as there
# probably isn't any need to use them outside of this module.
_dlls = dict()

def _findHelper(names, key, msg):
    dll = _dlls.get(key, None)
    if dll is not None:
        return dll
    location = None
    for name in names:
        location = ctypes.util.find_library(name)
        if location:
            break
    if not location:
        raise RuntimeError(msg)
    dll = ctypes.CDLL(location)
    _dlls[key] = dll
    return dll


def _findGDKLib():
    if 'gtk3' in wx.PlatformInfo:
        libname = 'gdk-3'
    else:
        libname = 'gdk-x11-2.0'
    return _findHelper([libname], 'gdk',
                       "Unable to find the GDK shared library")

def _findPangoCairoLib():
    return _findHelper(['pangocairo-1.0'], 'pangocairo',
                       "Unable to find the pangocairo shared library")
def _findAppSvcLib():
    return _findHelper(['ApplicationServices'], 'appsvc',
                       "Unable to find the ApplicationServices Framework")


#----------------------------------------------------------------------------

# PyCairo exports a C API in a structure via a PyCObject.  Using
# ctypes will let us use that API from Python too.  We'll use it to
# convert a C pointer value to pycairo objects.  The information about
# this API structure is gleaned from pycairo.h.

class Pycairo_CAPI(ctypes.Structure):
    if cairo.version_info < (1,8):  # This structure is known good with pycairo 1.6.4
        _fields_ = [
            ('Context_Type', ctypes.py_object),
            ('Context_FromContext', ctypes.PYFUNCTYPE(ctypes.py_object,
                                                      ctypes.c_void_p,
                                                      ctypes.py_object,
                                                      ctypes.py_object)),
            ('FontFace_Type', ctypes.py_object),
            ('FontFace_FromFontFace', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('FontOptions_Type', ctypes.py_object),
            ('FontOptions_FromFontOptions', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Matrix_Type', ctypes.py_object),
            ('Matrix_FromMatrix', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Path_Type', ctypes.py_object),
            ('Path_FromPath', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Pattern_Type', ctypes.py_object),
            ('SolidPattern_Type', ctypes.py_object),
            ('SurfacePattern_Type', ctypes.py_object),
            ('Gradient_Type', ctypes.py_object),
            ('LinearGradient_Type', ctypes.py_object),
            ('RadialGradient_Type', ctypes.py_object),
            ('Pattern_FromPattern', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('ScaledFont_Type', ctypes.py_object),
            ('ScaledFont_FromScaledFont', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Surface_Type', ctypes.py_object),
            ('ImageSurface_Type', ctypes.py_object),
            ('PDFSurface_Type', ctypes.py_object),
            ('PSSurface_Type', ctypes.py_object),
            ('SVGSurface_Type', ctypes.py_object),
            ('Win32Surface_Type', ctypes.py_object),
            ('XlibSurface_Type', ctypes.py_object),
            ('Surface_FromSurface', ctypes.PYFUNCTYPE(ctypes.py_object,
                                                      ctypes.c_void_p,
                                                      ctypes.py_object)),
            ('Check_Status', ctypes.PYFUNCTYPE(ctypes.c_int, ctypes.c_int))]

    # This structure is known good with pycairo 1.8.4.
    # We have to also test for (1,10,8) because pycairo 1.8.10 has an
    # incorrect version_info value
    elif cairo.version_info < (1,9) or cairo.version_info == (1,10,8):
        _fields_ = [
            ('Context_Type', ctypes.py_object),
            ('Context_FromContext', ctypes.PYFUNCTYPE(ctypes.py_object,
                                                      ctypes.c_void_p,
                                                      ctypes.py_object,
                                                      ctypes.py_object)),
            ('FontFace_Type', ctypes.py_object),
            ('ToyFontFace_Type', ctypes.py_object),  #** new in 1.8.4
            ('FontFace_FromFontFace', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('FontOptions_Type', ctypes.py_object),
            ('FontOptions_FromFontOptions', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Matrix_Type', ctypes.py_object),
            ('Matrix_FromMatrix', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Path_Type', ctypes.py_object),
            ('Path_FromPath', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Pattern_Type', ctypes.py_object),
            ('SolidPattern_Type', ctypes.py_object),
            ('SurfacePattern_Type', ctypes.py_object),
            ('Gradient_Type', ctypes.py_object),
            ('LinearGradient_Type', ctypes.py_object),
            ('RadialGradient_Type', ctypes.py_object),
            ('Pattern_FromPattern', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p,
                                                      ctypes.py_object)), #** changed in 1.8.4
            ('ScaledFont_Type', ctypes.py_object),
            ('ScaledFont_FromScaledFont', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Surface_Type', ctypes.py_object),
            ('ImageSurface_Type', ctypes.py_object),
            ('PDFSurface_Type', ctypes.py_object),
            ('PSSurface_Type', ctypes.py_object),
            ('SVGSurface_Type', ctypes.py_object),
            ('Win32Surface_Type', ctypes.py_object),
            ('XlibSurface_Type', ctypes.py_object),
            ('Surface_FromSurface', ctypes.PYFUNCTYPE(ctypes.py_object,
                                                      ctypes.c_void_p,
                                                      ctypes.py_object)),
            ('Check_Status', ctypes.PYFUNCTYPE(ctypes.c_int, ctypes.c_int))]

    # This structure is known good with pycairo 1.10.0. They keep adding stuff
    # to the middle of the structure instead of only adding to the end!
    elif cairo.version_info < (1,11):
        _fields_ = [
            ('Context_Type', ctypes.py_object),
            ('Context_FromContext', ctypes.PYFUNCTYPE(ctypes.py_object,
                                                      ctypes.c_void_p,
                                                      ctypes.py_object,
                                                      ctypes.py_object)),
            ('FontFace_Type', ctypes.py_object),
            ('ToyFontFace_Type', ctypes.py_object),
            ('FontFace_FromFontFace', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('FontOptions_Type', ctypes.py_object),
            ('FontOptions_FromFontOptions', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Matrix_Type', ctypes.py_object),
            ('Matrix_FromMatrix', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Path_Type', ctypes.py_object),
            ('Path_FromPath', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Pattern_Type', ctypes.py_object),
            ('SolidPattern_Type', ctypes.py_object),
            ('SurfacePattern_Type', ctypes.py_object),
            ('Gradient_Type', ctypes.py_object),
            ('LinearGradient_Type', ctypes.py_object),
            ('RadialGradient_Type', ctypes.py_object),
            ('Pattern_FromPattern', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p,
                                                      ctypes.py_object)), #** changed in 1.8.4
            ('ScaledFont_Type', ctypes.py_object),
            ('ScaledFont_FromScaledFont', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Surface_Type', ctypes.py_object),
            ('ImageSurface_Type', ctypes.py_object),
            ('PDFSurface_Type', ctypes.py_object),
            ('PSSurface_Type', ctypes.py_object),
            ('SVGSurface_Type', ctypes.py_object),
            ('Win32Surface_Type', ctypes.py_object),
            ('Win32PrintingSurface_Type', ctypes.py_object),  #** new
            ('XCBSurface_Type', ctypes.py_object),            #** new
            ('XlibSurface_Type', ctypes.py_object),
            ('Surface_FromSurface', ctypes.PYFUNCTYPE(ctypes.py_object,
                                                      ctypes.c_void_p,
                                                      ctypes.py_object)),
            ('Check_Status', ctypes.PYFUNCTYPE(ctypes.c_int, ctypes.c_int))]

    # This structure is known good with pycairo 1.11.1+.
    else:
        _fields_ = [
            ('Context_Type', ctypes.py_object),
            ('Context_FromContext', ctypes.PYFUNCTYPE(ctypes.py_object,
                                                      ctypes.c_void_p,
                                                      ctypes.py_object,
                                                      ctypes.py_object)),
            ('FontFace_Type', ctypes.py_object),
            ('ToyFontFace_Type', ctypes.py_object),
            ('FontFace_FromFontFace', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('FontOptions_Type', ctypes.py_object),
            ('FontOptions_FromFontOptions', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Matrix_Type', ctypes.py_object),
            ('Matrix_FromMatrix', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Path_Type', ctypes.py_object),
            ('Path_FromPath', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Pattern_Type', ctypes.py_object),
            ('SolidPattern_Type', ctypes.py_object),
            ('SurfacePattern_Type', ctypes.py_object),
            ('Gradient_Type', ctypes.py_object),
            ('LinearGradient_Type', ctypes.py_object),
            ('RadialGradient_Type', ctypes.py_object),
            ('Pattern_FromPattern', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p,
                                                      ctypes.py_object)), #** changed in 1.8.4
            ('ScaledFont_Type', ctypes.py_object),
            ('ScaledFont_FromScaledFont', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Surface_Type', ctypes.py_object),
            ('ImageSurface_Type', ctypes.py_object),
            ('PDFSurface_Type', ctypes.py_object),
            ('PSSurface_Type', ctypes.py_object),
            ('SVGSurface_Type', ctypes.py_object),
            ('Win32Surface_Type', ctypes.py_object),
            ('Win32PrintingSurface_Type', ctypes.py_object),  #** new
            ('XCBSurface_Type', ctypes.py_object),            #** new
            ('XlibSurface_Type', ctypes.py_object),
            ('Surface_FromSurface', ctypes.PYFUNCTYPE(ctypes.py_object,
                                                      ctypes.c_void_p,
                                                      ctypes.py_object)),
            ('Check_Status', ctypes.PYFUNCTYPE(ctypes.c_int, ctypes.c_int)),
            ('RectangleInt_Type', ctypes.py_object),
            ('RectangleInt_FromRectangleInt', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('Region_Type', ctypes.py_object),
            ('Region_FromRegion', ctypes.PYFUNCTYPE(ctypes.py_object, ctypes.c_void_p)),
            ('RecordingSurface_Type', ctypes.py_object)]


def _loadPycairoAPI():
    global pycairoAPI
    if pycairoAPI is not None:
        return

    if not hasattr(cairo, 'CAPI'):
        return

    if PY3:
        PyCapsule_GetPointer = ctypes.pythonapi.PyCapsule_GetPointer
        PyCapsule_GetPointer.argtypes = [ctypes.py_object, ctypes.c_char_p]
        PyCapsule_GetPointer.restype = ctypes.c_void_p
        ptr = PyCapsule_GetPointer(cairo.CAPI, b'cairo.CAPI')
    else:
        PyCObject_AsVoidPtr = ctypes.pythonapi.PyCObject_AsVoidPtr
        PyCObject_AsVoidPtr.argtypes = [ctypes.py_object]
        PyCObject_AsVoidPtr.restype = ctypes.c_void_p
        ptr = PyCObject_AsVoidPtr(cairo.CAPI)
    pycairoAPI = ctypes.cast(ptr, ctypes.POINTER(Pycairo_CAPI)).contents

#----------------------------------------------------------------------------

# Load these at import time.  That seems a bit better than doing it at
# first use...
_findCairoLib()
_loadPycairoAPI()

if 'wxMac' in wx.PlatformInfo:
    surface_create = cairoLib.cairo_quartz_surface_create_for_cg_context
    surface_create.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    surface_create.restype = ctypes.c_void_p

    cairo_create = cairoLib.cairo_create
    cairo_create.argtypes = [ctypes.c_void_p]
    cairo_create.restype = ctypes.c_void_p

    font_face_create = cairoLib.cairo_quartz_font_face_create_for_cgfont
    font_face_create.argtypes = [ctypes.c_void_p]
    font_face_create.restype = ctypes.c_void_p

elif 'wxMSW' in wx.PlatformInfo:
    cairoLib.cairo_win32_font_face_create_for_hfont.restype = ctypes.c_void_p

elif 'wxGTK' in wx.PlatformInfo:
    gdkLib = _findGDKLib()
    pcLib = _findPangoCairoLib()

    gdkLib.gdk_cairo_create.restype = ctypes.c_void_p
    pcLib.pango_cairo_font_map_get_default.restype = ctypes.c_void_p
    gdkLib.gdk_pango_context_get.restype = ctypes.c_void_p
    pcLib.pango_font_map_load_font.restype = ctypes.c_void_p
    pcLib.pango_cairo_font_get_scaled_font.restype = ctypes.c_void_p
    cairoLib.cairo_scaled_font_get_font_face.restype = ctypes.c_void_p

#----------------------------------------------------------------------------
