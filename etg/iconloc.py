#---------------------------------------------------------------------------
# Name:        etg/iconloc.py
# Author:      Robin Dunn
#
# Created:     14-Nov-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "iconloc"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxIconLocation', ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxIconLocation')
    assert isinstance(c, etgtools.ClassDef)

    c.addCppCtor('()', "return new wxIconLocation;")

    c.addCppCtor('(const wxString* filename, int num = 0)', """\
        #ifdef __WXMSW__
            return new wxIconLocation(*filename, num);
        #else
            return new wxIconLocation(*filename);
        #endif
        """)

    c.addCppMethod('int', '__nonzero__', '()', "return self->IsOk();")
    c.addCppMethod('int', '__bool__', '()', "return self->IsOk();")

    c.addCppMethod('int', 'GetIndex', '()', """\
        #ifdef __WXMSW__
            return self->GetIndex();
        #else
            return -1;
        #endif
        """)

    c.addCppMethod('void', 'SetIndex', '(int num)', """\
        #ifdef __WXMSW__
            self->SetIndex(num);
        #endif
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

