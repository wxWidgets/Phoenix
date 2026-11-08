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
from textwrap import dedent

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

    # The members of GeometryStore are private in the interface header, so
    # declare them here. As with GridCellEditor.EndEdit, the Restore methods
    # return the value, or None if it isn't found, instead of using an output
    # parameter.
    gs = c.find('GeometryStore')
    wig = etgtools.WigCode("""\
        GeometryStore();
        virtual ~GeometryStore();

        virtual bool SaveValue(const wxString& name, int value) = 0;
        %Docstring
            SaveValue(name, value) -> bool

            Save a single field with the given value. Returning ``False``
            makes SaveGeometry() fail.
        %End

        virtual bool SaveString(const wxString& name, const wxString& value);
        %Docstring
            SaveString(name, value) -> bool

            Save a single field with the given string value. This is only
            used with the Wayland XDG session management protocol.
        %End

        virtual SIP_PYOBJECT RestoreValue(const wxString& name) const = 0
            [bool (const wxString& name, int* value)];
        %Docstring
            RestoreValue(name) -> int | None

            Return the value of a single field, or ``None`` if it wasn't found.
        %End
        %MethodCode
            int value;
            bool rv;
            Py_BEGIN_ALLOW_THREADS
            rv = sipCpp->RestoreValue(*name, &value);
            Py_END_ALLOW_THREADS
            if (rv)
                sipRes = PyLong_FromLong(value);
            else {
                Py_INCREF(Py_None);
                sipRes = Py_None;
            }
        %End
        %VirtualCatcherCode
            PyObject* result = sipCallMethod(&sipIsErr, sipMethod, "N",
                                             new wxString(name), sipType_wxString, NULL);
            sipRes = false;
            if (result && result != Py_None) {
                long v = PyLong_AsLong(result);
                if (PyErr_Occurred())
                    sipIsErr = 1;
                else {
                    *value = (int)v;
                    sipRes = true;
                }
            }
            Py_XDECREF(result);
            if (sipIsErr)
                PyErr_Print();
        %End

        virtual SIP_PYOBJECT RestoreString(const wxString& name) const
            [bool (const wxString& name, wxString* value)];
        %Docstring
            RestoreString(name) -> str | None

            Return the value of a single string field, or ``None`` if it wasn't
            found. This is only used with the Wayland XDG session management
            protocol.
        %End
        %MethodCode
            wxString value;
            bool rv;
            Py_BEGIN_ALLOW_THREADS
            rv = sipSelfWasArg
                ? sipCpp->wxTopLevelWindow::GeometryStore::RestoreString(*name, &value)
                : sipCpp->RestoreString(*name, &value);
            Py_END_ALLOW_THREADS
            if (rv)
                sipRes = wx2PyString(value);
            else {
                Py_INCREF(Py_None);
                sipRes = Py_None;
            }
        %End
        %VirtualCatcherCode
            PyObject* result = sipCallMethod(&sipIsErr, sipMethod, "N",
                                             new wxString(name), sipType_wxString, NULL);
            sipRes = false;
            if (result && result != Py_None) {
                *value = Py2wxString(result);
                if (PyErr_Occurred())
                    sipIsErr = 1;
                else
                    sipRes = true;
            }
            Py_XDECREF(result);
            if (sipIsErr)
                PyErr_Print();
        %End
        """)
    wig.piCode = dedent("""\
        def __init__(self) -> None: ...
        def SaveValue(self, name: str, value: int) -> bool: ...
        def SaveString(self, name: str, value: str) -> bool: ...
        def RestoreValue(self, name: str) -> Optional[int]: ...
        def RestoreString(self, name: str) -> Optional[str]: ...
        """)
    gs.addItem(wig)

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

