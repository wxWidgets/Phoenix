#---------------------------------------------------------------------------
# Name:        gdicmn.py
# Author:      Robin Dunn
#
# Created:     4-Nov-2010
# RCS-ID:      $Id:$
# Copyright:   (c) 2010 by Total Control Software
# Licence:     wxWindows license
#---------------------------------------------------------------------------

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "gdicmn"
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [
    'wxPoint',
    'wxSize',
    'wxRect',
    'wxRealPoint',
]    
    
#---------------------------------------------------------------------------
# Parse the XML file(s) building a collection of Extractor objects

import etgtools
module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
etgtools.parseDoxyXML(module, ITEMS)

#---------------------------------------------------------------------------
# Tweak the parsed meta objects in the module object as needed for customizing
# the generated code and docstrings.

import etgtools.tweaker_tools
etgtools.tweaker_tools.ignoreAssignmentOperators(module)
etgtools.tweaker_tools.removeWxPrefixes(module)


module.addHeaderCode('#include <wx/wx.h>')

# ignore some of these enum values
e = module.find('wxBitmapType')
for i in e:
    if i.name.endswith('_RESOURCE'):
        i.ignore()

# TODO: We need an ETG way to indicate that an item is only available
# on certain platofmrs.
e = module.find('wxStockCursor')
e.find('wxCURSOR_BASED_ARROW_DOWN').ignore()
e.find('wxCURSOR_BASED_ARROW_UP').ignore()
e.find('wxCURSOR_CROSS_REVERSE').ignore()
e.find('wxCURSOR_DOUBLE_ARROW').ignore()

        
module.find('wxTheColourDatabase').ignore()  # TODO
module.find('wxSetCursor').ignore()          # TODO

module.find('wxClientDisplayRect.x').out = True
module.find('wxClientDisplayRect.y').out = True
module.find('wxClientDisplayRect.width').out = True
module.find('wxClientDisplayRect.height').out = True

module.find('wxDisplaySize.width').out = True
module.find('wxDisplaySize.height').out = True
module.find('wxDisplaySizeMM.width').out = True
module.find('wxDisplaySizeMM.height').out = True

#---------------------------------------
# wxPoint tweaks
c = module.find('wxPoint')

# Some operators are documented within the class that shouldn't be, so just
# ignore them all.
etgtools.tweaker_tools.ignoreAllOperators(c)

# Undo a few of those ignores for legitimate items that were 
# documented correctly
for f in c.find('operator+=').all() + c.find('operator-=').all():
    f.ignore(False)
    
# Add some stand-alone function declarations for the operators that really do
# exist.
wc = etgtools.WigCode("""\
bool operator==(const wxPoint& p1, const wxPoint& p2);
bool operator!=(const wxPoint& p1, const wxPoint& p2);
wxPoint operator+(const wxPoint& p, const wxSize& s);
wxPoint operator+(const wxPoint& p1, const wxPoint& p2);
wxPoint operator+(const wxSize& s, const wxPoint& p);
wxPoint operator-(const wxPoint& p);
wxPoint operator-(const wxPoint& p, const wxSize& s);
wxPoint operator-(const wxPoint& p1, const wxPoint& p2);
wxPoint operator-(const wxSize& s, const wxPoint& p);
wxPoint operator*(const wxPoint& s, int i);
wxPoint operator*(int i, const wxPoint& s);
wxPoint operator/(const wxPoint& s, int i);
""")
module.insertItemAfter(c, wc)

