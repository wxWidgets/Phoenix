#---------------------------------------------------------------------------
# Name:        etgtools/__init__.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Classes and tools for describing the public API of wxWidgets, parsing
them from the Doxygen XML, and producing wrapper code from them.
"""

import sys, os
from extractors import *

#---------------------------------------------------------------------------

phoenixRoot = os.path.abspath(os.path.split(__file__)[0]+'/..')
xmlsrcbase = 'docs/doxygen/out/xml'
WXWIN = os.environ.get('WXWIN')
if not WXWIN:
    for rel in ['../wxWidgets', '..']:
        path = os.path.join(phoenixRoot, rel, xmlsrcbase)
        if path and os.path.exists(path):
            WXWIN = os.path.abspath(os.path.join(phoenixRoot, rel))
            break
if WXWIN:
    XMLSRC = os.path.join(WXWIN, xmlsrcbase)
assert WXWIN and os.path.exists(XMLSRC), "Unable to locate Doxygen XML files"


#---------------------------------------------------------------------------

_filesparsed = set()

def parseDoxyXML(module, class_or_filename_list):
    """
    Parse a list of Doxygen XML files and add the item(s) found there to the
    ModuleDef object.
    
    If a name in the list a wx class name then the Doxygen XML filename is
    calculated from that name, otherwise it is treated as a filename in the
    Doxygen XML output folder.
    """
    
    def _classToDoxyName(name):
        import string
        filename = 'class'
        for c in name:
            if c in string.ascii_uppercase:
                filename += '_' + c.lower()
            else:
                filename += c                
        return os.path.join(XMLSRC, filename) + '.xml'
    
    def _includeToDoxyName(name):
        name = os.path.basename(name)
        name = name.replace('.h', '_8h')
        return os.path.join(XMLSRC, name) + '.xml', name + '.xml'
        
    for class_or_filename in class_or_filename_list:
        pathname = _classToDoxyName(class_or_filename)
        if not os.path.exists(pathname):
            pathname = os.path.join(XMLSRC, class_or_filename)
        if verbose():
            print "Loading %s..." % pathname
        _filesparsed.add(pathname)
        
        root = et.parse(pathname).getroot()
        for element in root:
            # extract and add top-level elements from the XML document
            item = module.addElement(element)
            
            # Also automatically parse the XML for the include file to get related
            # typedefs, functions, enums, etc.
            if hasattr(item, 'includes'):
                for inc in item.includes:
                    pathname, name = _includeToDoxyName(inc)
                    if os.path.exists(pathname) \
                       and pathname not in _filesparsed \
                       and name not in class_or_filename_list:
                        class_or_filename_list.append(name) 

        _filesparsed.clear()

#---------------------------------------------------------------------------
        
def getWrapperGenerator():
    """
    A simple factory function to create a wrapper generator class of the desired type.
    """
    if '--dump' in sys.argv:
        import generators
        gClass = generators.DumpWrapperGenerator
    elif '--swig' in sys.argv:
        import swig_generator
        gClass = swig_generator.SwigWrapperGenerator
    elif '--sip' in sys.argv:
        import sip_generator
        gClass = sip_generator.SipWrapperGenerator
    else:
        # The default is sip, at least for now...
        import sip_generator
        gClass = sip_generator.SipWrapperGenerator
    
    return gClass()

#---------------------------------------------------------------------------

def getDocsGenerator():
    import generators    
    g = generators.StubbedDocsGenerator()
    return g

#---------------------------------------------------------------------------
        
        
