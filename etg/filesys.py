#---------------------------------------------------------------------------
# Name:        etg/filesys.py
# Author:      Robin Dunn
#
# Created:     25-Feb-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "filesys"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxFileSystem",
           "wxFSFile",
           "wxFileSystemHandler",
           "wxMemoryFSHandler",
           "wxArchiveFSHandler",
           "wxFilterFSHandler",
           "wxInternetFSHandler",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFileSystem')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()
    c.find('AddHandler.handler').transfer = True
    c.find('RemoveHandler').transferBack = True

    c = module.find('wxFileSystemHandler')
    c.find('GetAnchor').ignore(False)
    c.find('GetLeftLocation').ignore(False)
    c.find('GetProtocol').ignore(False)
    c.find('GetRightLocation').ignore(False)
    c.find('OpenFile').factory = True


    def _fixHandlerClass(klass):
        klass.addItem(etgtools.WigCode("""\
            virtual bool CanOpen(const wxString& location);
            virtual wxFSFile* OpenFile(wxFileSystem& fs, const wxString& location) /Factory/;
            virtual wxString FindFirst(const wxString& spec, int flags = 0);
            virtual wxString FindNext();
            """))


    c = module.find('wxArchiveFSHandler')
    _fixHandlerClass(c)
    c.addPrivateCopyCtor()
    module.addPyCode('ZipFSHandler = wx.deprecated(ArchiveFSHandler, "Use ArchiveFSHandler instead.")')

    c = module.find('wxFSFile')
    c.addPrivateCopyCtor()
    c.find('wxFSFile.stream').keepReference = True

    c = module.find('wxFilterFSHandler')
    _fixHandlerClass(c)
    c.addPrivateCopyCtor()

    c = module.find('wxInternetFSHandler')
    _fixHandlerClass(c)
    c.addPrivateCopyCtor()


    c = module.find('wxMemoryFSHandler')
    _fixHandlerClass(c)
    c.addPrivateCopyCtor()

    # Make some more python-friendly versions of the AddFile methods accepting text or raw data
    c.find('AddFile').findOverload('textdata').ignore()
    c.addCppMethod('void', 'AddFile', '(const wxString& filename, const wxString& textdata)',
        isStatic=True,
        doc="Add a file from text data, which will first be converted to utf-8 encoded bytes.",
        body="""\
            wxScopedCharBuffer buf = textdata->utf8_str();
            wxMemoryFSHandler::AddFile(*filename, (const char*)buf, strlen(buf));
            """)

    c.find('AddFile').findOverload('binarydata').ignore()
    c.addCppMethod('void', 'AddFile', '(const wxString& filename, wxPyBuffer* binarydata)',
        isStatic=True,
        doc="Add a file from raw data in a python buffer compatible object.",
        body="""\
            wxMemoryFSHandler::AddFile(*filename, binarydata->m_ptr, binarydata->m_len);
            """)

    c.find('AddFileWithMimeType').findOverload('textdata').ignore()
    c.addCppMethod('void', 'AddFileWithMimeType',
                   '(const wxString& filename, const wxString& textdata, const wxString& mimetype)',
        isStatic=True,
        doc="Add a file from text data, which will first be converted to utf-8 encoded bytes.",
        body="""\
            wxScopedCharBuffer buf = textdata->utf8_str();
            wxMemoryFSHandler::AddFileWithMimeType(*filename, (const char*)buf, strlen(buf), *mimetype);
            """)

    c.find('AddFileWithMimeType').findOverload('binarydata').ignore()
    c.addCppMethod('void', 'AddFileWithMimeType',
                   '(const wxString& filename, wxPyBuffer* binarydata, const wxString& mimetype)',
        isStatic=True,
        doc="Add a file from raw data in a python buffer compatible object.",
        body="""\
            wxMemoryFSHandler::AddFileWithMimeType(
                    *filename, binarydata->m_ptr, binarydata->m_len, *mimetype);
            """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

