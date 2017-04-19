#---------------------------------------------------------------------------
# Name:        etg/msgdlg.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     24-Sept-2011
# Copyright:   (c) 2011 by Kevin Ollivier
# Copyright:   (c) 2011-2017 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools
import copy

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "msgdlg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  =    [
                'wxMessageDialog',
            ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxMessageDialog')
    assert isinstance(c, etgtools.ClassDef)

    module.addGlobalStr('wxMessageBoxCaptionStr', c)

    # These argument types are actually ButtonLabel, but the class is a private
    # helper. We will always be passing in strings, and ButtonLabel will implicitly
    # convert.
    #
    # TODO: Add a mapped type for ButtonLabel that converts from a string or stock ID. See #276
    c.find('SetHelpLabel.help').type = 'const wxString&'
    c.find('SetOKCancelLabels.ok').type = 'const wxString&'
    c.find('SetOKCancelLabels.cancel').type = 'const wxString&'

    c.find('SetOKLabel.ok').type = 'const wxString&'

    c.find('SetYesNoCancelLabels.yes').type = 'const wxString&'
    c.find('SetYesNoCancelLabels.no').type = 'const wxString&'
    c.find('SetYesNoCancelLabels.cancel').type = 'const wxString&'

    c.find('SetYesNoLabels.yes').type = 'const wxString&'
    c.find('SetYesNoLabels.no').type = 'const wxString&'

    tools.fixTopLevelWindowClass(c)



    # Make a copy of wxMessageDialog so we can generate code for
    # wxGenericMessageDialog too.
    gmd = copy.deepcopy(c)
    assert isinstance(gmd, etgtools.ClassDef)
    gmd.name = 'wxGenericMessageDialog'
    gmd.find('wxMessageDialog').name = 'wxGenericMessageDialog'  # the ctor

    m = gmd.addItem(etgtools.MethodDef(
        protection='protected', type='void', name='AddMessageDialogCheckBox',
        briefDoc="Can be overridden to provide more contents for the dialog",
        className=gmd.name))
    m.addItem(etgtools.ParamDef(type='wxSizer*', name='sizer'))

    m = gmd.addItem(etgtools.MethodDef(
        protection='protected', type='void', name='AddMessageDialogDetails',
        briefDoc="Can be overridden to provide more contents for the dialog",
        className=gmd.name))
    m.addItem(etgtools.ParamDef(type='wxSizer*', name='sizer'))

    module.addItem(gmd)


    module.find('wxMessageBox').releaseGIL()

    c = module.find('wxMessageBox')
    c.mustHaveApp()


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

