# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Name:        etg/bitmap.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     25-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

from textwrap import dedent

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "bitmap"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxBitmap',
           'wxBitmapHandler',
           'wxMask' ]

OTHERDEPS = [ 'src/bitmap_ex.h',
              'src/bitmap_ex.cpp', ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxMask')
    c.mustHaveApp()
    for m in c.find('Create').all():
        m.ignore()

    c = module.find('wxBitmap')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    tools.removeVirtuals(c)

    # TODO: The wxCursor version of the ctor is not implemented on OSX...
    c.find('wxBitmap').findOverload('wxCursor').ignore()

    c.find('wxBitmap.bits').type = 'const char*'
    c.find('wxBitmap.type').default = 'wxBITMAP_TYPE_ANY'
    c.find('LoadFile.type').default = 'wxBITMAP_TYPE_ANY'

    c.find('wxBitmap').findOverload('(const char *const *bits)').ignore()

    c.addCppCtor('(PyObject* listOfBytes)',
        doc="Construct a Bitmap from a list of strings formatted as XPM data.",
        body="""\
            wxPyThreadBlocker blocker;
            char**    cArray = NULL;
            int       count;
            char      errMsg[] = "Expected a list of bytes objects.";

            if (!PyList_Check(listOfBytes)) {
                PyErr_SetString(PyExc_TypeError, errMsg);
                return NULL;
            }
            count = PyList_Size(listOfBytes);
            cArray = new char*[count];

            for(int x=0; x<count; x++) {
                PyObject* item = PyList_GET_ITEM(listOfBytes, x);
                if (!PyBytes_Check(item)) {
                    PyErr_SetString(PyExc_TypeError, errMsg);
                    delete [] cArray;
                    return NULL;
                }
                cArray[x] = PyBytes_AsString(item);
            }
            wxBitmap* bmp = new wxBitmap(cArray);
            delete [] cArray;
            return bmp;
            """)


    c.find('SetMask.mask').transfer = True

    # TODO: This is different than the docs, but only on MSW... Remove this
    # if/when that gets fixed.
    c.find('UseAlpha').type = 'void'

    c.addCppMethod('void', 'SetMaskColour', '(const wxColour& colour)',
        doc="Create a mask for this bitmap based on the pixels with the given colour.",
        body="""\
        wxMask* mask = new wxMask(*self, *colour);
        self->SetMask(mask);
        """)

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addCppMethod('long', 'GetHandle', '()',
        doc='MSW-only method to fetch the windows handle for the bitmap.',
        body="""\
            #ifdef __WXMSW__
                return HandleToLong(self->GetHandle());
            #else
                return 0;
            #endif
            """)

    c.addCppMethod('void', 'SetHandle', '(long handle)',
        doc='MSW-only method to set the windows handle for the bitmap.',
        body="""\
            #ifdef __WXMSW__
                self->SetHandle((WXHANDLE)LongToHandle(handle));
            #endif
            """)

    c.addCppMethod('void', 'SetSize', '(const wxSize& size)',
        doc='Set the bitmap size (does not alter the existing native bitmap data or image size).',
        body="""\
            self->SetWidth(size->x);
            self->SetHeight(size->y);
            """)



    # On MSW the bitmap handler classes are different than what is
    # documented, and this causes compile errors. Nobody has needed them from
    # Python thus far, so just ignore them all for now.
    for m in c.find('FindHandler').all():
        m.ignore()
    c.find('AddHandler').ignore()
    c.find('CleanUpHandlers').ignore()
    c.find('GetHandlers').ignore()
    c.find('InsertHandler').ignore()
    c.find('RemoveHandler').ignore()

    # This one is called from the wx startup code, it's not needed in Python
    # so nuke it too since we're nuking all the others.
    c.find('InitStandardHandlers').ignore()

    module.find('wxBitmapHandler').ignore()
    #module.addItem(tools.wxListWrapperTemplate('wxList', 'wxBitmapHandler', module))


    #-----------------------------------------------------------------------
    # Declarations, helpers and methods for converting to/from buffer objects
    # with raw bitmap access.

    from etgtools import EnumDef, EnumValueDef
    e = EnumDef(name='wxBitmapBufferFormat')
    e.items.extend([ EnumValueDef(name='wxBitmapBufferFormat_RGB'),
                     EnumValueDef(name='wxBitmapBufferFormat_RGBA'),
                     EnumValueDef(name='wxBitmapBufferFormat_RGB32'),
                     EnumValueDef(name='wxBitmapBufferFormat_ARGB32'),
                     ])
    module.insertItem(0, e)

    c.includeCppCode('src/bitmap_ex.cpp')
    module.addHeaderCode('#include "bitmap_ex.h"')


    c.addCppMethod('void', 'CopyFromBuffer',
        '(wxPyBuffer* data, wxBitmapBufferFormat format=wxBitmapBufferFormat_RGB, int stride=-1)',
        doc=dedent("""\
            Copy data from a buffer object to replace the bitmap pixel data.
            Default format is plain RGB, but other formats are now supported as
            well.  The following symbols are used to specify the format of the
            bytes in the buffer:

                =============================  ================================
                wx.BitmapBufferFormat_RGB      A simple sequence of RGB bytes
                wx.BitmapBufferFormat_RGBA     A simple sequence of RGBA bytes
                wx.BitmapBufferFormat_ARGB32   A sequence of 32-bit values in native endian order, with alpha in the upper 8 bits, followed by red, green, and blue.
                wx.BitmapBufferFormat_RGB32    Same as above but the alpha byte is ignored.
                =============================  ================================"""),
        body="""\
            wxPyCopyBitmapFromBuffer(self, (byte*)data->m_ptr, data->m_len, format, stride);
        """)


    c.addCppMethod('void', 'CopyToBuffer',
        '(wxPyBuffer* data, wxBitmapBufferFormat format=wxBitmapBufferFormat_RGB, int stride=-1)',
        doc=dedent("""\
            Copy pixel data to a buffer object.  See :meth:`CopyFromBuffer` for buffer
            format details."""),
        body="""\
            wxPyCopyBitmapToBuffer(self, (byte*)data->m_ptr, data->m_len, format, stride);
            """)


    # Some bitmap factories added as static methods

    c.addCppMethod('wxBitmap*', 'FromBufferAndAlpha',
        '(int width, int height, wxPyBuffer* data, wxPyBuffer* alpha)',
        isStatic=True,
        factory=True,
        doc=dedent("""\
            Creates a :class:`wx.Bitmap` from in-memory data.  The data and alpha
            parameters must be a Python object that implements the buffer
            interface, such as a string, bytearray, etc.  The data object
            is expected to contain a series of RGB bytes and be at least
            ``(width * height * 3)`` bytes long, while the alpha object is expected
            to be ``(width * height)`` bytes long and represents the image's alpha
            channel.  On Windows and Mac the RGB values will be
            'premultiplied' by the alpha values.  (The other platforms do
            the multiplication themselves.)

            Unlike :func:`wx.ImageFromBuffer` the bitmap created with this function
            does not share the memory block with the buffer object.  This is
            because the native pixel buffer format varies on different
            platforms, and so instead an efficient as possible copy of the
            data is made from the buffer object to the bitmap's native pixel
            buffer.
            """),
        body="""\
            if (!data->checkSize(width*height*3) || !alpha->checkSize(width*height))
                return NULL;

            byte* ddata = (byte*)data->m_ptr;
            byte* adata = (byte*)alpha->m_ptr;
            wxBitmap* bmp = new wxBitmap(width, height, 32);

            wxAlphaPixelData pixData(*bmp, wxPoint(0,0), wxSize(width,height));
            if (! pixData) {
                wxPyErr_SetString(PyExc_RuntimeError, "Failed to gain raw access to bitmap data.");
                return NULL;
            }

            wxAlphaPixelData::Iterator p(pixData);
            for (int y=0; y<height; y++) {
                wxAlphaPixelData::Iterator rowStart = p;
                for (int x=0; x<width; x++) {
                    byte a = *(adata++);
                    p.Red()   = wxPy_premultiply(*(ddata++), a);
                    p.Green() = wxPy_premultiply(*(ddata++), a);
                    p.Blue()  = wxPy_premultiply(*(ddata++), a);
                    p.Alpha() = a;
                    ++p;
                }
                p = rowStart;
                p.OffsetY(pixData, 1);
            }
            return bmp;
            """)

    c.addCppMethod('wxBitmap*', 'FromBuffer', '(int width, int height, wxPyBuffer* data)',
        isStatic=True,
        factory=True,
        doc=dedent("""\
            Creates a :class:`wx.Bitmap` from in-memory data.  The data parameter
            must be a Python object that implements the buffer interface, such
            as a string, bytearray, etc.  The data object is expected to contain
            a series of RGB bytes and be at least ``(width * height * 3)`` bytes long.

            Unlike :func:`wx.ImageFromBuffer` the bitmap created with this function
            does not share the memory block with the buffer object.  This is
            because the native pixel buffer format varies on different
            platforms, and so instead an efficient as possible copy of the
            data is made from the buffer object to the bitmap's native pixel
            buffer.
            """),
        body="""\
            wxBitmap* bmp = new wxBitmap(width, height, 24);
            wxPyCopyBitmapFromBuffer(bmp, (byte*)data->m_ptr, data->m_len, wxBitmapBufferFormat_RGB);
            wxPyThreadBlocker blocker;
            if (PyErr_Occurred()) {
                delete bmp;
                bmp = NULL;
            }
            return bmp;
            """)

    module.addPyFunction('BitmapFromBuffer', '(width, height, dataBuffer, alphaBuffer=None)',
        deprecated="Use :meth:`wx.Bitmap.FromBuffer` or :meth:`wx.Bitmap.FromBufferAndAlpha` instead.",
        doc='A compatibility wrapper for :meth:`wx.Bitmap.FromBuffer` and :meth:`wx.Bitmap.FromBufferAndAlpha`',
        body="""\
            if alphaBuffer is not None:
                return Bitmap.FromBufferAndAlpha(width, height, dataBuffer, alphaBuffer)
            else:
                return Bitmap.FromBuffer(width, height, dataBuffer)
            """)




    c.addCppMethod('wxBitmap*', 'FromBufferRGBA', '(int width, int height, wxPyBuffer* data)',
        isStatic=True,
        factory=True,
        doc=dedent("""\
            Creates a :class:`wx.Bitmap` from in-memory data.  The data parameter
            must be a Python object that implements the buffer interface, such
            as a string, bytearray, etc.  The data object is expected to contain
            a series of RGBA bytes and be at least ``(width * height * 4)`` bytes long.
            On Windows and Mac the RGB values will be 'premultiplied' by the
            alpha values.  (The other platforms do the multiplication themselves.)

            Unlike :func:`wx.ImageFromBuffer` the bitmap created with this function
            does not share the memory block with the buffer object.  This is
            because the native pixel buffer format varies on different
            platforms, and so instead an efficient as possible copy of the
            data is made from the buffer object to the bitmap's native pixel
            buffer.
            """),
        body="""\
            wxBitmap* bmp = new wxBitmap(width, height, 32);
            wxPyCopyBitmapFromBuffer(bmp, (byte*)data->m_ptr, data->m_len, wxBitmapBufferFormat_RGBA);
            wxPyThreadBlocker blocker;
            if (PyErr_Occurred()) {
                delete bmp;
                bmp = NULL;
            }
            return bmp;
            """)

    module.addPyFunction('BitmapFromBufferRGBA', '(width, height, dataBuffer)',
        deprecated="Use :meth:`wx.Bitmap.FromBufferRGBA` instead.",
        doc='A compatibility wrapper for :meth:`wx.Bitmap.FromBufferRGBA`',
        body='return Bitmap.FromBufferRGBA(width, height, dataBuffer)')


    c.addCppMethod('wxBitmap*', 'FromRGBA',
        '(int width, int height, byte red=0, byte green=0, byte blue=0, byte alpha=0)',
        isStatic=True,
        factory=True,
        doc=dedent("""\
            Creates a new empty 32-bit :class:`wx.Bitmap` where every pixel has been
            initialized with the given RGBA values.
            """),
        body="""\
            if ( !(width > 0 && height > 0) ) {
                wxPyErr_SetString(PyExc_ValueError, "Width and height must be greater than zero");
                return NULL;
            }

            wxBitmap* bmp = new wxBitmap(width, height, 32);
            wxAlphaPixelData pixData(*bmp, wxPoint(0,0), wxSize(width,height));
            if (! pixData) {
                wxPyErr_SetString(PyExc_RuntimeError, "Failed to gain raw access to bitmap data.");
                return NULL;
            }

            wxAlphaPixelData::Iterator p(pixData);
            for (int y=0; y<height; y++) {
                wxAlphaPixelData::Iterator rowStart = p;
                for (int x=0; x<width; x++) {
                    p.Red()   = wxPy_premultiply(red, alpha);
                    p.Green() = wxPy_premultiply(green, alpha);
                    p.Blue()  = wxPy_premultiply(blue, alpha);
                    p.Alpha() = alpha;
                    ++p;
                }
                p = rowStart;
                p.OffsetY(pixData, 1);
            }
            return bmp;
            """)


    c.find('NewFromPNGData').detailedDoc = [dedent("""\
        This helper function provides the simplest way to create a wx.Bitmap from
        in-memory PNG image data.
        """)]

    c.addCppMethod('wxBitmap*', 'FromPNGData', '(wxPyBuffer* data)',
        isStatic=True,
        factory=True,
        doc=dedent("""\
            Like :meth:`NewFromPNGData`, but with a simpler API accepting a Python
            buffer-compatible object.
            """),
        body="""\
            wxBitmap bmp = wxBitmap::NewFromPNGData(data->m_ptr, data->m_len);
            return new wxBitmap(bmp);
            """ )

    module.addPyFunction('EmptyBitmapRGBA', '(width, height, red=0, green=0, blue=0, alpha=0)',
        deprecated="Use :meth:`wx.Bitmap.FromRGBA` instead.",
        doc='A compatibility wrapper for :meth:`wx.Bitmap.FromRGBA`',
        body='return Bitmap.FromRGBA(width, height, red, green, blue, alpha)')

    #-----------------------------------------------------------------------

    # For compatibility:
    module.addPyFunction('EmptyBitmap', '(width, height, depth=BITMAP_SCREEN_DEPTH)',
                         deprecated="Use :class:`wx.Bitmap` instead",
                         doc='A compatibility wrapper for the wx.Bitmap(width, height, depth) constructor',
                         body='return Bitmap(width, height, depth)')

    module.addPyFunction('BitmapFromImage', '(image)',
                         deprecated="Use :class:`wx.Bitmap` instead",
                         doc='A compatibility wrapper for the wx.Bitmap(wx.Image) constructor',
                         body='return Bitmap(image)')

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

