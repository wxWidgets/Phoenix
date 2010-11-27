#---------------------------------------------------------------------------
# Name:        etc/colour.py
# Author:      Robin Dunn
#
# Created:     19-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "colour"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'wxColour' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
    
    
    # Add a ctor/factory for the Mac that can use the theme brush
    module.addCppCode("""\
    #ifdef __WXMAC__
    #include <wx/osx/carbon/private.h>
    #endif
    """)
    
    module.addCppFunction('wxColour', 'MacThemeColour', '(int themeBrushID)', """\
    #ifdef __WXMAC__
        sipRes = new wxColour(wxMacCreateCGColorFromHITheme(themeBrushID));
    #else
        wxPyRaiseNotImplemented(); 
        sipIsErr = 1;
        sipRes = NULL; 
    #endif
    """, factory=True)
    
    # Change this macro into a value so we wont have problems when SIP takes its
    # address
    module.addCppCode("""\
    #undef wxTransparentColour
    wxColour wxTransparentColour(0, 0, 0, wxALPHA_TRANSPARENT);
    """)
    
    
    module.find('wxFromString').ignore()
    module.find('wxToString').ignore()
    
    # TODO: fix this?
    for name in [ 'wxBLACK',
                  'wxBLUE',             
                  'wxCYAN',
                  'wxGREEN',
                  'wxYELLOW',
                  'wxLIGHT_GREY',
                  'wxRED',
                  'wxWHITE',
                  ]:
        module.find(name).ignore()
    
    module.find('wxALPHA_TRANSPARENT').type = 'const int'
    module.find('wxALPHA_OPAQUE').type = 'const int'
        
    
        
    c = module.find('wxColour')
    assert isinstance(c, etgtools.ClassDef)
    tools.removeVirtuals(c)
    
    # Hide the string ctor so our typemap will be invoked for the copy ctor instead.
    c.find('wxColour').findOverload('wxString').ignore()
    
    c.addProperty('Pixel GetPixel')
    c.addProperty('RGB GetRGB SetRGB')
    c.addProperty('RGBA GetRGBA SetRGBA')
    c.addProperty('red Red')
    c.addProperty('green Green')
    c.addProperty('blue Blue')
    c.addProperty('alpha Alpha')
    
    c.find('GetPixel').ignore()  # We need to add a typcast
    c.addCppMethod('wxIntPtr', 'GetPixel', '()', """\
        sipRes = (wxIntPtr)sipCpp->GetPixel();
    """)
        
    # Set a flag on the return value and parameter types that are 'unsigned char'
    # such that they will be treated as an integer instead of a string. 
    for item in c.allItems():
        if hasattr(item, 'type') and item.type == 'unsigned char':
            item.pyInt = True
            
    
    c.find('ChangeLightness.r').inOut = True
    c.find('ChangeLightness.g').inOut = True
    c.find('ChangeLightness.b').inOut = True
    
    c.find('MakeDisabled.r').inOut = True
    c.find('MakeDisabled.g').inOut = True
    c.find('MakeDisabled.b').inOut = True
    
    c.find('MakeGrey.r').inOut = True
    c.find('MakeGrey.g').inOut = True
    c.find('MakeGrey.b').inOut = True
    c.find('MakeGrey').findOverload('double').find('r').inOut = True
    c.find('MakeGrey').findOverload('double').find('g').inOut = True
    c.find('MakeGrey').findOverload('double').find('b').inOut = True
    
    c.find('MakeMono.r').out = True
    c.find('MakeMono.g').out = True
    c.find('MakeMono.b').out = True
    
    
    c.addCppMethod('SIP_PYOBJECT', 'Get', '(bool includeAlpha=true)', """\
        int red = -1;
        int green = -1;
        int blue = -1;
        int alpha = wxALPHA_OPAQUE;
        if (sipCpp->IsOk()) {
            red =   sipCpp->Red();
            green = sipCpp->Green();
            blue =  sipCpp->Blue();
            alpha = sipCpp->Alpha();
        }
        if (includeAlpha)
            sipRes = sipBuildResult(&sipIsErr, "(iiii)", red, green, blue, alpha);
        else
            sipRes = sipBuildResult(&sipIsErr, "(iii)", red, green, blue);
    """, briefDoc="""\
        Get(includeAlpha=Valse) -> (r,g,b) or (r,g,b,a)\n
        Returns the RGB intensity values as a tuple, optionally the alpha value as well.""")
    
    
    # Add sequence protocol methods and other goodies
    c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
    c.addPyMethod('__repr__', '(self)',            'return "wx.Colour"+str(self.Get())')
    c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
    c.addPyMethod('__nonzero__', '(self)',         'return self.IsOk()')
    c.addPyMethod('__reduce__', '(self)',          'return (Colour, self.Get())')
    c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
    c.addPyMethod('__setitem__', '(self, idx, val)',
                  """\
                  if idx == 0: self.red = val
                  elif idx == 1: self.green = val
                  elif idx == 2: self.blue = val
                  elif idx == 3: self.alpha = val
                  else: raise IndexError
                  """) 
    c.addPyCode('Rect.__safe_for_unpickling__ = True')
    
    
    
    
    
    # Types that can be converted to wx.Colour:
    #     wxColour (duh)
    #     Sequence with 3 or 4 integers
    #     String with color name or #RRGGBB or #RRGGBBAA format
    #     None  (converts to wxNullColour)
    c.allowNone = True
    c.convertFromPyObject = """\
        // is it just a typecheck?
        if (!sipIsErr) {
            if (sipPy == Py_None)
                return 1;
            if (sipCanConvertToType(sipPy, sipType_wxColour, SIP_NO_CONVERTORS))
                return 1;
            if (PyString_Check(sipPy) || PyUnicode_Check(sipPy))
                return 1;           
            if (PySequence_Check(sipPy)) {
                size_t len = PySequence_Size(sipPy);
                if (len != 3 && len != 4) 
                    return 0;
                // ensure all the items in the sequence are numbers
                for (int idx=0; idx<len; idx+=1) {
                    PyObject* o = PySequence_ITEM(sipPy, idx);
                    bool isNum = PyNumber_Check(o);
                    Py_DECREF(o);
                    if (!isNum)
                        return 0;
                }
                return 1;
            }
            return 0;
        }
        // otherwise do the conversion
        // is it None?
        if (sipPy == Py_None) {
            *sipCppPtr = new wxColour(wxNullColour);
            return sipGetState(sipTransferObj);
        }
        // Is it a string?
        else if (PyString_Check(sipPy) || PyUnicode_Check(sipPy)) {
            wxString spec = Py2wxString(sipPy);
            if (spec.GetChar(0) == '#' 
                && (spec.length() == 7 || spec.length() == 9)) {  // It's  #RRGGBB[AA]
                long red, green, blue;
                red = green = blue = 0;
                spec.Mid(1,2).ToLong(&red,   16);
                spec.Mid(3,2).ToLong(&green, 16);
                spec.Mid(5,2).ToLong(&blue,  16);
    
                if (spec.length() == 7)         // no alpha
                    *sipCppPtr = new wxColour(red, green, blue);
                else {                          // yes alpha
                    long alpha;
                    spec.Mid(7,2).ToLong(&alpha, 16);
                    *sipCppPtr = new wxColour(red, green, blue, alpha);
                }
                return sipGetState(sipTransferObj);
            }
            else {                                       // assume it's a colour name
                // check if alpha is there too
                int pos;
                if (((pos = spec.Find(':', true)) != wxNOT_FOUND) && (pos == spec.length()-3)) {
                    long alpha;
                    spec.Right(2).ToLong(&alpha, 16);
                    wxColour c = wxColour(spec.Left(spec.length()-3));
                    *sipCppPtr = new wxColour(c.Red(), c.Green(), c.Blue(), alpha);
                }
                else
                    *sipCppPtr = new wxColour(spec);
                return sipGetState(sipTransferObj);
            }
        }
        // Is it a 3 or 4 element sequence?
        else if (PySequence_Check(sipPy)) {
            size_t len = PyObject_Length(sipPy);
            
            PyObject* o1 = PySequence_GetItem(sipPy, 0);
            PyObject* o2 = PySequence_GetItem(sipPy, 1);
            PyObject* o3 = PySequence_GetItem(sipPy, 2);
            if (len == 3) 
                *sipCppPtr = new wxColour(PyInt_AsLong(o1), PyInt_AsLong(o2), PyInt_AsLong(o3));
            else {
                PyObject* o4 = PySequence_GetItem(sipPy, 3);
                *sipCppPtr = new wxColour(PyInt_AsLong(o1), PyInt_AsLong(o2), PyInt_AsLong(o3),
                                          PyInt_AsLong(o4));
                Py_DECREF(o4);
            }
            Py_DECREF(o1);
            Py_DECREF(o2);
            Py_DECREF(o3);
            return sipGetState(sipTransferObj);
        }
    
        // if we get this far then it must already be a wxColour instance
        *sipCppPtr = reinterpret_cast<wxColour*>(sipConvertToType(
            sipPy, sipType_wxColour, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
        return sipGetState(sipTransferObj);
    """
    
    
    
    # Just for TESTING, remove it later
    module.addCppCode("""\
    wxColour testColourTypeMap(const wxColour& c)
    {
        return c;
    }
    extern void wxInitializeStockLists();
    """)
    module.addItem(etgtools.WigCode("""\
    wxColour testColourTypeMap(const wxColour& c);
    void wxInitializeStockLists();
    """))
    
    
    #-----------------------------------------------------------------
    tools.ignoreAssignmentOperators(module)
    tools.removeWxPrefixes(module)
    #-----------------------------------------------------------------
    # Run the generators
    
    # Create the code generator and make the wrapper code
    wg = etgtools.getWrapperGenerator()
    wg.generate(module)
    
    # Create a documentation generator and let it do its thing
    dg = etgtools.getDocsGenerator()
    dg.generate(module)
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

