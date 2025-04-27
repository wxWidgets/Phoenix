#---------------------------------------------------------------------------
# Name:        etg/_glcanvas.py
# Author:      Robin Dunn
#
# Created:     3-Nov-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_glcanvas"
NAME      = "_glcanvas"   # Base name of the file to generate to for this script
DOCSTRING = """\
These classes enable viewing and interacting with an OpenGL context in a wx.Window.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxGLAttribsBase',
           'wxGLAttributes',
           'wxGLContextAttrs',
           'wxGLContext',
           'wxGLCanvas',
          ]


# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "gl" library in a multi-lib build.
INCLUDES = [ ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from the build scripts to get a list of
# sources and/or additional dependencies when building this extension module.
ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
DEPENDS = tools.getNonEtgFiles(INCLUDES)
OTHERDEPS = [  ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)
    module.check4unittest = False

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wxPython/wxpy_api.h>')
    module.addImport('_core')
    module.addPyCode('import wx', order=10)
    module.addInclude(INCLUDES)


    #-----------------------------------------------------------------

    module.addHeaderCode('#include <wx/glcanvas.h>')

    tools.generateStubs('wxUSE_GLCANVAS', module,
                        extraHdrCode='#define wxGLCanvasName wxT("GLCanvas")\n',
                        typeValMap={'wxGLAttributes &': '*this',
                                    'wxGLContextAttrs &': '*this',
                                    })

    c = module.find('wxGLContext')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    c.addPrivateCopyCtor()


    c = module.find('wxGLAttribsBase')
    assert isinstance(c, etgtools.ClassDef)
    c.find('GetGLAttrs').ignore()

    c = module.find('wxGLCanvas')
    tools.fixWindowClass(c)

    # We already have a MappedType for wxArrayInt, so just tweak the
    # interfaces to use that instead of a const int pointer.
    c.find('wxGLCanvas').findOverload('const int *attribList').ignore()
    m = c.addCppCtor_sip(
        argsString="""(
             wxWindow* parent /TransferThis/,
             wxWindowID id=wxID_ANY,
             wxArrayInt* attribList=NULL,
             const wxPoint& pos=wxDefaultPosition,
             const wxSize& size=wxDefaultSize,
             long style=0,
             const wxString& name="GLCanvas",
             const wxPalette& palette=wxNullPalette)
             """,
        cppSignature="""(
             wxWindow* parent, wxWindowID id=wxID_ANY, const int* attribList=NULL,
             const wxPoint& pos=wxDefaultPosition, const wxSize& size=wxDefaultSize,
             long style=0, const wxString& name="GLCanvas",
             const wxPalette& palette=wxNullPalette)""",
        pyArgsString="(parent, id=wx.ID_ANY, attribList=None, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name='GLCanvas', palette=wx.NullPalette)",
        body="""\
            const int* attribPtr = NULL;
            if (attribList) {
                attribList->push_back(0); // ensure it is zero-terminated
                attribPtr = &attribList->front();
            }
            sipCpp = new sipwxGLCanvas(parent, id, attribPtr, *pos, *size, style, *name, *palette);
            """,
        noDerivedCtor=False,
        )


    m = c.find('IsDisplaySupported').findOverload('attribList')
    m.find('attribList').type = 'wxArrayInt*'
    m.setCppCode_sip("""\
        const int* attribPtr = NULL;
        if (attribList) {
            attribList->push_back(0); // ensure it is zero-terminated
            attribPtr = &attribList->front();
        }
        sipRes = wxGLCanvas::IsDisplaySupported(attribPtr);
        """)

    c.find('CreateSurface').setCppCode("""\
        #if wxUSE_GLCANVAS_EGL
            return self->CreateSurface();
        #else
            wxPyRaiseNotImplemented();
            return false;
        #endif
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
