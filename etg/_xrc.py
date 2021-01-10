#---------------------------------------------------------------------------
# Name:        etg/_xrc.py
# Author:      Robin Dunn
#
# Created:     28-Nov-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
from etgtools import ClassDef, MethodDef, ParamDef

PACKAGE   = "wx"
MODULE    = "_xrc"
NAME      = "_xrc"   # Base name of the file to generate to for this script
DOCSTRING = """\
The classes in this module enable loading widgets and layout from XML.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxXmlResource',
           'wxXmlResourceHandler',
           ]


# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "xrc" library in a multi-lib build.
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
    module.addImport('_xml')
    module.addPyCode('''\
    import wx
    ID_NONE = wx.ID_NONE  # Needed for some parameter defaults in this module
    ''', order=10)
    module.addInclude(INCLUDES)

    module.addInitializerCode("""\
        wxXmlInitResourceModule();
        wxXmlResource::Get()->InitAllHandlers();
        """)

    module.addHeaderCode('#include <wx/animate.h>')
    module.addHeaderCode('#include <wx/xrc/xmlres.h>')
    module.addHeaderCode('#include <wx/fs_mem.h>')
    module.addHeaderCode('#include "wxpybuffer.h"')

    module.insertItem(0, etgtools.WigCode("""\
        // forward declarations
        class wxAnimation;
        class wxAnimationCtrl;
        """))

    #-----------------------------------------------------------------

    c = module.find('wxXmlResource')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()

    # Add a bit of code to the ctors to call InitAllHandlers(), for
    # compatibility with Classic
    for ctor in c.find('wxXmlResource').all():
        template = """\
        Py_BEGIN_ALLOW_THREADS
        sipCpp = new sipwxXmlResource({args});
        sipCpp->InitAllHandlers();
        Py_END_ALLOW_THREADS
        """
        if 'filemask' in ctor.argsString:
            args = '*filemask,flags,*domain'
        else:
            args = 'flags,*domain'
        ctor.setCppCode_sip(template.format(args=args))


    c.addPublic()
    c.addCppMethod('bool', 'LoadFromBuffer', '(wxPyBuffer* data)',
        doc="Load the resource from a bytes string or other data buffer compatible object.",
        #protection='public',
        body="""\
            static int s_memFileIdx = 0;

            // Check for memory FS. If not present, load the handler:
            wxMemoryFSHandler::AddFile(wxT("XRC_resource/dummy_file"),
                                       wxT("dummy data"));
            wxFileSystem fsys;
            wxFSFile *f = fsys.OpenFile(wxT("memory:XRC_resource/dummy_file"));
            wxMemoryFSHandler::RemoveFile(wxT("XRC_resource/dummy_file"));
            if (f)
                delete f;
            else
                wxFileSystem::AddHandler(new wxMemoryFSHandler);

            // Now put the resource data into the memory FS
            wxString filename(wxT("XRC_resource/data_string_"));
            filename << s_memFileIdx;
            s_memFileIdx += 1;
            wxMemoryFSHandler::AddFile(filename, data->m_ptr, data->m_len);

            // Load the "file" into the resource object
            bool retval = self->Load(wxT("memory:") + filename );
            return retval;
            """)
    c.addPyCode("XmlResource.LoadFromString = wx.deprecated(XmlResource.LoadFromBuffer, 'Use LoadFromBuffer instead')")

    c.find('AddHandler.handler').transfer = True
    c.find('InsertHandler.handler').transfer = True
    c.find('Set.res').transfer = True
    c.find('Set').transferBack = True
    c.find('AddSubclassFactory.factory').transfer = True


    #-----------------------------------------------------------------
    c = module.find('wxXmlResourceHandler')

    # un-ignore all the protected methods
    for item in c.allItems():
        if isinstance(item, etgtools.MethodDef):
            item.ignore(False)

    c.find('DoCreateResource').factory = True

    # TODO: It looks like there may be a bug in wx here.
    # Just ignore it for now.
    c.find('GetFilePath').ignore()

    c.find('GetAnimation.ctrl').type = 'wxAnimationCtrl *'

    #-----------------------------------------------------------------
    module.addPyFunction('EmptyXmlResource', '(flags=XRC_USE_LOCALE, domain="")',
        deprecated="Use :class:`xrc.XmlResource` instead",
        doc='A compatibility wrapper for the XmlResource(flags, domain) constructor',
        body='return XmlResource(flags, domain)')

    module.addPyFunction('XRCID', '(str_id, value_if_not_found=wx.ID_NONE)',
        doc='Returns a numeric ID that is equivalent to the string ID used in an XML resource.',
        body='return XmlResource.GetXRCID(str_id, value_if_not_found)')

    module.addPyFunction('XRCCTRL', '(window, str_id, *ignoreargs)',
        doc='Returns the child window associated with the string ID in an XML resource.',
        body='return window.FindWindow(XRCID(str_id))')



    cls = ClassDef(name='wxXmlSubclassFactory',
        briefDoc="",
        items=[
            MethodDef(name='wxXmlSubclassFactory', isCtor=True),
            MethodDef(name='~wxXmlSubclassFactory', isDtor=True),
            MethodDef(name='Create', type='wxObject*',
                isVirtual=True, isPureVirtual=True, factory=True,
                items=[ParamDef(type='const wxString&', name='className')])
            ])
    module.addItem(cls)



    module.addPyCode("""\
        # Create a factory for handling the subclass property of XRC's
        # object tag.  This factory will search for the specified
        # package.module.class and will try to instantiate it for XRC's
        # use.  The class must support instantiation with no parameters and
        # delayed creation of the UI widget (aka 2-phase create).

        def _my_import(name):
            try:
                mod = __import__(name)
            except ImportError:
                import traceback
                print(traceback.format_exc())
                raise
            components = name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod

        class XmlSubclassFactory_Python(XmlSubclassFactory):
            def __init__(self):
                XmlSubclassFactory.__init__(self)

            def Create(self, className):
                assert className.find('.') != -1, "Module name must be specified!"
                mname = className[:className.rfind('.')]
                cname = className[className.rfind('.')+1:]
                module = _my_import(mname)
                klass = getattr(module, cname)
                inst = klass()
                return inst

        XmlResource.AddSubclassFactory(XmlSubclassFactory_Python())
        """)

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
