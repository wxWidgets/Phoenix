#---------------------------------------------------------------------------
# Name:        etg/config.py
# Author:      Kevin Ollivier
#
# Created:     10-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
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
ITEMS  = [ 'wxConfigBase', 'wxFileConfig', ]
    
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
            
    c.addCppMethod('long', 'ReadInt', '(const wxString& key, long defaultVal = 0)', """
        long rv;
        self->Read(*key, &rv, defaultVal);
        return rv;
    """)
    c.addCppMethod('double', 'ReadFloat', '(const wxString& key, double defaultVal = 0.0)', """
        double rv;
        self->Read(*key, &rv, defaultVal);
        return rv;
    """)
    c.addCppMethod('bool', 'ReadBool', '(const wxString& key, bool defaultVal = false)', """
        bool rv;
        self->Read(*key, &rv, defaultVal);
        return rv;
    """)

    
    c.find('Write').overloads = []
    c.addCppMethod('bool', 'WriteInt', '(const wxString& key, long value)', """
        return self->Write(*key, value);
    """)
    c.addCppMethod('bool', 'WriteFloat', '(const wxString& key, double value)', """
        return self->Write(*key, value);
    """)
    c.addCppMethod('bool', 'WriteBool', '(const wxString& key, bool value)', """
        return self->Write(*key, value);
    """)
    
    
    
    c = module.find('wxFileConfig')
    c.addPrivateCopyCtor()
    c.find('wxFileConfig').findOverload('wxInputStream').ignore()
    ctor = c.find('wxFileConfig').findOverload('wxString')
    ctor.items.remove(ctor.find('conv'))
    ctor = c.find('Save').ignore()
    c.find('GetGlobalFile').ignore()
    c.find('GetLocalFile').ignore()
    

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
        bool GetFirstEntry(wxString & str, long & index) const;
        bool GetFirstGroup(wxString & str, long & index) const;
        bool GetNextEntry(wxString & str, long & index) const;
        bool GetNextGroup(wxString & str, long & index) const;
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
    tools.doCommonTweaks(module)
    tools.addGetterSetterProps(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