# wxPoint typemap
c.convertFromPyObject = """\
   // is it just a typecheck?
   if (!sipIsErr) {
       if (sipCanConvertToType(sipPy, sipType_wxPoint, SIP_NO_CONVERTORS))
           return 1;

       if (PySequence_Check(sipPy) and PySequence_Size(sipPy) == 2) {
           int rval = 1;
           PyObject* o1 = PySequence_ITEM(sipPy, 0);
           PyObject* o2 = PySequence_ITEM(sipPy, 1);
           if (!PyNumber_Check(o1) || !PyNumber_Check(o2)) 
               rval = 0;
           Py_DECREF(o1);
           Py_DECREF(o2);
           return rval;
       }
       return 0;
   }   
   
   // otherwise do the conversion
   if (sipPy == Py_None) {
       *sipCppPtr = new wxPoint(-1, -1);
       return sipGetState(sipTransferObj);
   }
   
   if (PySequence_Check(sipPy)) {
       PyObject* o1 = PySequence_ITEM(sipPy, 0);
       PyObject* o2 = PySequence_ITEM(sipPy, 1);
       *sipCppPtr = new wxPoint(PyInt_AsLong(o1), PyInt_AsLong(o2));
       Py_DECREF(o1);
       Py_DECREF(o2);
       return sipGetState(sipTransferObj);
    }
    
    *sipCppPtr = reinterpret_cast<wxPoint*>(sipConvertToType(
                sipPy, sipType_wxPoint, sipTransferObj, SIP_NO_CONVERTORS, 0, sipIsErr));
    return 0;
"""


#---------------------------------------
# wxSize tweaks
c = module.find('wxSize')

c.addProperty("width GetWidth SetWidth")
c.addProperty("height GetHeight SetHeight")

# take care of the same issues as wxPoint
etgtools.tweaker_tools.ignoreAllOperators(c)
for f in c.find('operator+=').all() + \
         c.find('operator-=').all() + \
         c.find('operator*=').all() + \
         c.find('operator/=').all():
    f.ignore(False)
wc = etgtools.WigCode("""\
bool operator==(const wxSize& s1, const wxSize& s2);
bool operator!=(const wxSize& s1, const wxSize& s2);
wxSize operator*(const wxSize& s, int i);
wxSize operator*(int i, const wxSize& s);
wxSize operator+(const wxSize& s1, const wxSize& s2);
wxSize operator-(const wxSize& s1, const wxSize& s2);
wxSize operator/(const wxSize& s, int i);
""")
module.insertItemAfter(c, wc)


#---------------------------------------
# wxRect tweaks
c = module.find('wxRect')

# take care of the same issues as wxPoint
etgtools.tweaker_tools.ignoreAllOperators(c)
for f in c.find('operator+=').all() + \
         c.find('operator*=').all():
    f.ignore(False)
wc = etgtools.WigCode("""\
bool operator==(const wxRect& r1, const wxRect& r2);
bool operator!=(const wxRect& r1, const wxRect& r2);
wxRect operator+(const wxRect& r1, const wxRect& r2);
wxRect operator*(const wxRect& r1, const wxRect& r2);
""")
module.insertItemAfter(c, wc)

# These methods have some overloads that will end up with the same signature
# in Python, so we have to remove one.
module.find('wxRect.Deflate').findOverload(') const').ignore()
module.find('wxRect.Inflate').findOverload(') const').ignore()
module.find('wxRect.Union').findOverload(') const').ignore()
module.find('wxRect.Intersect').findOverload(') const').ignore()


#---------------------------------------
# wxRealPoint tweaks
c = module.find('wxRealPoint')
    
# take care of the same issues as wxPoint
etgtools.tweaker_tools.ignoreAllOperators(c)
for f in c.find('operator+=').all() + \
         c.find('operator-=').all():
    f.ignore(False)
wc = etgtools.WigCode("""\
bool operator==(const wxRealPoint& p1, const wxRealPoint& p2);
bool operator!=(const wxRealPoint& p1, const wxRealPoint& p2);
wxRealPoint operator*(const wxRealPoint& s, double i);
wxRealPoint operator*(double i, const wxRealPoint& s);
wxRealPoint operator+(const wxRealPoint& p1, const wxRealPoint& p2);
wxRealPoint operator-(const wxRealPoint& p1, const wxRealPoint& p2);
wxRealPoint operator/(const wxRealPoint& s, int i);
""")
module.insertItemAfter(c, wc)



#---------------------------------------------------------------------------
#---------------------------------------------------------------------------
# Run the generators

# Create the code generator and make the wrapper code
wg = etgtools.getWrapperGenerator()
wg.generate(module)

# Create a documentation generator and let it do its thing
dg = etgtools.getDocsGenerator()
dg.generate(module)

#---------------------------------------------------------------------------
