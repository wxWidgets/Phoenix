#---------------------------------------------------------------------------
# Name:        gdicmn.py
# Author:      Robin Dunn
#
# Created:     4-Nov-2010
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

import etgtools.tweaker_tools as tools
tools.ignoreAssignmentOperators(module)
tools.removeWxPrefixes(module)


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
tools.ignoreAllOperators(c)

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
c.convertFromPyObject = tools.convertTwoIntegersTemplate('wxPoint')

c.addCppMethod('SIP_PYOBJECT', 'Get', '()', """\
    sipRes = sipBuildResult(&sipIsErr, "(ii)", sipCpp->x, sipCpp->y);
""", briefDoc="""\
    Get() -> (x,y)\n    
    Return the x and y properties as a tuple.""")

# Add sequence protocol methods and other goodies
c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
c.addPyMethod('__repr__', '(self)',            'return "wx.Point"+str(self.Get())')
c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0)')
c.addPyMethod('__reduce__', '(self)',          'return (Point, self.Get())')
c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
c.addPyMethod('__setitem__', '(self, idx, val)',
              """\
              if idx == 0: self.x = val
              elif idx == 1: self.y = val
              else: raise IndexError
              """) 
c.addPyCode('Point.__safe_for_unpickling__ = True')
              
              


#---------------------------------------
# wxSize tweaks
c = module.find('wxSize')

c.addProperty("width GetWidth SetWidth")
c.addProperty("height GetHeight SetHeight")

# take care of the same issues as wxPoint
tools.ignoreAllOperators(c)
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


# wxSize typemap
c.convertFromPyObject = tools.convertTwoIntegersTemplate('wxSize')

c.addCppMethod('SIP_PYOBJECT', 'Get', '()', """\
    sipRes = sipBuildResult(&sipIsErr, "(ii)", sipCpp->GetWidth(), sipCpp->GetHeight());
""", briefDoc="""\
    Get() -> (width, height)\n    
    Return the width and height properties as a tuple.""")

# Add sequence protocol methods and other goodies
c.addPyMethod('__str__', '(self)',             'return str(self.Get())')
c.addPyMethod('__repr__', '(self)',            'return "wx.Size"+str(self.Get())')
c.addPyMethod('__len__', '(self)',             'return len(self.Get())')
c.addPyMethod('__nonzero__', '(self)',         'return self.Get() != (0,0)')
c.addPyMethod('__reduce__', '(self)',          'return (Size, self.Get())')
c.addPyMethod('__getitem__', '(self, idx)',    'return self.Get()[idx]')
c.addPyMethod('__setitem__', '(self, idx, val)',
              """\
              if idx == 0: self.width = val
              elif idx == 1: self.height = val
              else: raise IndexError
              """) 
c.addPyCode('Size.__safe_for_unpickling__ = True')



#---------------------------------------
# wxRect tweaks
c = module.find('wxRect')

# take care of the same issues as wxPoint
tools.ignoreAllOperators(c)
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
tools.ignoreAllOperators(c)
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
