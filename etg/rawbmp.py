#---------------------------------------------------------------------------
# Name:        etg/rawbmp.py
# Author:      Robin Dunn
#
# Created:     14-Aug-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import (ClassDef, MethodDef, ParamDef, TypedefDef, WigCode,
                      CppMethodDef, PyMethodDef)

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "rawbmp"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]

# NOTE: It is intentional that there are no items in the ITEMS list. This is
# because we will not be loading any classes from the doxygen XML files here,
# but rather will be constructing the extractor objects here in this module
# instead.


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode("#include <wx/rawbmp.h>")

    addPixelDataBaseClass(module)

    addPixelDataClass(module, 'wxNativePixelData', 'wxBitmap', bpp=24,
        doc="""\
        A class providing direct access to a :class:`wx.Bitmap`'s
        internal data without alpha channel (RGB).
        """)
    addPixelDataClass(module, 'wxAlphaPixelData', 'wxBitmap', bpp=32,
        doc="""\
        A class providing direct access to a :class:`wx.Bitmap`'s
        internal data including the alpha channel (RGBA).
        """)
    #addPixelDataClass(module, 'wxImagePixelData', 'wxImage', bpp=32,
    #    doc="""\
    #    ImagePixelData: A class providing direct access to a wx.Image's
    #    internal data using the same api as the other PixelData classes.
    #    """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

def addPixelDataBaseClass(module):
    # wxPixelDataBase is the common base class of the other pixel data classes
    cls = ClassDef(name='wxPixelDataBase', items=[
        MethodDef(
            name='wxPixelDataBase', isCtor=True, protection='protected'),
        MethodDef(
            type='wxPoint', name='GetOrigin',  isConst=True,
            briefDoc="Return the origin of the area this pixel data represents."),
        MethodDef(
            type='int', name='GetWidth', isConst=True,
            briefDoc="Return the width of the area this pixel data represents."),
        MethodDef(
            type='int', name='GetHeight', isConst=True,
            briefDoc="Return the height of the area this pixel data represents."),
        MethodDef(
            type='wxSize', name='GetSize', isConst=True,
            briefDoc="Return the size of the area this pixel data represents."),
        MethodDef(
            type='int', name='GetRowStride', isConst=True,
            briefDoc="Returns the distance between the start of one row to the start of the next row."),
        ])

    # TODO: Try to remember why I chose to do it this way instead of directly
    # returning an instance of the Iterator and giving it the methods needed
    # to be a Python iterator...

    # TODO: Determine how much of a performance difference not using the
    # PixelFacade class would make. Not using the __iter__ makes about 0.02
    # seconds difference per 100x100 bmp in samples/rawbmp/rawbmp1.py...

    cls.addPyMethod('__iter__', '(self)',
        doc="""\
            Create and return an iterator/generator object for traversing
            this pixel data object.
            """,
        body="""\
            width  = self.GetWidth()
            height = self.GetHeight()
            pixels = self.GetPixels() # this is the C++ iterator

            # This class is a facade over the pixels object (using the one
            # in the enclosing scope) that only allows Get() and Set() to
            # be called.
            class PixelFacade(object):
                def Get(self):
                    return pixels.Get()
                def Set(self, *args, **kw):
                    return pixels.Set(*args, **kw)
                def __str__(self):
                    return str(self.Get())
                def __repr__(self):
                    return 'pixel(%d,%d): %s' % (x,y,self.Get())
                X = property(lambda self: x)
                Y = property(lambda self: y)

            import sys
            rangeFunc = range if sys.version_info >= (3,) else xrange

            pf = PixelFacade()
            for y in rangeFunc(height):
                pixels.MoveTo(self, 0, y)
                for x in rangeFunc(width):
                    # We always generate the same pf instance, but it
                    # accesses the pixels object which we use to iterate
                    # over the pixel buffer.
                    yield pf
                    pixels.nextPixel()
            """)

    module.addItem(cls)



