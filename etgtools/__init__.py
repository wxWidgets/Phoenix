#---------------------------------------------------------------------------
# Name:        etgtools/__init__.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

"""
Classes and tools for describing the public API of wxWidgets, parsing
them from the Doxygen XML, and producing wrapper code from them.
"""

import sys, os
# Mac Python actually has a buildtools module, so we need
# to make sure ours is picked up when we're not run from the
# Phoenix root dir.
sys.path.insert(0, os.path.abspath(os.path.split(__file__)[0]+'/..'))

from buildtools.config import Config
from .extractors import *

#---------------------------------------------------------------------------
cfg = Config(noWxConfig=True)

phoenixRoot = cfg.ROOT_DIR
XMLSRC = cfg.DOXY_XML_DIR

class DoxyXMLError(Exception):
    pass

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

    def _classToDoxyName(name, attempts, base='class'):
        import string
        filename = base
        for c in name:
            if c in string.ascii_uppercase:
                filename += '_' + c.lower()
            else:
                filename += c
        filename = os.path.join(XMLSRC, filename) + '.xml'
        attempts.append(filename)
        return filename

    def _includeToDoxyName(name):
        name = os.path.basename(name)
        name = name.replace('.h', '_8h')
        pathname = os.path.join(XMLSRC, name) + '.xml'
        if os.path.exists(pathname):
            return pathname, name + '.xml'
        else:
            name = 'interface_2wx_2' + name
            return os.path.join(XMLSRC, name) + '.xml', name + '.xml'

    for class_or_filename in class_or_filename_list:
        attempts = []
        pathname = _classToDoxyName(class_or_filename, attempts)

        if not os.path.exists(pathname):
            pathname = _classToDoxyName(class_or_filename, attempts, 'struct')
            if not os.path.exists(pathname):
                pathname = os.path.join(XMLSRC, class_or_filename)
                attempts.append(pathname)
                if not os.path.exists(pathname):
                    msg = "Unable to find xml file for ITEM: %s" % class_or_filename
                    print(msg)
                    print("Tried: %s" % ('\n       '.join(attempts)))
                    raise DoxyXMLError(msg)

        if verbose():
            print("Loading %s..." % pathname)
        _filesparsed.add(pathname)

        root = et.parse(pathname).getroot()
        for element in root:
            # extract and add top-level elements from the XML document
            item = module.addElement(element)

            # Also automatically parse the XML for the include file to get related
            # typedefs, functions, enums, etc.
            # Make sure though, that for interface files we only parse the one
            # that belongs to this class. Otherwise, enums, etc. will be defined
            # in multiple places.
            xmlname = class_or_filename.replace('wx', '').lower()

            if hasattr(item, 'includes'):
                for inc in item.includes:
                    pathname, name = _includeToDoxyName(inc)
                    if os.path.exists(pathname) \
                       and pathname not in _filesparsed \
                       and ("interface" not in name or xmlname in name) \
                       and name not in class_or_filename_list:
                        class_or_filename_list.append(name)

        _filesparsed.clear()

    module.parseCompleted()

#---------------------------------------------------------------------------


#---------------------------------------------------------------------------


