#---------------------------------------------------------------------------
# Name:        etg/notifmsg.py
# Author:      Robin Dunn
#
# Created:     21-May-2012
# Copyright:   (c) 2012-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_adv"
NAME      = "notifmsg"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [ "wxNotificationMessage",
           ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    c = module.find('wxNotificationMessage')
    assert isinstance(c, etgtools.ClassDef)
    c.mustHaveApp()

    # take care of some methods only available on MSW
    c.find('UseTaskBarIcon').setCppCode("""\
        #ifdef __WXMSW__
            return wxNotificationMessage::UseTaskBarIcon(icon);
        #else
            wxPyRaiseNotImplemented();
            return NULL;
        #endif
        """)

    c.find('MSWUseToasts').setCppCode("""\
        #ifdef __WXMSW__
            return wxNotificationMessage::MSWUseToasts(*shortcutPath, *appId);
        #else
            wxPyRaiseNotImplemented();
            return false;
        #endif
        """)

    # TODO: Also add wxGenericNotificationMessage

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