def addPixelDataClass(module, pd, img, bpp, doc=""):
    # This function creates a ClassDef for a PixelData class defined in C++.
    # The C++ versions are template instantiations, so this allows us to
    # create nearly identical classes and just substitute the image class
    # name and the pixel data class name.

    #itrName = 'Iterator'

    itrName = pd + '_Accessor'
    module.addHeaderCode('typedef %s::Iterator %s;' % (pd, itrName))


    # First generate the class and methods for the PixelData class
    cls = ClassDef(name=pd, bases=['wxPixelDataBase'], briefDoc=doc, items=[
        MethodDef(name=pd, isCtor=True, items=[
            ParamDef(type=img+'&', name='bmp')],
            overloads=[
                MethodDef(name=pd, isCtor=True, items=[
                    ParamDef(type=img+'&',         name='bmp'),
                    ParamDef(type='const wxRect&', name='rect')]),

                MethodDef(name=pd, isCtor=True, items=[
                    ParamDef(type=img+'&',          name='bmp'),
                    ParamDef(type='const wxPoint&', name='pt' ),
                    ParamDef(type='const wxSize&',  name='sz' )]),
                ]),

        MethodDef(name='~'+pd, isDtor=True),

        MethodDef(type=itrName, name='GetPixels', isConst=True),

        CppMethodDef('int', '__nonzero__', '()', body="return (int)self->operator bool();"),
        CppMethodDef('int', '__bool__', '()', body="return self->operator bool();"),
        ])

    # add this class to the module
    module.addItem(cls)


    # Now do the class and methods for its C++ Iterator class
    icls = ClassDef(name=itrName, items=[
        # Constructors
        MethodDef(name=itrName, isCtor=True, items=[
            ParamDef(name='data', type=pd+'&')],
            overloads=[
                MethodDef(name=itrName, isCtor=True, items=[
                    ParamDef(name='bmp', type=img+'&'),
                    ParamDef(name='data', type=pd+'&')]),
                MethodDef(name=itrName, isCtor=True)]),

        MethodDef(name='~'+itrName, isDtor=True),

        # Methods
        MethodDef(type='void', name='Reset', items=[
            ParamDef(type='const %s&' % pd, name='data')]),

        MethodDef(type='bool', name='IsOk', isConst=True),

        CppMethodDef('int', '__nonzero__', '()', body="return (int)self->IsOk();"),
        CppMethodDef('int', '__bool__', '()', body="return self->IsOk();"),

        MethodDef(type='void', name='Offset', items=[
            ParamDef(type='const %s&' % pd, name='data'),
            ParamDef(type='int', name='x'),
            ParamDef(type='int', name='y')]),

        MethodDef(type='void', name='OffsetX', items=[
            ParamDef(type='const %s&' % pd, name='data'),
            ParamDef(type='int', name='x')]),

        MethodDef(type='void', name='OffsetY', items=[
            ParamDef(type='const %s&' % pd, name='data'),
            ParamDef(type='int', name='y')]),

        MethodDef(type='void', name='MoveTo', items=[
            ParamDef(type='const %s&' % pd, name='data'),
            ParamDef(type='int', name='x'),
            ParamDef(type='int', name='y')]),

        # should this return the iterator?
        CppMethodDef('void', 'nextPixel', '()', body="++(*self);"),

        # NOTE: For now I'm not wrapping the Red, Green, Blue and Alpha
        # functions because I can't hide the premultiplying needed on wxMSW
        # if only the individual components are wrapped, plus it would mean 3
        # or 4 trips per pixel from Python to C++ instead of just one.
        # Instead I'll add the Set and Get functions below and put the
        # premultiplying in there.
        ])

    assert bpp in [24, 32]

    if bpp == 24:
        icls.addCppMethod('void', 'Set', '(byte red, byte green, byte blue)',
            body="""\
                self->Red()   = red;
                self->Green() = green;
                self->Blue()  = blue;
                """)

        icls.addCppMethod('PyObject*', 'Get', '()',
            body="""\
                wxPyThreadBlocker blocker;
                PyObject* rv = PyTuple_New(3);
                PyTuple_SetItem(rv, 0, wxPyInt_FromLong(self->Red()));
                PyTuple_SetItem(rv, 1, wxPyInt_FromLong(self->Green()));
                PyTuple_SetItem(rv, 2, wxPyInt_FromLong(self->Blue()));
                return rv;
                """)

    elif bpp == 32:
        icls.addCppMethod('void', 'Set', '(byte red, byte green, byte blue, byte alpha)',
            body="""\
                self->Red()   = wxPy_premultiply(red,   alpha);
                self->Green() = wxPy_premultiply(green, alpha);
                self->Blue()  = wxPy_premultiply(blue,  alpha);
                self->Alpha() = alpha;
                """)

        icls.addCppMethod('PyObject*', 'Get', '()',
            body="""\
                wxPyThreadBlocker blocker;
                PyObject* rv = PyTuple_New(4);
                int red   = self->Red();
                int green = self->Green();
                int blue  = self->Blue();
                int alpha = self->Alpha();

                PyTuple_SetItem(rv, 0, wxPyInt_FromLong( wxPy_unpremultiply(red,   alpha) ));
                PyTuple_SetItem(rv, 1, wxPyInt_FromLong( wxPy_unpremultiply(green, alpha) ));
                PyTuple_SetItem(rv, 2, wxPyInt_FromLong( wxPy_unpremultiply(blue,  alpha) ));
                PyTuple_SetItem(rv, 3, wxPyInt_FromLong( alpha ));
                return rv;
                """)



    # add it to the main pixel data class as a nested class
    #cls.insertItem(0, icls)

    # It's really a nested class, but we're pretending that it isn't (see the
    # typedef above) so add it at the module level instead.
    module.addItem(icls)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

