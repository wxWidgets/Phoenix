#----------------------------------------------------------------------
# Name:        wx_cairocffi
# Purpose:     wx.lib.wxcairo implementation functions for cairocffi
#
# Author:      Robin Dunn
#
# Created:     19-July-2016
# Copyright:   (c) 2016-2017 by Total Control Software
# Licence:     wxWindows license
#
# Tags:        phoenix-port, py3-port
#----------------------------------------------------------------------

"""
wx.lib.wxcairo implementation functions using cairocffi.
"""

import os
import os.path as op
import wx

# On Windows try to get cairocffi to import the Cairo DLLs included with
# wxPython instead of the first ones found on the system's PATH. Otherwise, if
# CAIRO is set in the environment then use that one instead.  This hack is
# accomplished by temporarily altering the PATH and then restoring it after
# cairocffi has initialized.
if os.name == 'nt':
    _save_path = os.environ.get('PATH')
    _cairo_path = os.environ.get('CAIRO')
    if not _cairo_path:
        _cairo_path = op.abspath(op.dirname(wx.__file__))
        os.environ['PATH'] = _cairo_path + os.pathsep + _save_path

import cairocffi
from cairocffi import cairo as cairo_c
from cairocffi import ffi

# Make it so subsequent `import cairo` statements still work as if it
# was really PyCairo
cairocffi.install_as_pycairo()

# Now restore the original PATH
if os.name == 'nt':
    os.environ['PATH'] = _save_path


#----------------------------------------------------------------------------

# convenience functions, just to save a bit of typing below
def voidp(ptr):
    """Convert a SIP void* type to a ffi cdata"""
    if isinstance(ptr, ffi.CData):
        return ptr
    return ffi.cast('void *', int(ptr))

def ct_voidp(ptr):
    """Convert a SIP void* type to a ctypes c_void_p"""
    import ctypes
    return ctypes.c_void_p(int(ptr))

#----------------------------------------------------------------------------

def _ContextFromDC(dc):
    if not isinstance(dc, wx.WindowDC) and not isinstance(dc, wx.MemoryDC):
        raise TypeError("Only window and memory DC's are supported at this time.")

    if 'wxMac' in wx.PlatformInfo:
        width, height = dc.GetSize()

        # use the CGContextRef of the DC to make the cairo surface
        cgc = dc.GetHandle()
        assert cgc is not None and int(cgc) != 0, "Unable to get CGContext from DC."
        ptr = voidp(cgc)
        surfaceptr = cairo_c.cairo_quartz_surface_create_for_cg_context(
            ptr, width, height)
        surface = cairocffi.Surface._from_pointer(surfaceptr, False)

        # Now create a cairo context for that surface
        ctx = cairocffi.Context(surface)

    elif 'wxMSW' in wx.PlatformInfo:
        # Similarly, get the HDC and create a surface from it
        hdc = voidp(dc.GetHandle())
        surfaceptr = cairo_c.cairo_win32_surface_create(hdc)
        surface = cairocffi.Surface._from_pointer(surfaceptr, False)

        # Now create a cairo context for that surface
        ctx = cairocffi.Context(surface)

    elif 'wxGTK' in wx.PlatformInfo:
        if 'gtk3' in wx.PlatformInfo:
            # With wxGTK3, GetHandle() returns a cairo context directly
            ctxptr = voidp( dc.GetHandle() )
            ctx = cairocffi.Context._from_pointer(ctxptr, True)

        else:
            # Get the GdkDrawable from the dc
            drawable = ct_voidp( dc.GetHandle() )

            # Call a GDK API to create a cairo context
            ctxptr = gdkLib.gdk_cairo_create(drawable)

            # Turn it into a Cairo context object
            ctx = cairocffi.Context._from_pointer(voidp(ctxptr), False)

    else:
        raise NotImplementedError("Help  me, I'm lost...")

    return ctx


#----------------------------------------------------------------------------

def _FontFaceFromFont(font):
    if 'wxMac' in wx.PlatformInfo:
        cgFont = voidp(font.OSXGetCGFont())
        fontfaceptr = cairo_c.cairo_quartz_font_face_create_for_cgfont(cgFont)
        fontface = cairocffi.FontFace._from_pointer(fontfaceptr, False)

    elif 'wxMSW' in wx.PlatformInfo:
        hfont = voidp(font.GetHFONT())
        fontfaceptr = cairo_c.cairo_win32_font_face_create_for_hfont(hfont)
        fontface = cairocffi.FontFace._from_pointer(fontfaceptr, False)

    elif 'wxGTK' in wx.PlatformInfo:
        # wow, this is a hell of a lot of steps...
        desc = ct_voidp( font.GetPangoFontDescription() )

        pcfm = ct_voidp(pcLib.pango_cairo_font_map_get_default())

        pctx = ct_voidp(gdkLib.gdk_pango_context_get())

        pfnt = ct_voidp( pcLib.pango_font_map_load_font(pcfm, pctx, desc) )

        scaledfontptr = ct_voidp( pcLib.pango_cairo_font_get_scaled_font(pfnt) )

        fontfaceptr = cairo_c.cairo_scaled_font_get_font_face(voidp(scaledfontptr.value))
        fontface = cairocffi.FontFace._from_pointer(fontfaceptr, True)

        gdkLib.g_object_unref(pctx)

    else:
        raise NotImplementedError("Help  me, I'm lost...")

    return fontface


#----------------------------------------------------------------------------
# GTK platforms we need to load some other shared libraries to help us get
# from wx objects to cairo objects.  This is using ctypes mainly because it
# was already working this way in wx_pycairo.py and so it required fewer brain
# cells to be sacrificed to port it to this module.
#
# TODO: consider moving this code to use cffi instead, for consistency.

if 'wxGTK' in wx.PlatformInfo:
    import ctypes
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


    gdkLib = _findGDKLib()
    pcLib = _findPangoCairoLib()

    gdkLib.gdk_cairo_create.restype = ctypes.c_void_p
    gdkLib.gdk_pango_context_get.restype = ctypes.c_void_p

    pcLib.pango_cairo_font_map_get_default.restype = ctypes.c_void_p
    pcLib.pango_font_map_load_font.restype = ctypes.c_void_p
    pcLib.pango_cairo_font_get_scaled_font.restype = ctypes.c_void_p


#----------------------------------------------------------------------------
