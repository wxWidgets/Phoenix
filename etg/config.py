#---------------------------------------------------------------------------
# Name:        etg/config.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "config"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxConfigBase',
           'wxFileConfig',
           'wxConfigPathChanger',
           'interface_2wx_2config_8h.xml'
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxConfigBase')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()
    c.find('Get').mustHaveApp()
    c.find('Create').mustHaveApp()

    c.abstract = True
    ctor = c.find('wxConfigBase')
    ctor.items.remove(ctor.find('conv'))
    c.find('ReadObject').ignore()

    c.find('Set').transferBack = True      # Python takes ownership of the return value
    c.find('Set.pConfig').transfer = True  # C++ takes ownership of the arg

    for func in c.findAll('Read'):
        if not 'wxString' in func.type:
            func.ignore()
        else:
            func.find('defaultVal').default = 'wxEmptyString'

    c.addCppMethod('long', '_cpp_ReadInt', '(const wxString& key, long defaultVal=0)',  """\
        long rv;
        self->Read(*key, &rv, defaultVal);
        return rv;
        """)
    c.addPyMethod('ReadInt', '(self, key, defaultVal=0)', body="""\
        import six
        rv = self._cpp_ReadInt(key, defaultVal)
        if six.PY2:
            rv = int(rv)
        return rv
        """)

    c.addCppMethod('double', 'ReadFloat', '(const wxString& key, double defaultVal=0.0)', """\
        double rv;
        self->Read(*key, &rv, defaultVal);
        return rv;
        """)
    c.find('ReadBool').ignore()
    c.addCppMethod('bool', 'ReadBool', '(const wxString& key, bool defaultVal=false)', """\
        bool rv;
        self->Read(*key, &rv, defaultVal);
        return rv;
        """)


    c.find('Write').overloads = []
    c.addCppMethod('bool', 'WriteInt', '(const wxString& key, long value)', """\
        return self->Write(*key, value);
        """)
    c.addCppMethod('bool', 'WriteFloat', '(const wxString& key, double value)', """\
        return self->Write(*key, value);
        """)
    c.addCppMethod('bool', 'WriteBool', '(const wxString& key, bool value)', """\
        return self->Write(*key, value);
        """)


    c.find('GetFirstGroup').ignore()
    c.find('GetNextGroup').ignore()
    c.find('GetFirstEntry').ignore()
    c.find('GetNextEntry').ignore()

    c.addCppCode("""\
        static PyObject* _Config_EnumerationHelper(bool flag, wxString& str, long index) {
        wxPyThreadBlocker blocker;
            PyObject* ret = PyTuple_New(3);
            if (ret) {
                PyTuple_SET_ITEM(ret, 0, PyBool_FromLong(flag));
                PyTuple_SET_ITEM(ret, 1, wx2PyString(str));
                PyTuple_SET_ITEM(ret, 2, wxPyInt_FromLong(index));
            }
            return ret;
        }
        """)

    c.addCppMethod('PyObject*', 'GetFirstGroup', '()',
        doc="""\
            GetFirstGroup() -> (more, value, index)\n
            Allows enumerating the subgroups in a config object.  Returns a tuple
            containing a flag indicating if there are more items, the name of the
            current item, and an index to pass to GetNextGroup to fetch the next
            item.""",
        body="""\
            bool     more;
            long     index = 0;
            wxString value;
            more = self->GetFirstGroup(value, index);
            return _Config_EnumerationHelper(more, value, index);
            """)

    c.addCppMethod('PyObject*', 'GetNextGroup', '(long index)',
        doc="""\
            GetNextGroup(long index) -> (more, value, index)\n
            Allows enumerating the subgroups in a config object.  Returns a tuple
            containing a flag indicating if there are more items, the name of the
            current item, and an index to pass to GetNextGroup to fetch the next
            item.""",
        body="""\
            bool more;
            wxString value;
            more = self->GetNextGroup(value, index);
            return _Config_EnumerationHelper(more, value, index);
            """)


    c.addCppMethod('PyObject*', 'GetFirstEntry', '()',
        doc="""\
            GetFirstEntry() -> (more, value, index)\n
            Allows enumerating the entries in the current group in a config
            object.  Returns a tuple containing a flag indicating if there are more
            items, the name of the current item, and an index to pass to
            GetNextEntry to fetch the next item.""",
        body="""\
            bool     more;
            long     index = 0;
            wxString value;
            more = self->GetFirstEntry(value, index);
            return _Config_EnumerationHelper(more, value, index);
            """)

    c.addCppMethod('PyObject*', 'GetNextEntry', '(long index)',
        doc="""\
            GetNextEntry() -> (more, value, index)\n
            Allows enumerating the entries in the current group in a config
            object.  Returns a tuple containing a flag indicating if there are more
            items, the name of the current item, and an index to pass to
            GetNextEntry to fetch the next item.""",
        body="""\
            bool     more;
            wxString value;
            more = self->GetNextEntry(value, index);
            return _Config_EnumerationHelper(more, value, index);
            """)


    #-----------------------------------------------------------------
    c = module.find('wxFileConfig')
    c.mustHaveApp()
    c.addPrivateCopyCtor()
    c.find('wxFileConfig').findOverload('wxInputStream').find('conv').ignore()
    ctor = c.find('wxFileConfig').findOverload('wxString').find('conv').ignore()
    c.find('Save').ignore()
    c.find('GetGlobalFile').ignore()
    c.find('GetLocalFile').ignore()

    c.find('GetFirstGroup').ignore()
    c.find('GetNextGroup').ignore()
    c.find('GetFirstEntry').ignore()
    c.find('GetNextEntry').ignore()

    c.addCppMethod('bool', 'Save', '(wxOutputStream& os)', doc=c.find('Save').briefDoc, body="""\
        #if wxUSE_STREAMS
            return self->Save(*os);
        #else
            wxPyRaiseNotImplemented();
        #endif
        """)

    #-----------------------------------------------------------------
    # In C++ wxConfig is a #define to some other config class. We'll let our
    # backend generator believe that it's a real class with that name. It will
    # end up using the wxConfig #defined in the C++ code, and will actually be
    # whatever is the default config class for the platform.
    wc = etgtools.WigCode("""\
    class wxConfig : wxConfigBase
    {
    public:
        wxConfig(const wxString& appName = wxEmptyString,
                 const wxString& vendorName = wxEmptyString,
                 const wxString& localFilename = wxEmptyString,
                 const wxString& globalFilename = wxEmptyString,
                 long style = wxCONFIG_USE_LOCAL_FILE | wxCONFIG_USE_GLOBAL_FILE);
        ~wxConfig();

        // pure virtuals with implementations here
        const wxString & GetPath() const;
        void SetPath(const wxString & strPath);
        size_t GetNumberOfEntries(bool bRecursive = false) const;
        size_t GetNumberOfGroups(bool bRecursive = false) const;
        bool HasEntry(const wxString & strName) const;
        bool HasGroup(const wxString & strName) const;
        bool Flush(bool bCurrentOnly = false);
        bool RenameEntry(const wxString & oldName, const wxString & newName);
        bool RenameGroup(const wxString & oldName, const wxString & newName);
        bool DeleteAll();
        bool DeleteEntry(const wxString & key, bool bDeleteGroupIfEmpty = true);
        bool DeleteGroup(const wxString & key);

    private:
        wxConfig(const wxConfig&);
    };
    """)
    module.addItem(wc)


    #-----------------------------------------------------------------
    c = module.find('wxConfigPathChanger')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    # context manager methods
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

