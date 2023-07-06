#---------------------------------------------------------------------------
# Name:        etg/image.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     25-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from buildtools.backports.textwrap3 import dedent

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "image"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxImage',
           'wxImageHistogram',
           'wxImageHandler',
           'wxTIFFHandler',
           'wxGIFHandler',
           "wxIFFHandler",
           "wxJPEGHandler",
           "wxPCXHandler",
           "wxPNGHandler",
           "wxPNMHandler",
           "wxTGAHandler",
           "wxXPMHandler"
           #'wxQuantize',
           #'wxPalette',
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxImage')
    assert isinstance(c, etgtools.ClassDef)
    c.find('wxImage').findOverload('(const char *const *xpmData)').ignore()

    c.find('GetHandlers').ignore()  # TODO

    c.find('wxImage').findOverload('wxBitmap').mustHaveApp()


    # Ignore the ctors taking raw data buffers, so we can add in our own
    # versions that are a little smarter (accept any buffer object, check
    # the data length, etc.)
    c.find('wxImage').findOverload('int width, int height, unsigned char *data, bool static_data').ignore()
    c.find('wxImage').findOverload('const wxSize &sz, unsigned char *data, bool static_data').ignore()
    c.find('wxImage').findOverload('int width, int height, unsigned char *data, unsigned char *alpha, bool static_data').ignore()
    c.find('wxImage').findOverload('const wxSize &sz, unsigned char *data, unsigned char *alpha, bool static_data').ignore()


    c.addCppCtor_sip('(int width, int height, wxPyBuffer* data)',
        doc="Creates an image from RGB data in memory.",
        body="""\
            if (! data->checkSize(width*height*3))
                return NULL;
            void* copy = data->copy();
            if (! copy)
                return NULL;
            sipCpp = new sipwxImage;
            sipCpp->Create(width, height, (byte*)copy);
            """)

    c.addCppCtor_sip('(int width, int height, wxPyBuffer* data, wxPyBuffer* alpha)',
        doc="Creates an image from RGB data in memory, plus an alpha channel",
        body="""\
            void* dcopy; void* acopy;
            if (!data->checkSize(width*height*3) || !alpha->checkSize(width*height))
                return NULL;
            if ((dcopy = data->copy()) == NULL || (acopy = alpha->copy()) == NULL)
                return NULL;
            sipCpp = new sipwxImage;
            sipCpp->Create(width, height, (byte*)dcopy, (byte*)acopy, false);
            """)

    c.addCppCtor_sip('(const wxSize& size, wxPyBuffer* data)',
        doc="Creates an image from RGB data in memory.",
        body="""\
            if (! data->checkSize(size->x*size->y*3))
                return NULL;
            void* copy = data->copy();
            if (! copy)
                return NULL;
            sipCpp = new sipwxImage;
            sipCpp->Create(size->x, size->y, (byte*)copy, false);
            """)

    c.addCppCtor_sip('(const wxSize& size, wxPyBuffer* data, wxPyBuffer* alpha)',
        doc="Creates an image from RGB data in memory, plus an alpha channel",
        body="""\
            void* dcopy; void* acopy;
            if (!data->checkSize(size->x*size->y*3) || !alpha->checkSize(size->x*size->y))
                return NULL;
            if ((dcopy = data->copy()) == NULL || (acopy = alpha->copy()) == NULL)
                return NULL;
            sipCpp = new sipwxImage;
            sipCpp->Create(size->x, size->y, (byte*)dcopy, (byte*)acopy, false);
            """)


    # Do the same for the Create method overloads that need to deal with data buffers
    c.find('Create').findOverload('int width, int height, unsigned char *data, bool static_data').ignore()
    c.find('Create').findOverload('const wxSize &sz, unsigned char *data, bool static_data').ignore()
    c.find('Create').findOverload('int width, int height, unsigned char *data, unsigned char *alpha, bool static_data').ignore()
    c.find('Create').findOverload('const wxSize &sz, unsigned char *data, unsigned char *alpha, bool static_data').ignore()

    c.addCppMethod('bool', 'Create', '(int width, int height, wxPyBuffer* data)',
        doc="Create a new image initialized with the given RGB data.",
        body="""\
            if (! data->checkSize(width*height*3))
                return false;
            void* copy = data->copy();
            if (! copy)
                return false;
            return self->Create(width, height, (byte*)copy);
            """)

    c.addCppMethod('bool', 'Create', '(int width, int height, wxPyBuffer* data, wxPyBuffer* alpha)',
        doc="Create a new image initialized with the given RGB data and Alpha data.",
        body="""\
            void* dcopy; void* acopy;
            if (!data->checkSize(width*height*3) || !alpha->checkSize(width*height))
                return false;
            if ((dcopy = data->copy()) == NULL || (acopy = alpha->copy()) == NULL)
                return false;
            return self->Create(width, height, (byte*)dcopy, (byte*)acopy);
            """)

    c.addCppMethod('bool', 'Create', '(const wxSize& size, wxPyBuffer* data)',
        doc="Create a new image initialized with the given RGB data.",
        body="""\
            if (! data->checkSize(size->x*size->y*3))
                return false;
            void* copy = data->copy();
            if (! copy)
                return false;
            return self->Create(size->x, size->y, (byte*)copy);
            """)

    c.addCppMethod('bool', 'Create', '(const wxSize& size, wxPyBuffer* data, wxPyBuffer* alpha)',
        doc="Create a new image initialized with the given RGB data and Alpha data.",
        body="""\
            void* dcopy; void* acopy;
            if (!data->checkSize(size->x*size->y*3) || !alpha->checkSize(size->x*size->y))
                return false;
            if ((dcopy = data->copy()) == NULL || (acopy = alpha->copy()) == NULL)
                return false;
            return self->Create(size->x, size->y, (byte*)dcopy, (byte*)acopy);
            """)


    # And also do similar for SetData and SetAlpha
    m = c.find('SetData').findOverload('unsigned char *data')
    bd, dd = m.briefDoc, m.detailedDoc
    m.ignore()
    c.addCppMethod('void', 'SetData', '(wxPyBuffer* data)',
        briefDoc=bd, detailedDoc=dd,
        body="""\
        if (!data->checkSize(self->GetWidth()*self->GetHeight()*3))
            return;
        void* copy = data->copy();
        if (!copy)
            return;
        self->SetData((byte*)copy, false);
        """)

    c.find('SetData').findOverload('int new_width').ignore()
    c.addCppMethod('void', 'SetData', '(wxPyBuffer* data, int new_width, int new_height)',
        body="""\
        if (!data->checkSize(new_width*new_height*3))
            return;
        void* copy = data->copy();
        if (!copy)
            return;
        self->SetData((byte*)copy, new_width, new_height, false);
        """)

    m = c.find('SetAlpha').findOverload('unsigned char *alpha')
    bd, dd = m.briefDoc, m.detailedDoc
    m.ignore()
    c.addCppMethod('void', 'SetAlpha', '(wxPyBuffer* alpha)',
        briefDoc=bd, detailedDoc=dd,
        body="""\
        if (!alpha->checkSize(self->GetWidth()*self->GetHeight()))
            return;
        void* copy = alpha->copy();
        if (!copy)
            return;
        self->SetAlpha((byte*)copy, false);
        """)


    # GetData() and GetAlpha() return a copy of the image data/alpha bytes as
    # a bytearray object.
    c.find('GetData').ignore()
    c.addCppMethod('PyObject*', 'GetData', '()',
        doc="Returns a copy of the RGB bytes of the image.",
        body="""\
            byte* data = self->GetData();
            Py_ssize_t len = self->GetWidth() * self->GetHeight() * 3;
            PyObject* rv = NULL;
            wxPyBLOCK_THREADS( rv = PyByteArray_FromStringAndSize((const char*)data, len));
            return rv;
            """)

    c.find('GetAlpha').findOverload('()').ignore()
    c.addCppMethod('PyObject*', 'GetAlpha', '()',
        doc="Returns a copy of the Alpha bytes of the image.",
        body="""\
            byte* data = self->GetAlpha();
            Py_ssize_t len = self->GetWidth() * self->GetHeight();
            PyObject* rv = NULL;
            wxPyBLOCK_THREADS( rv = PyByteArray_FromStringAndSize((const char*)data, len));
            return rv;
            """)


    # GetDataBuffer, GetAlphaBuffer provide direct access to the image's
    # internal buffers as a writable buffer object.  We'll use memoryview
    # objects.
    c.addCppMethod('PyObject*', 'GetDataBuffer', '()',
        doc="""\
        Returns a writable Python buffer object that is pointing at the RGB
        image data buffer inside the :class:`Image`. You need to ensure that you do
        not use this buffer object after the image has been destroyed.""",
        body="""\
            byte* data = self->GetData();
            Py_ssize_t len = self->GetWidth() * self->GetHeight() * 3;
            PyObject* rv;
            wxPyThreadBlocker blocker;
            rv = wxPyMakeBuffer(data, len);
            return rv;
            """)

    c.addCppMethod('PyObject*', 'GetAlphaBuffer', '()',
        doc="""\
        Returns a writable Python buffer object that is pointing at the Alpha
        data buffer inside the :class:`Image`. You need to ensure that you do
        not use this buffer object after the image has been destroyed.""",
        body="""\
            byte* data = self->GetAlpha();
            Py_ssize_t len = self->GetWidth() * self->GetHeight();
            PyObject* rv;
            wxPyThreadBlocker blocker;
            rv = wxPyMakeBuffer(data, len);
            return rv;
            """)

    # SetDataBuffer, SetAlphaBuffer tell the image to use some other memory
    # buffer pointed to by a Python buffer object.
    c.addCppMethod('void', 'SetDataBuffer', '(wxPyBuffer* data)',
        doc="""\
        Sets the internal image data pointer to point at a Python buffer
        object.  This can save making an extra copy of the data but you must
        ensure that the buffer object lives lives at least as long as the
        :class:`Image` does.""",
        body="""\
            if (!data->checkSize(self->GetWidth() * self->GetHeight() * 3))
                return;
            // True means don't free() the pointer
            self->SetData((byte*)data->m_ptr, true);
            """)
    c.addCppMethod('void', 'SetDataBuffer', '(wxPyBuffer* data, int new_width, int new_height)',
        doc="""\
        Sets the internal image data pointer to point at a Python buffer
        object.  This can save making an extra copy of the data but you must
        ensure that the buffer object lives lives at least as long as the
        :class:`Image` does.""",
        body="""\
            if (!data->checkSize(new_width * new_height * 3))
                return;
            // True means don't free() the pointer
            self->SetData((byte*)data->m_ptr, new_width, new_height, true);
            """)


    c.addCppMethod('void', 'SetAlphaBuffer', '(wxPyBuffer* alpha)',
        doc="""\
        Sets the internal image alpha pointer to point at a Python buffer
        object.  This can save making an extra copy of the data but you must
        ensure that the buffer object lives lives at least as long as the
        :class:`Image` does.""",
        body="""\
            if (!alpha->checkSize(self->GetWidth() * self->GetHeight()))
                return;
            // True means don't free() the pointer
            self->SetAlpha((byte*)alpha->m_ptr, true);
            """)




    def setParamsPyInt(name):
        """Set the pyInt flag on 'unsigned char' params"""
        method = c.find(name)
        for m in [method] + method.overloads:
            for p in m.items:
                if p.type == 'unsigned char':
                    p.pyInt = True

    setParamsPyInt('Clear')
    setParamsPyInt('Replace')
    setParamsPyInt('ConvertAlphaToMask')
    setParamsPyInt('ConvertToMono')
    setParamsPyInt('ConvertToDisabled')
    setParamsPyInt('IsTransparent')
    setParamsPyInt('SetAlpha')
    setParamsPyInt('SetMaskColour')
    setParamsPyInt('SetMaskFromImage')
    setParamsPyInt('SetRGB')

    c.find('FindFirstUnusedColour').type = 'void'
    c.find('FindFirstUnusedColour.r').pyInt = True
    c.find('FindFirstUnusedColour.g').pyInt = True
    c.find('FindFirstUnusedColour.b').pyInt = True
    c.find('FindFirstUnusedColour.startR').pyInt = True
    c.find('FindFirstUnusedColour.startG').pyInt = True
    c.find('FindFirstUnusedColour.startB').pyInt = True
    c.find('FindFirstUnusedColour.r').out = True
    c.find('FindFirstUnusedColour.g').out = True
    c.find('FindFirstUnusedColour.b').out = True

    c.find('GetAlpha').findOverload('int x, int y').pyInt = True
    c.find('GetRed').pyInt = True
    c.find('GetGreen').pyInt = True
    c.find('GetBlue').pyInt = True
    c.find('GetMaskRed').pyInt = True
    c.find('GetMaskGreen').pyInt = True
    c.find('GetMaskBlue').pyInt = True

    c.find('GetOrFindMaskColour').type = 'void'
    c.find('GetOrFindMaskColour.r').pyInt = True
    c.find('GetOrFindMaskColour.g').pyInt = True
    c.find('GetOrFindMaskColour.b').pyInt = True
    c.find('GetOrFindMaskColour.r').out = True
    c.find('GetOrFindMaskColour.g').out = True
    c.find('GetOrFindMaskColour.b').out = True

    c.find('RGBValue.red').pyInt = True
    c.find('RGBValue.green').pyInt = True
    c.find('RGBValue.blue').pyInt = True
    c.find('RGBValue.RGBValue.r').pyInt = True
    c.find('RGBValue.RGBValue.g').pyInt = True
    c.find('RGBValue.RGBValue.b').pyInt = True


    c.addCppMethod('int', '__nonzero__', '()', 'return self->IsOk();')
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addPyMethod('ConvertToBitmap', '(self, depth=-1)',
        doc="""\
        ConvertToBitmap(depth=-1) -> Bitmap\n
        Convert the image to a :class:`wx.Bitmap`.""",
        body="""\
        bmp = wx.Bitmap(self, depth)
        return bmp
        """)

    c.addPyMethod('ConvertToMonoBitmap', '(self, red, green, blue)',
        doc="""\
        ConvertToMonoBitmap(red, green, blue) -> Bitmap\n
        Creates a monochrome version of the image and returns it as a :class:`wx.Bitmap`.""",
        body="""\
        mono = self.ConvertToMono( red, green, blue )
        bmp = wx.Bitmap( mono, 1 )
        return bmp
        """)


    c.addCppMethod('wxImage*', 'AdjustChannels',
        '(double factor_red, double factor_green, double factor_blue, double factor_alpha=1.0)',
        doc="""\
        This function muliplies all 4 channels (red, green, blue, alpha) with
        a factor (around 1.0). Useful for gamma correction, colour correction
        and to add a certain amount of transparency to a image (fade in fade
        out effects). If factor_alpha is given but the original image has no
        alpha channel then a alpha channel will be added.
        """,
        body="""\
        wxCHECK_MSG( self->Ok(), NULL, wxT("invalid image") );

        wxImage* dest = new wxImage( self->GetWidth(), self->GetHeight(), false );
        wxCHECK_MSG( dest && dest->IsOk(), NULL, wxT("unable to create image") );

        unsigned rgblen =   3 * self->GetWidth() * self->GetHeight();
        unsigned alphalen = self->GetWidth() * self->GetHeight();
        byte* src_data =  self->GetData();
        byte* src_alpha = self->GetAlpha();
        byte* dst_data =  dest->GetData();
        byte* dst_alpha = NULL;

        // adjust rgb
        if ( factor_red == 1.0 && factor_green == 1.0 && factor_blue == 1.0)
        {
            // nothing to do for RGB
            memcpy(dst_data, src_data, rgblen);
        }
        else
        {
            // rgb pixel for pixel
            for ( unsigned i = 0; i < rgblen; i= i + 3 )
            {
                dst_data[i] =     (byte) wxMin( 255, (int) (factor_red * src_data[i]) );
                dst_data[i + 1] = (byte) wxMin( 255, (int) (factor_green * src_data[i + 1]) );
                dst_data[i + 2] = (byte) wxMin( 255, (int) (factor_blue * src_data[i + 2]) );
            }
        }

        // adjust the mask colour
        if ( self->HasMask() )
        {
            dest->SetMaskColour((byte) wxMin( 255, (int) (factor_red * self->GetMaskRed() ) ),
                                (byte) wxMin( 255, (int) (factor_green * self->GetMaskGreen() ) ),
                                (byte) wxMin( 255, (int) (factor_blue * self->GetMaskBlue() ) ) );
        }

        // adjust the alpha channel
        if ( src_alpha )
        {
            // source image already has alpha information
            dest->SetAlpha(); // create an empty alpha channel (not initialized)
            dst_alpha = dest->GetAlpha();

            wxCHECK_MSG( dst_alpha, NULL, wxT("unable to create alpha data") );

            if ( factor_alpha == 1.0)
            {
                // no need to adjust
                memcpy(dst_alpha, src_alpha, alphalen);
            }
            else
            {
                // alpha value for alpha value
                for ( unsigned i = 0; i < alphalen; ++i )
                {
                    dst_alpha[i] = (byte) wxMin( 255, (int) (factor_alpha * src_alpha[i]) );
                }
            }
        }
        else if ( factor_alpha != 1.0 )
        {
            // no alpha yet but we want to adjust -> create
            dest->SetAlpha(); // create an empty alpha channel (not initialized)
            dst_alpha = dest->GetAlpha();

            wxCHECK_MSG( dst_alpha, NULL, wxT("unable to create alpha data") );

            for ( unsigned i = 0; i < alphalen; ++i )
            {
                dst_alpha[i] = (byte) wxMin( 255, (int) (factor_alpha * 255) );
            }
        }

        // do we have an alpha channel and a mask in the new image?
        if ( dst_alpha && dest->HasMask() )
        {
            // make the mask transparent honoring the alpha channel
            const byte mr = dest->GetMaskRed();
            const byte mg = dest->GetMaskGreen();
            const byte mb = dest->GetMaskBlue();

            for ( unsigned i = 0; i < alphalen; ++i )
            {
                int n = i * 3;
                dst_alpha[i] = ( dst_data[n] == mr && dst_data[n + 1] == mg && dst_data[n + 2] == mb )
                    ? wxIMAGE_ALPHA_TRANSPARENT
                    : dst_alpha[i];
            }

            // remove the mask now
            dest->SetMask(false);
        }

        return dest;""",
        factory=True)

    c.addProperty('Width GetWidth')
    c.addProperty('Height GetHeight')
    c.addProperty('MaskBlue GetMaskBlue')
    c.addProperty('MaskGreen GetMaskGreen')
    c.addProperty('MaskRed GetMaskRed')
    c.addProperty('Type GetType SetType')


    c.addCppMethod('wxRegion*', 'ConvertToRegion',
        '(int R=-1, int G=-1, int B=-1, int tolerance=0)',
        briefDoc="Create a :class:`wx.Region` where the transparent areas match the given RGB values.",
        detailedDoc=[dedent("""\
            If the RGB values are not given, then the image's mask colour components will
            be used instead. If a non-zero tolerance is given then the pixels that fall
            into the range of (R,G,B) to (R+tolerance, G+tolerance, B+tolerance) will be
            considered to be transparent.

            If there are no pixels matching the transparent colours then the region
            returned will match the image's full dimensions.

            :param int `R`: The red component of the transparent colour.
            :param int `G`: The red component of the transparent colour.
            :param int `B`: The red component of the transparent colour.
            :param int `tolerance`: Broadens the range of colours that will
                be considered transparent.
            :returns: a :class:`wx.Region` object.
            """)],
        body="""\
            wxRegion* region = new wxRegion();
            unsigned char hiR, hiG, hiB;

            if (R == -1) { R = self->GetMaskRed(); }
            if (G == -1) { G = self->GetMaskGreen(); }
            if (B == -1) { B = self->GetMaskBlue(); }

            // Make sure nothing out of range was passed
            R &= 0xFF;
            G &= 0xFF;
            B &= 0xFF;

            hiR = (unsigned char)wxMin(0xFF, R + tolerance);
            hiG = (unsigned char)wxMin(0xFF, G + tolerance);
            hiB = (unsigned char)wxMin(0xFF, B + tolerance);

            // Loop through the image row by row, pixel by pixel, building up
            // rectangles to add to the region.
            int width = self->GetWidth();
            int height = self->GetHeight();

            for (int y=0; y < height; y++)
            {
                wxRect rect;
                rect.y = y;
                rect.height = 1;

                for (int x=0; x < width; x++)
                {
                    // search for a continuous range of non-transparent pixels
                    int x0 = x;
                    while ( x < width)
                    {
                        unsigned char red = self->GetRed(x,y);
                        unsigned char grn = self->GetGreen(x,y);
                        unsigned char blu = self->GetBlue(x,y);
                        if (( red >= R && red <= hiR) &&
                            ( grn >= G && grn <= hiG) &&
                            ( blu >= B && blu <= hiB))  // It's transparent
                            break;
                        x++;
                    }

                    // Add the run of non-transparent pixels (if any) to the region
                    if (x > x0) {
                        rect.x = x0;
                        rect.width = x - x0;
                        region->Union(rect);
                    }
                }
            }
            if (region->IsEmpty())
                region->Union(0, 0, width, height);
            return region;
            """)


    # For compatibility:
    module.addPyFunction('EmptyImage', '(width=0, height=0, clear=True)',
                         deprecated="Use :class:`Image` instead.",
                         doc='A compatibility wrapper for the wx.Image(width, height) constructor',
                         body='return Image(width, height, clear)')

    module.addPyFunction('ImageFromBitmap', '(bitmap)',
                         deprecated="Use bitmap.ConvertToImage instead.",
                         doc='Create a :class:`Image` from a :class:`wx.Bitmap`',
                         body='return bitmap.ConvertToImage()')

    module.addPyFunction('ImageFromStream', '(stream, type=BITMAP_TYPE_ANY, index=-1)',
                         deprecated="Use :class:`Image` instead.",
                         doc='Load an image from a stream (file-like object)',
                         body='return wx.Image(stream, type, index)')

    module.addPyFunction('ImageFromData', '(width, height, data)',
                         deprecated="Use :class:`Image` instead.",
                         doc='Compatibility wrapper for creating an image from RGB data',
                         body='return Image(width, height, data)')

    module.addPyFunction('ImageFromDataWithAlpha', '(width, height, data, alpha)',
                         deprecated="Use :class:`Image` instead.",
                         doc='Compatibility wrapper for creating an image from RGB and Alpha data',
                         body='return Image(width, height, data, alpha)')



    module.addPyFunction('ImageFromBuffer', '(width, height, dataBuffer, alphaBuffer=None)',
        doc="""\
            Creates a :class:`Image` from the data in `dataBuffer`.  The `dataBuffer`
            parameter must be a Python object that implements the buffer interface,
            such as a string, array, etc.  The `dataBuffer` object is expected to
            contain a series of RGB bytes and be width*height*3 bytes long.  A buffer
            object can optionally be supplied for the image's alpha channel data, and
            it is expected to be width*height bytes long.

            The :class:`Image` will be created with its data and alpha pointers initialized
            to the memory address pointed to by the buffer objects, thus saving the
            time needed to copy the image data from the buffer object to the :class:`Image`.
            While this has advantages, it also has the shoot-yourself-in-the-foot
            risks associated with sharing a C pointer between two objects.

            To help alleviate the risk a reference to the data and alpha buffer
            objects are kept with the :class:`Image`, so that they won't get deleted until
            after the wx.Image is deleted.  However please be aware that it is not
            guaranteed that an object won't move its memory buffer to a new location
            when it needs to resize its contents.  If that happens then the :class:`Image`
            will end up referring to an invalid memory location and could cause the
            application to crash.  Therefore care should be taken to not manipulate
            the objects used for the data and alpha buffers in a way that would cause
            them to change size.
            """,
        body="""\
            img = Image(width, height)
            img.SetDataBuffer(dataBuffer)
            if alphaBuffer:
                img.SetAlphaBuffer(alphaBuffer)
            img._buffer = dataBuffer
            img._alpha = alphaBuffer
            return img
            """)

    #-------------------------------------------------------
    c = module.find('wxImageHistogram')
    c.bases = [] # wxImageHistogramBase doesn't actually exist
    setParamsPyInt('MakeKey')
    c.find('FindFirstUnusedColour').type = 'void'
    c.find('FindFirstUnusedColour.r').pyInt = True
    c.find('FindFirstUnusedColour.g').pyInt = True
    c.find('FindFirstUnusedColour.b').pyInt = True
    c.find('FindFirstUnusedColour.startR').pyInt = True
    c.find('FindFirstUnusedColour.startG').pyInt = True
    c.find('FindFirstUnusedColour.startB').pyInt = True
    c.find('FindFirstUnusedColour.r').out = True
    c.find('FindFirstUnusedColour.g').out = True
    c.find('FindFirstUnusedColour.b').out = True



    #-------------------------------------------------------
    c = module.find('wxImageHandler')
    c.addPrivateCopyCtor()
    c.find('GetLibraryVersionInfo').ignore()

    c.find('DoGetImageCount').ignore(False)
    c.find('DoCanRead').ignore(False)

    module.addHeaderCode("""\
        #include <wx/imaggif.h>
        #include <wx/imagiff.h>
        #include <wx/imagjpeg.h>
        #include <wx/imagpcx.h>
        #include <wx/imagpng.h>
        #include <wx/imagpnm.h>
        #include <wx/imagtga.h>
        #include <wx/imagtiff.h>
        #include <wx/imagxpm.h>
        """)

    #-------------------------------------------------------
    # tweak for GIFHandler
    # need to include anidecod.h, otherwise use of forward declared class
    # compilation errors will occur.
    c = module.find('wxGIFHandler')
    c.find('DoCanRead').ignore(False)

    module.addHeaderCode("#include <wx/anidecod.h>")
    module.addItem(tools.wxArrayWrapperTemplate('wxImageArray', 'wxImage', module))

    #-------------------------------------------------------
    # tweak for IFFHandler
    c = module.find('wxIFFHandler')
    c.find('DoCanRead').ignore(False)

    #-------------------------------------------------------
    # tweak for JPEGHandler
    c = module.find('wxJPEGHandler')
    c.find('DoCanRead').ignore(False)

    #-------------------------------------------------------
    # tweak for PCXHandler
    c = module.find('wxPCXHandler')
    c.find('DoCanRead').ignore(False)

    #-------------------------------------------------------
    # tweak for PNGHandler
    c = module.find('wxPNGHandler')
    c.find('DoCanRead').ignore(False)

    #-------------------------------------------------------
    # tweak for PNMHandler
    c = module.find('wxPNMHandler')
    c.find('DoCanRead').ignore(False)

    #-------------------------------------------------------
    # tweak for TGAHandler
    c = module.find('wxTGAHandler')
    c.find('DoCanRead').ignore(False)

    #-------------------------------------------------------
    # tweak for TIFFHandler
    c = module.find('wxTIFFHandler')
    c.find('GetLibraryVersionInfo').ignore()
    c.find('DoCanRead').ignore(False)

    #-------------------------------------------------------
    # tweak for XPMHandler
    c = module.find('wxXPMHandler')
    c.find('DoCanRead').ignore(False)

    #-------------------------------------------------------

    module.find('wxIMAGE_ALPHA_TRANSPARENT').pyInt = True
    module.find('wxIMAGE_ALPHA_OPAQUE').pyInt = True
    module.find('wxIMAGE_ALPHA_THRESHOLD').pyInt = True

    # These are defines for string objects, not integers, so we can't
    # generate code for them the same way as integer values. Since they are
    # #defines we can't just tell SIP that they are global wxString objects
    # because it will then end up taking the address of temporary values when
    # it makes the getters for them. So instead we'll just make some python
    # code to insert into the .py module and hope that the interface file
    # always has the correct values of these options.
    pycode = ""
    for item in module:
        if 'IMAGE_OPTION' in item.name and isinstance(item, etgtools.DefineDef):
            item.ignore()
            name = tools.removeWxPrefix(item.name)
            value = item.value
            for txt in ['wxString(', 'wxT(', ')']:
                value = value.replace(txt, '')

            pycode += '%s = %s\n' % (name, value)
    module.addPyCode(pycode)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

