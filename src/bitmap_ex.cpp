//--------------------------------------------------------------------------
// Name:        src/bitmap_ex.h
// Purpose:     Helper functions and etc. for copying bitmap data to/from
//              buffer objects.  This file is included in etg/bitmap.py and
//              used in the wxBitmap wrapper.
//
// Author:      Robin Dunn
//
// Created:     27-Apr-2012
// Copyright:   (c) 2012-2020 by Total Control Software
// Licence:     wxWindows license
//--------------------------------------------------------------------------


#include <wx/rawbmp.h>

// TODO: Switch these APIs to use the new wxPyBuffer class

void wxPyCopyBitmapFromBuffer(wxBitmap* bmp,
                              buffer data, Py_ssize_t DATASIZE,
                              wxBitmapBufferFormat format, int stride)
{
    int height = bmp->GetHeight();
    int width = bmp->GetWidth();

    switch (format) {
        // A simple sequence of RGB bytes
        case wxBitmapBufferFormat_RGB:
        {
            if (DATASIZE < width * height * 3) {
                wxPyErr_SetString(PyExc_ValueError, "Invalid data buffer size.");
                return;
            }
            wxNativePixelData pixData(*bmp, wxPoint(0,0), wxSize(width, height));
            if (! pixData) {
                wxPyErr_SetString(PyExc_RuntimeError,
                                  "Failed to gain raw access to bitmap data.");
                return;
            }

            wxNativePixelData::Iterator p(pixData);
            for (int y=0; y<height; y++) {
                wxNativePixelData::Iterator rowStart = p;
                for (int x=0; x<width; x++) {
                    p.Red()   = *(data++);
                    p.Green() = *(data++);
                    p.Blue()  = *(data++);
                    ++p;
                }
                p = rowStart;
                p.OffsetY(pixData, 1);
            }
            break;
        }

        // A simple sequence of RGBA bytes
        case wxBitmapBufferFormat_RGBA:
        {
            if (DATASIZE < width * height * 4) {
                wxPyErr_SetString(PyExc_ValueError, "Invalid data buffer size.");
                return;
            }
            wxAlphaPixelData pixData(*bmp, wxPoint(0,0), wxSize(width, height));
            if (! pixData) {
                wxPyErr_SetString(PyExc_RuntimeError,
                                  "Failed to gain raw access to bitmap data.");
                return;
            }
            wxAlphaPixelData::Iterator p(pixData);
            for (int y=0; y<height; y++) {
                wxAlphaPixelData::Iterator rowStart = p;
                for (int x=0; x<width; x++) {
                    byte a = data[3];
                    p.Red()   = wxPy_premultiply(*(data++), a);
                    p.Green() = wxPy_premultiply(*(data++), a);
                    p.Blue()  = wxPy_premultiply(*(data++), a);
                    p.Alpha() = a; data++;
                    ++p;
                }
                p = rowStart;
                p.OffsetY(pixData, 1);
            }
            break;
        }

        // A sequence of 32-bit values in native endian order,
        // where the alpha is in the upper 8 bits, then red, then
        // green, then blue.  The stride is the distance in bytes
        // from the beginning of one row of the image data to the
        // beginning of the next row.  This may not be the same as
        // width*4 if alignment or platform specific optimizations
        // have been utilized.

        // NOTE: This is normally used with Cairo, which seems to
        // already have the values premultiplied.  Should we have
        // a way to optionally do it anyway?

        case wxBitmapBufferFormat_RGB32:
        case wxBitmapBufferFormat_ARGB32:
        {
            bool useAlpha = (format == wxBitmapBufferFormat_ARGB32);
            byte* rowStart = data;
            wxUint32* bufptr;
            wxUint32  value;

            if (stride == -1)
                stride = width * 4;

            if (DATASIZE < stride * height) {
                wxPyErr_SetString(PyExc_ValueError, "Invalid data buffer size.");
                return;
            }

            wxAlphaPixelData pixData(*bmp, wxPoint(0,0), wxSize(width,height));
            if (! pixData) {
                wxPyErr_SetString(PyExc_RuntimeError,
                                  "Failed to gain raw access to bitmap data.");
                return;
            }

            wxAlphaPixelData::Iterator pix(pixData);
            for (int y=0; y<height; y++) {
                pix.MoveTo(pixData, 0, y);
                bufptr = (wxUint32*)rowStart;
                for (int x=0; x<width; x++) {
                    value = *bufptr;
                    pix.Alpha() = useAlpha ? (value >> 24) & 0xFF : 255;
                    pix.Red()   = (value >> 16) & 0xFF;
                    pix.Green() = (value >>  8) & 0xFF;
                    pix.Blue()  = (value >>  0) & 0xFF;
                    ++pix;
                    ++bufptr;
                }
                rowStart += stride;
            }
            break;
        }
    }
}


// Some helper macros used below to help declutter the code
#define MAKE_PIXDATA(type) \
    type pixData(*bmp, wxPoint(0,0), wxSize(width, height)); \
    if (! pixData) { \
        wxPyErr_SetString(PyExc_RuntimeError, "Failed to gain raw access to bitmap data."); \
        return; \
    } \
    type::Iterator p(pixData); \
    type::Iterator rowStart

