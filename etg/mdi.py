#---------------------------------------------------------------------------
# Name:        etg/mdi.py
# Author:      Robin Dunn
#
# Created:     05-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "mdi"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxMDIClientWindow",
           "wxMDIParentFrame",
           "wxMDIChildFrame",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # Let the generator know about these intermediate classes even though they
    # are undocumented. wxTDIChildFrame is used elsewhere in the class hierarchy
    # so it needs to be available.
    module.insertItemBefore(module.find('wxMDIClientWindow'), etgtools.WigCode("""\
class wxMDIChildFrameBase : wxFrame
{
public:
    wxMDIChildFrameBase();
    virtual void Activate() = 0;
    wxMDIParentFrame *GetMDIParent() const;
    virtual bool IsTopLevel() const;
};

class wxTDIChildFrame : wxMDIChildFrameBase /Abstract/
{
public:
};
    """))

    c = module.find('wxMDIClientWindow')
    assert isinstance(c, etgtools.ClassDef)
    tools.fixWindowClass(c)
    c.find('CreateClient').isVirtual = True

    c = module.find('wxMDIParentFrame')
    tools.fixTopLevelWindowClass(c)
    c.find('OnCreateClient').isVirtual = True

    m = c.find('GetClientWindow')
    assert isinstance(m, etgtools.MethodDef)
    m.type = 'wxMDIClientWindow *'
    m.setCppCode("return static_cast<wxMDIClientWindow*>(self->GetClientWindow());")

    c = module.find('wxMDIChildFrame')
    c.bases = ['wxMDIChildFrameBase']
    tools.fixTopLevelWindowClass(c)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

