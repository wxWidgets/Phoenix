#---------------------------------------------------------------------------
# Name:        etg/_richtext.py
# Author:      Robin Dunn
#
# Created:     27-Oct-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_richtext"
NAME      = "_richtext"   # Base name of the file to generate to for this script
DOCSTRING = """\
The :class:`RichTextCtrl` is a generic, ground-up implementation of a rich
text control capable of showing multiple text styles and images.  This module
contains the control and many supporting classes needed for using the features
of the :class:`RichTextCtrl`.

.. note:: Due to some internal dynamic initialization in wxWidgets, this
          module should be imported **before** the :class:`wx.App` object is
          created.
"""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ ]


# The list of other ETG scripts and back-end generator modules that are
# included as part of this module. These should all be items that are put in
# the wxWidgets "richtext" library in a multi-lib build.
INCLUDES = [ 'richtextbuffer',
             'richtextctrl',
             'richtexthtml',
             'richtextxml',
             'richtextprint',
             'richtextstyles',
             'richtextstyledlg',
             'richtextsymboldlg',
             'richtextformatdlg',
             ]


# Separate the list into those that are generated from ETG scripts and the
# rest. These lists can be used from the build scripts to get a list of
# sources and/or additional dependencies when building this extension module.
ETGFILES = ['etg/%s.py' % NAME] + tools.getEtgFiles(INCLUDES)
DEPENDS = tools.getNonEtgFiles(INCLUDES)
OTHERDEPS = [  ]


#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING,
                                check4unittest = False)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    module.addHeaderCode('#include <wxPython/wxpy_api.h>')
    module.addImport('_core')
    module.addPyCode("import wx", order=10)
    module.addImport('_xml')
    module.addImport('_html')
    module.addImport('_adv')

    module.addInclude(INCLUDES)

    # Redo the initialization of wxModules in the case where this extension
    # module is not imported until *after* the wx.App has been created.
    module.addInitializerCode("""\
        wxPyReinitializeModules();
        """)


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)



#---------------------------------------------------------------------------

if __name__ == '__main__':
    run()
