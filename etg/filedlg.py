#---------------------------------------------------------------------------
# Name:        etg/filedlg.py
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
NAME      = "filedlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ 'wxFileDialog' ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxFileDialog')
    isinstance(c, etgtools.ClassDef)
    module.addGlobalStr('wxFileDialogNameStr', c)
    module.find('wxFileSelectorDefaultWildcardStr').ignore()


    # TODO: add this back. We'll need a way to pass it a callable that can be
    # called from a C ExtraControlCreatorFunction function
    c.find('SetExtraControlCreator').ignore()
    c.find('ExtraControlCreatorFunction').ignore()


    c.find('GetFilenames').ignore()
    c.addCppMethod('wxArrayString*', 'GetFilenames', '()', doc="""\
        Returns a list of filenames chosen in the dialog.  This function
        should only be used with the dialogs which have wx.MULTIPLE style,
        use GetFilename for the others.""",
        body="""\
        wxArrayString* arr = new wxArrayString;
        self->GetFilenames(*arr);
        return arr;""",
        factory=True)

    c.find('GetPaths').ignore()
    c.addCppMethod('wxArrayString*', 'GetPaths', '()', doc="""\
        Returns a list of the full paths of the files chosen. This function
        should only be used with the dialogs which have wx.MULTIPLE style, use
        GetPath for the others.
        """,
        body="""\
        wxArrayString* arr = new wxArrayString;
        self->GetPaths(*arr);
        return arr;""",
        factory=True)


    tools.fixTopLevelWindowClass(c)


    for funcname in ['wxFileSelector',
                     'wxFileSelectorEx',
                     'wxLoadFileSelector',
                     'wxSaveFileSelector',
                     ]:
        c = module.find(funcname)
        c.mustHaveApp()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

