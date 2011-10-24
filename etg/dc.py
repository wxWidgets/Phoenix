#---------------------------------------------------------------------------
# Name:        etg/stattext.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     26-Aug-2011
# Copyright:   (c) 2011 by Wide Open Technologies
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "dc"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxFontMetrics',
           'wxDC', 
           'wxDCClipper',
           'wxDCBrushChanger',
           'wxDCPenChanger',
           'wxDCTextColourChanger',
           'wxDCFontChanger',
           ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
            
    c = module.find('wxDC')
    assert isinstance(c, etgtools.ClassDef)

    c.addPrivateCopyCtor()
    c.addPublic()
    tools.removeVirtuals(c)
    
    # rename the more complex overload for these two, like in classic wxPython
    c.find('GetTextExtent').findOverload('wxCoord *').pyName = 'GetFullTextExtent'
    c.find('GetMultiLineTextExtent').findOverload('wxCoord *').pyName = 'GetFullMultiLineTextExtent'                   
    
    # Keep only the wxSize overloads of these
    c.find('GetSize').findOverload('wxCoord').ignore()
    c.find('GetSizeMM').findOverload('wxCoord').ignore()
    
    # TODO: needs wxAffineMatrix2D support.
    c.find('GetTransformMatrix').ignore()
    c.find('SetTransformMatrix').ignore()

    # remove wxPoint* overloads, we use the wxPointList ones
    c.find('DrawLines').findOverload('wxPoint points').ignore()
    c.find('DrawPolygon').findOverload('wxPoint points').ignore()
    c.find('DrawSpline').findOverload('wxPoint points').ignore()

    # TODO: we'll need a custom method implementation for this since there
    # are multiple array parameters involved...
    c.find('DrawPolyPolygon').ignore()


    
    # Add output param annotations so the generated docstrings will be correct
    c.find('GetUserScale.x').out = True
    c.find('GetUserScale.y').out = True

    c.find('GetLogicalScale.x').out = True
    c.find('GetLogicalScale.y').out = True
    
    c.find('GetLogicalOrigin').overloads = []
    c.find('GetLogicalOrigin.x').out = True
    c.find('GetLogicalOrigin.y').out = True
    
    c.find('GetTextExtent.w').out = True
    c.find('GetTextExtent.h').out = True
    c.find('GetTextExtent.descent').out = True
    c.find('GetTextExtent.externalLeading').out = True

    c.find('GetMultiLineTextExtent.w').out = True
    c.find('GetMultiLineTextExtent.h').out = True
    c.find('GetMultiLineTextExtent.heightLine').out = True
    
    c.find('GetClippingBox.x').out = True
    c.find('GetClippingBox.y').out = True
    c.find('GetClippingBox.width').out = True
    c.find('GetClippingBox.height').out = True
    c.addPyMethod('GetClippingRect', '(self)', 
        doc="Gets the rectangle surrounding the current clipping region",
        body="return wx.Rect(*self.GetClippingBox())")

    
    # Add some alternate implementations for DC methods, in order to avoid
    # using parameters as return values, etc. as well as Classic
    # compatibility.
    c.find('GetPixel').ignore()
    c.addCppMethod('wxColour*', 'GetPixel', '(wxCoord x, wxCoord y)', 
        doc="Gets the colour at the specified location on the DC.", body="""\
        wxColour* col = new wxColour;
        self->GetPixel(x, y, col);
        return col;
        """, factory=True)

    # Return the rect instead of using an output parameter
    m = c.find('DrawLabel')
    m.type = 'wxRect*'
    m.find('rectBounding').ignore()
    m.factory = True  # a new instance is being created
    m.setCppCode("""\
        wxRect rv;
        self->DrawLabel(*text, *bitmap, *rect, alignment, indexAccel, &rv);
        return new wxRect(rv);
        """)
    c.addPyCode('DC.DrawImageLabel = wx.deprecated(DC.DrawLabel)')

    # Return the array instead of using an output parameter
    m = c.find('GetPartialTextExtents')
    m.type = 'wxArrayInt*'
    m.find('widths').ignore()
    m.factory = True  # a new instance is being created
    m.setCppCode("""\
        wxArrayInt rval;
        self->GetPartialTextExtents(*text, rval);
        return new wxArrayInt(rval);
        """)

    
    c.addCppMethod('int', '__nonzero__', '()', """\
        return self->IsOk();
        """)
   
    c.addPyMethod('GetBoundingBox', '(self)', doc="""\
        GetBoundingBox() -> (x1,y1, x2,y2)\n
        Returns the min and max points used in drawing commands so far.""",
        body="return (self.MinX(), self.MinY(), self.MaxX(), self.MaxY())")
    
    
    # Add some methods that return handles to the platform specific parts of a wxDC
    c.addHeaderCode("""\
        #ifdef __WXMSW__
        #include <wx/msw/dc.h>
        #endif
        #ifdef __WXGTK__
        #include <wx/gtk/dc.h>
        #endif
        #include <wx/dcgraph.h>
        """)
    c.addCppMethod('long', 'GetHDC', '()', """\
        #ifdef __WXMSW__
            return (long)((wxMSWDCImpl*)self->GetImpl())->GetHDC();
        #else
            wxPyRaiseNotImplemented();
            return 0;
        #endif""")
    c.addCppMethod('void*', 'GetCGContext', '()', """\
        #ifdef __WXMAC__
            void* cgctx = NULL;
            wxGraphicsContext* gc = ((wxGCDCImpl*)self->GetImpl())->GetGraphicsContext();
            if (gc) {
                cgctx = gc->GetNativeContext();
            }
            return cgctx;
        #else
            wxPyRaiseNotImplemented();
            return NULL;
        #endif""")
    c.addCppMethod('void*', 'GetGdkDrawable', '()', """\
        #ifdef __WXGTK__
            // TODO: Is this always non-null?  if not then we can check
            // GetSelectedBitmap and get the GdkPixmap from it, as that is a
            // drawable too.
            return ((wxGTKDCImpl*)self->GetImpl())->GetGDKWindow();
        #else
            wxPyRaiseNotImplemented();
            return NULL;
        #endif""")
    

    # TODO: Port the wxPyDrawXXX code and the DrawXXXList methods from Classic
    # TODO: Port the PseudoDC from Classic

    
    c = module.find('wxDCClipper')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')
    
    c = module.find('wxDCBrushChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')
    
    c = module.find('wxDCPenChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')
    
    c = module.find('wxDCTextColourChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')
    
    c = module.find('wxDCFontChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')
    
    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

