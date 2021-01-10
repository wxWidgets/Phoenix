#---------------------------------------------------------------------------
# Name:        etg/log.py
# Author:      Kevin Ollivier
#              Robin Dunn
#
# Created:     08-Sept-2011
# Copyright:   (c) 2013 by Wide Open Technologies
# Copyright:   (c) 2011-2020 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"
MODULE    = "_core"
NAME      = "log"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script.
ITEMS  = [
            'wxLog',
            'wxLogGui',
            'wxLogNull',
            'wxLogRecordInfo',
            'wxLogChain',
            'wxLogInterposer',
            'wxLogInterposerTemp',
            'wxLogWindow',
            #'wxLogStream',  # needs std::ostream
            'wxLogStderr',
            'wxLogBuffer',
            'wxLogTextCtrl',
            'wxLogFormatter',
         ]

#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING)
    etgtools.parseDoxyXML(module, ITEMS)

    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.

    # do not use the va_list forms of the functions
    for func in module.allItems():
        if 'wxVLog' in func.name:
            func.ignore()

    for f in module.find('wxLogTrace').all(): # deprecated in 2.8
        f.ignore()

    # Switch the parameters to wxStrings to capitalize on the conversion code
    # we already have for them. String formatting can be done in Python if
    # needed. Drop the '...' too.
    for name in ['wxLogMessage', 'wxLogVerbose', 'wxLogWarning', 'wxLogFatalError',
                 'wxLogError', 'wxLogDebug', 'wxLogStatus', 'wxLogSysError',
                 'wxLogGeneric']:
        for f in module.find(name).all():
            p = f.find('formatString')
            p.type = 'const wxString&'
            p.name = 'message'
            f.items = f.items[:-1]

    module.find('wxSysErrorMsg').type = 'wxString'

    c = module.find('wxLogRecordInfo')
    c.find('threadId').ignore()


    c = module.find('wxLog')
    assert isinstance(c, etgtools.ClassDef)
    c.addPrivateCopyCtor()
    c.addDefaultCtor('public')
    c.addDtor('public', isVirtual=True)


    c.find('SetActiveTarget').transferBack = True
    c.find('SetActiveTarget.logtarget').transfer = True
    c.find('SetThreadActiveTarget').transferBack = True
    c.find('SetThreadActiveTarget.logger').transfer = True
    c.find('SetFormatter').transferBack = True
    c.find('SetFormatter.formatter').transfer = True


    # we need to un-ignore these protected methods as they need to be overridable
    c.find('DoLogRecord').ignore(False)
    c.find('DoLogTextAtLevel').ignore(False)
    c.find('DoLogText').ignore(False)


    c = module.find('wxLogStderr')
    c.find('wxLogStderr.fp').ignore()
    c.find('wxLogStderr.conv').ignore()
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()


    c = module.find('wxLogBuffer')
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()

    c = module.find('wxLogChain')
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()

    c = module.find('wxLogGui')
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()

    c = module.find('wxLogTextCtrl')
    c.addPrivateCopyCtor()
    c.addPrivateAssignOp()

    c = module.find('wxLogFormatter')
    c.find('FormatTime').ignore(False)

    c = module.find('wxLogNull')
    c.addPyMethod('__enter__', '(self)', 'return self')
    c.addPyMethod('__exit__', '(self, exc_type, exc_val, exc_tb)', 'return False')


    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)


#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

