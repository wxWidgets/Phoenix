#---------------------------------------------------------------------------
# Name:        etg/help.py
# Author:      Robin Dunn
#
# Created:     06-Apr-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "help"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxHelpControllerBase",
           #"wxHelpController",        See note below
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxHelpControllerBase')
    assert isinstance(c, etgtools.ClassDef)

    c.find('GetFrameParameters.size').out = True
    c.find('GetFrameParameters.pos').out = True
    c.find('GetFrameParameters.newFrameEachTime').out = True


    # NOTE: Since wxHelpController is an alias for wxHtmlHelpController on
    # Mac and GTK, and since we don't want to force the wx.core extension
    # module to link to the wxHTML library, then we won't provide a wrapper
    # for the wxHelpController 'class' here.
    #
    # Instead we'll add a Python factory function that accomplishes the same
    # thing. Basically it just provides a help controller instance that is the
    # best for the platform.

    module.addPyFunction('HelpController', '(parentWindow=None)',
        doc="""\
            Rather than being an alias for some class, the Python version of
            ``HelpController`` is a factory function that creates and returns an
            instance of the best Help Controller for the platform.
            """,
        body="""\
            try:
                if 'wxMSW' in wx.PlatformInfo:
                    from .msw import CHMHelpController as ControllerClass
                else:
                    from .html import HtmlHelpController as ControllerClass
            except ImportError:
                from .adv import ExtHelpController as ControllerClass

            return ControllerClass(parentWindow)
            """)



    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

