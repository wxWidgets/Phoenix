#----------------------------------------------------------------------
# Name:        wx_cairocffi
# Purpose:     wx.lib.wxcairo implementation functions for cairocffi
#
# Author:      Robin Dunn
#
# Created:     19-July-2016
# Copyright:   (c) 2016 by Total Control Software
# Licence:     wxWindows license
#
# Tags:        phoenix-port, py3-port
#----------------------------------------------------------------------

"""
wx.lib.wxcairo implementation functions using cairocffi.
"""

import wx

import cairocffi
from cairocffi import cairo as cairo_c
from cairocffi import ffi

# Make it so subsequent `import cairo` statements still work as if it
# was really PyCairo
cairocffi.install_as_pycairo()


#----------------------------------------------------------------------------

# a convenience function, just to save a bit of typing below
def voidp(ptr):
    """Convert a SIP void* type to a ffi cdata"""
    return ffi.cast('void *', int(ptr))

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