#define CHECK_BUFFERSIZE(size_needed) \
    if (DATASIZE < size_needed) { \
        wxPyErr_SetString(PyExc_ValueError, "Invalid data buffer size."); \
        return; \
    }


void wxPyCopyBitmapToBuffer(wxBitmap* bmp,
                            buffer data, Py_ssize_t DATASIZE,
                            wxBitmapBufferFormat format, int stride)
{
    int height = bmp->GetHeight();
    int width = bmp->GetWidth();
    int depth = bmp->GetDepth();

    // images loaded from a file may not have set the depth, at least on Mac...
    if (depth == -1) {
        if (bmp->HasAlpha())
            depth = 32;
        else
            depth = 24;
    }

    switch (format) {
        // A simple sequence of RGB bytes
        case wxBitmapBufferFormat_RGB:
        {
            CHECK_BUFFERSIZE(width * height * 3);
            if (depth == 24) {
                MAKE_PIXDATA(wxNativePixelData);

                for (int y=0; y<height; y++) {
                    rowStart = p;
                    for (int x=0; x<width; x++) {
                        *(data++) = p.Red();
                        *(data++) = p.Green();
                        *(data++) = p.Blue();
                        ++p;
                    }
                    p = rowStart;
                    p.OffsetY(pixData, 1);
                }
            }
            if (depth == 32) {
                // Source has alpha, but we won't be using it because the
                // destination buffer doesn't
                MAKE_PIXDATA(wxAlphaPixelData);

                for (int y=0; y<height; y++) {
                    rowStart = p;
                    for (int x=0; x<width; x++) {
                        *(data++) = p.Red();
                        *(data++) = p.Green();
                        *(data++) = p.Blue();
                        ++p;
                    }
                    p = rowStart;
                    p.OffsetY(pixData, 1);
                }
            }
            break;
        }

        // A simple sequence of RGBA bytes
        case wxBitmapBufferFormat_RGBA:
        {
            CHECK_BUFFERSIZE(width * height * 4);
            if (depth == 24) {
                MAKE_PIXDATA(wxNativePixelData);
                for (int y=0; y<height; y++) {
                    rowStart = p;
                    for (int x=0; x<width; x++) {
                        byte a = wxALPHA_OPAQUE;
                        *(data++) = wxPy_unpremultiply(p.Red(), a);
                        *(data++) = wxPy_unpremultiply(p.Green(), a);
                        *(data++) = wxPy_unpremultiply(p.Blue(), a);
                        *(data++) = a;
                        ++p;
                    }
                    p = rowStart;
                    p.OffsetY(pixData, 1);
                }
            }
            if (depth == 32) {
                MAKE_PIXDATA(wxAlphaPixelData);
                for (int y=0; y<height; y++) {
                    rowStart = p;
                    for (int x=0; x<width; x++) {
                        byte a = p.Alpha();
                        *(data++) = wxPy_unpremultiply(p.Red(), a);
                        *(data++) = wxPy_unpremultiply(p.Green(), a);
                        *(data++) = wxPy_unpremultiply(p.Blue(), a);
                        *(data++) = a;
                        ++p;
                    }
                    p = rowStart;
                    p.OffsetY(pixData, 1);
                }
            }
            break;
        }

        // A sequence of 32-bit values in native endian order,
        // where the alpha is in the upper 8 bits, then red, then
        // green, then blue.  The stride is the distance in bytes
        // from the beginning of one row of the image data to the
        // beginning of the next row.  This may not be the same as
        // width*4 if alignment or platform specific optimizations
        // have been utilized.

        // NOTE: This is normally used with Cairo, which seems to
        // already have the values premultiplied.  Should we have
        // a way to optionally do it anyway?

        case wxBitmapBufferFormat_RGB32:
        case wxBitmapBufferFormat_ARGB32:
        {
            bool useAlpha = (format == wxBitmapBufferFormat_ARGB32);
            byte* dataRow = data;
            wxUint32* bufptr;
            wxUint32  value;

            if (stride == -1)
                stride = width * 4;

            CHECK_BUFFERSIZE(stride * height);

            if (useAlpha && depth == 32) {
                MAKE_PIXDATA(wxAlphaPixelData);
                for (int y=0; y<height; y++) {
                    p.MoveTo(pixData, 0, y);
                    bufptr = (wxUint32*)dataRow;
                    for (int x=0; x<width; x++) {
                        value =
                            (p.Alpha() << 24) |
                            (p.Red() << 16) |
                            (p.Green() << 8) |
                            (p.Blue());
                        *bufptr = value;
                        ++p;
                        ++bufptr;
                    }
                    dataRow += stride;
                }
            }
            else // if (!useAlpha /*depth == 24*/)
            {
                MAKE_PIXDATA(wxNativePixelData);
                for (int y=0; y<height; y++) {
                    p.MoveTo(pixData, 0, y);
                    bufptr = (wxUint32*)dataRow;
                    for (int x=0; x<width; x++) {
                        value =
                            (wxALPHA_OPAQUE << 24) |
                            (p.Red() << 16) |
                            (p.Green() << 8) |
                            (p.Blue());
                        *bufptr = value;
                        ++p;
                        ++bufptr;
                    }
                    dataRow += stride;
                }
            }
            break;
        }
    }
}

//--------------------------------------------------------------------------
