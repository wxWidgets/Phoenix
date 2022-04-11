//--------------------------------------------------------------------------
// Name:        src/bitmap_ex.h
// Purpose:     Helper functions and etc. for copying bitmap data to/from
//              buffer objects.
//
// Author:      Robin Dunn
//
// Created:     27-Apr-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


#ifndef BITMAP_EX_H
#define BITMAP_EX_H


enum wxBitmapBufferFormat {
    wxBitmapBufferFormat_RGB,
    wxBitmapBufferFormat_RGBA,
    wxBitmapBufferFormat_RGB32,
    wxBitmapBufferFormat_ARGB32,
};


// See http://tinyurl.com/e5adr for what premultiplying alpha means. wxMSW and
// wxMac want to have the values premultiplied by the alpha value, but the
// other platforms don't.  These macros help keep the code clean.
#if defined(__WXMSW__) || defined(__WXMAC__)
#define wxPy_premultiply(p, a)   ((p) * (a) / 0xff)
#define wxPy_unpremultiply(p, a) ((a) ? ((p) * 0xff / (a)) : (p))
#else
#define wxPy_premultiply(p, a)   (p)
#define wxPy_unpremultiply(p, a) (p)
#endif


void wxPyCopyBitmapFromBuffer(wxBitmap* bmp,
                              buffer data, Py_ssize_t DATASIZE,
                              wxBitmapBufferFormat format, int stride=-1);

void wxPyCopyBitmapToBuffer(wxBitmap* bmp,
                            buffer data, Py_ssize_t DATASIZE,
                            wxBitmapBufferFormat format, int stride=-1);

#endif
