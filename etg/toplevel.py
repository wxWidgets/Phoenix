#---------------------------------------------------------------------------
# Name:        etg/toplevel.py
# Author:      Robin Dunn
#
# Created:     4-Dec-2010
# Copyright:   (c) 2010-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "toplevel"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxTopLevelWindow' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING,
                                check4unittest=False)
    etgtools.parseDoxyXML(module, ITEMS)
    module.check4unittest = False

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxTopLevelWindow')
    assert isinstance(c, etgtools.ClassDef)
    module.addGlobalStr('wxFrameNameStr', c)

    c.find('wxTopLevelWindow.title').default = 'wxEmptyString'
    c.find('Create.title').default = 'wxEmptyString'

    c.find('IsUsingNativeDecorations').ignore()
    c.find('UseNativeDecorations').ignore()
    c.find('UseNativeDecorationsByDefault').ignore()
    c.find('MSWGetSystemMenu').ignore() # what is this?

    c.addCppMethod('void', 'MacSetMetalAppearance', '(bool on)', """\
        int style = self->GetExtraStyle();
        if ( on )
            style |= wxFRAME_EX_METAL;
        else
            style &= ~wxFRAME_EX_METAL;
        self->SetExtraStyle(style);
        """)

    c.addCppMethod('bool', 'MacGetMetalAppearance', '()', """\
        return self->GetExtraStyle() & wxFRAME_EX_METAL;
        """)

    c.addCppMethod('bool', 'MacGetUnifiedAppearance', '()', 'return true;')

    c.addCppMethod('void*', 'MacGetTopLevelWindowRef', '()', """\
        #ifdef __WXMAC__
            return (void*)(self->MacGetTopLevelWindowRef());
        #else
            return 0;
        #endif
        """)

    c.find('GeometrySerializer').abstract = True

    c.addProperty('DefaultItem GetDefaultItem SetDefaultItem')
    c.addProperty('Icon GetIcon SetIcon')
    c.addProperty('Title GetTitle SetTitle')
    c.addProperty('TmpDefaultItem GetTmpDefaultItem SetTmpDefaultItem')
    c.addProperty('OSXModified OSXIsModified OSXSetModified')
    c.addProperty('MacMetalAppearance MacGetMetalAppearance MacSetMetalAppearance')

    tools.fixTopLevelWindowClass(c)
    c.find('ShouldPreventAppExit').isVirtual = True

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

