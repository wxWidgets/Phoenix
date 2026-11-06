#---------------------------------------------------------------------------
# Name:        etg/statbox.py
# Author:      Robin Dunn
#
# Created:     29-Oct-2011
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import MethodDef, ParamDef


PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "statbox"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxStaticBox",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxStaticBox')
    assert isinstance(c, etgtools.ClassDef)
    c.find('wxStaticBox.label').default = 'wxEmptyString'
    c.find('Create.label').default = 'wxEmptyString'
    tools.fixWindowClass(c)

    # The window-label overloads only exist on some platforms (not wxOSX), so
    # they are created in two steps and raise NotImplementedError elsewhere.
    # wx.HAS_WINDOW_LABEL_IN_STATIC_BOX tells which, as the docs suggest.
    module.addHeaderCode("""\
        #ifdef wxHAS_WINDOW_LABEL_IN_STATIC_BOX
        #define wxPyHAS_WINDOW_LABEL_IN_STATIC_BOX 1
        #else
        #define wxPyHAS_WINDOW_LABEL_IN_STATIC_BOX 0
        #endif
        """)
    module.addItem(etgtools.DefineDef(name='wxPyHAS_WINDOW_LABEL_IN_STATIC_BOX',
                                      pyName='HAS_WINDOW_LABEL_IN_STATIC_BOX',
                                      value='1', forcedInt=True))

    # fixWindowClass gave id a default, but label has none
    for name in ['wxStaticBox', 'Create']:
        c.find(name).findOverload('wxWindow *label').find('id').default = ''

    ctor = c.find('wxStaticBox').findOverload('wxWindow *label')
    ctor.noDerivedCtor = True
    ctor.setCppCode_sip("""\
        #ifdef wxHAS_WINDOW_LABEL_IN_STATIC_BOX
            sipCpp = new sipwxStaticBox();
            sipCpp->Create(parent, id, label, *pos, *size, style, *name);
        #else
            wxPyRaiseNotImplemented();
            sipIsErr = 1;
        #endif
        """)
    c.find('Create').findOverload('wxWindow *label').setCppCode_sip("""\
        #ifdef wxHAS_WINDOW_LABEL_IN_STATIC_BOX
            sipRes = sipCpp->Create(parent, id, label, *pos, *size, style, *name);
        #else
            wxPyRaiseNotImplemented();
            sipIsErr = 1;
        #endif
        """)


    # This is intentionally not documented, but I think it would be handy to
    # use from wxPython.
    meth = MethodDef(
        name='GetBordersForSizer', isConst=True, isVirtual=True, type='void', protection='public',
        briefDoc="Returns extra space that may be needed for borders within a StaticBox.",
        items=[ParamDef(name='borderTop', type='int*', out=True),
               ParamDef(name='borderOther', type='int*', out=True),
               ])
    c.addItem(meth)

    module.addGlobalStr('wxStaticBoxNameStr', c)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

