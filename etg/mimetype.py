#---------------------------------------------------------------------------
# Name:        etg/mimetype.py
# Author:      Robin Dunn
#
# Created:     16-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "mimetype"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxFileType",
           "wxFileTypeInfo",
           "wxMimeTypesManager",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFileType')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.addPublic()

    # Change semantics for some methods to return values instead of using
    # output parameters. This is for Classic compatibility as well as being a
    # bit more pythonic.
    c.find('GetDescription').ignore()
    c.addCppMethod('wxString', 'GetDescription', '()',
        doc="""\
            Returns a brief description for this file type: for example, "text document" for
            the "text/plain" MIME type.""",
        body="""\
            wxString rv;
            self->GetDescription(&rv);
            return new wxString(rv);
            """)

    c.find('GetExtensions').ignore()
    c.addCppMethod('wxArrayString*', 'GetExtensions', '()',
        factory=True,
        doc="""\
            Returns all extensions associated with this file type: for
            example, it may contain the following two elements for the MIME
            type "text/html" (notice the absence of the leading dot): "html"
            and "htm".

            This function is not implemented on Windows, there is no (efficient)
            way to retrieve associated extensions from the given MIME type on
            this platform. """,
        body="""\
            wxArrayString* arr = new wxArrayString;
            self->GetExtensions(*arr); return arr;
            """)

    c.find('GetMimeType').ignore()
    c.addCppMethod('wxString', 'GetMimeType', '()',
        doc='Returns full MIME type specification for this file type: for example, "text/plain".',
        body="""\
            wxString rv;
            self->GetMimeType(&rv);
            return new wxString(rv);
            """)

    c.find('GetMimeTypes').ignore()
    c.addCppMethod('wxArrayString*', 'GetMimeTypes', '()',
        factory=True,
        doc="""\
            Same as GetMimeType but returns a list of types.  This will usually contain
            only one item, but sometimes, such as on Unix with KDE more than one type
            if there are differences between KDE< mailcap and mime.types.""",
        body="""\
            wxArrayString* arr = new wxArrayString;
            self->GetMimeTypes(*arr);
            return arr;
            """)


    c.find('GetIcon').ignore()
    c.addCppMethod('wxIcon*', 'GetIcon', '()',
        factory = True,
        doc="Return the icon associated with this mime type, if any.",
        body="""\
            wxIconLocation loc;
            if (self->GetIcon(&loc))
                return new wxIcon(loc);
            else
                return NULL;
            """)
    c.addCppMethod('wxIconLocation*', 'GetIconLocation', '()',
        factory = True,
        doc="Returns a wx.IconLocation that can be used to fetch the icon for this mime type.",
        body="""\
            wxIconLocation loc;
            if (self->GetIcon(&loc))
                return new wxIconLocation(loc);
            else
                return NULL;
            """)


    for m in c.find('GetOpenCommand').all():
        m.ignore()
    c.addCppMethod('wxString', 'GetOpenCommand', '(const wxFileType::MessageParameters& params)',
        doc="""\
            Returns the command which must be executed (see wx.Execute()) in order
            to open the file of the given type. The name of the file as well as
            any other parameters is retrieved from MessageParameters() class.""",
        body="""\
            wxString rv;
            self->GetOpenCommand(&rv, *params);
            return new wxString(rv);
            """)
    c.addCppMethod('wxString', 'GetOpenCommand', '(const wxString& filename)',
        doc="""\
            Returns the command which should be used to open the given
            filename. An empty string is returned to indicate that an error
            occurred (typically meaning that there is no standard way to open
            this kind of files).""",
        body="""\
            return new wxString( self->GetOpenCommand(*filename) );
            """)


    c.find('GetPrintCommand').ignore()
    c.addCppMethod('wxString', 'GetPrintCommand', '(const wxFileType::MessageParameters& params)',
        doc="""\
            Returns the command which must be executed (see wxExecute()) in order to
            print the file of the given type. The name of the file is retrieved from
            the MessageParameters class.""",
        body="""\
            wxString rv;
            self->GetPrintCommand(&rv, *params);
            return new wxString(rv);
            """)

    m = c.find('GetAllCommands')
    m.find('verbs').out = True
    m.find('commands').out = True
    m.type = 'void'
    m.briefDoc = \
        "Returns a tuple containing the `verbs` and `commands` arrays, " \
        "corresponding for the registered information for this mime type."



    c.addCppMethod('PyObject*', 'GetIconInfo', '()',
        doc="""\
            Returns a tuple containing the Icon for this file type, the file where the
            icon is found, and the index of the image in that file, if applicable.
            """,
        body="""\
            wxIconLocation loc;
            if (self->GetIcon(&loc)) {
                wxString iconFile = loc.GetFileName();
                int iconIndex     = -1;
            #ifdef __WXMSW__
                iconIndex = loc.GetIndex();
            #endif
                // Make a tuple and put the values in it
                wxPyThreadBlocker blocker;
                PyObject* tuple = PyTuple_New(3);
                PyTuple_SetItem(tuple, 0,
                    wxPyConstructObject(new wxIcon(loc), wxT("wxIcon"), true));
                PyTuple_SetItem(tuple, 1, wx2PyString(iconFile));
                PyTuple_SetItem(tuple, 2, wxPyInt_FromLong(iconIndex));
                return tuple;
            }
            else
                RETURN_NONE();
            """)



    #-----------------------------------------------------------------
    c = module.find('wxFileTypeInfo')

    # Ignore the variadic nature of this ctor
    ctor = c.find('wxFileTypeInfo').findOverload('extension')
    ctor.items[-1].ignore()
    ctor.setCppCode("""\
        wxFileTypeInfo* fti = new wxFileTypeInfo(*mimeType);
        fti->SetOpenCommand(*openCmd);
        fti->SetPrintCommand(*printCmd);
        fti->SetDescription(*description);
        fti->AddExtension(*extension);
        return fti;
        """)
    ctor.useDerivedName = False


    #-----------------------------------------------------------------
    c = module.find('wxMimeTypesManager')
    c.addPrivateCopyCtor()

    c.find('Associate').factory = True

    c.find('EnumAllFileTypes').ignore()
    c.addCppMethod('wxArrayString*', 'EnumAllFileTypes', '()',
        factory=True,
        doc="Returns a list of all known file types.",
        body="""\
            wxArrayString* arr = new wxArrayString;
            self->EnumAllFileTypes(*arr);
            return arr;
            """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

