#---------------------------------------------------------------------------
# Name:        etg/filesys.py
# Author:      Robin Dunn
#
# Created:     25-Feb-2012
# Copyright:   (c) 2013 by Total Control Software
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
    c.find('AddHandler.handler').transfer = True
    c.find('RemoveHandler').transferBack = True

    c = module.find('wxFileSystemHandler')
    c.find('GetAnchor').ignore(False)
    c.find('GetLeftLocation').ignore(False)
    c.find('GetProtocol').ignore(False)
    c.find('GetRightLocation').ignore(False)


    def _fixHandlerClass(klass):
        klass.addItem(etgtools.WigCode("""\
            virtual bool CanOpen(const wxString& location);
            virtual wxFSFile* OpenFile(wxFileSystem& fs, const wxString& location);
            """))


    c = module.find('wxArchiveFSHandler')
    c.addPrivateCopyCtor();
    module.addPyCode('ZipFSHandler = wx.deprecated(ArchiveFSHandler, "Use ArchiveFSHandler instead.")')
    _fixHandlerClass(c)
    
    c = module.find('wxFSFile')
    c.addPrivateCopyCtor();
    _fixHandlerClass(c)
    
    c = module.find('wxFilterFSHandler')
    c.addPrivateCopyCtor();
    _fixHandlerClass(c)
    
    c = module.find('wxInternetFSHandler')
    c.addPrivateCopyCtor();
    _fixHandlerClass(c)
    
    c = module.find('wxMemoryFSHandler')
    c.addPrivateCopyCtor();
    _fixHandlerClass(c)

    
    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

