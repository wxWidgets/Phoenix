'''
This is used internally by pubsub to allow modules of the pubsub.utils 
subpackage to import modules of a sibbling subpackage (such as 
pubsub.core).

Value of "up" parameter: For intraImport() the defaut up is 1 because 
it is always used from within an __init__ file ie most likely scenario 
is up=1. The parentImport() function mostly used from within modules
of a package so up defaults to 2. 

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.
'''

# allow utils modules to find sibblings in core
def intraImport(pathList, up=1):
    '''Enable modules of a subpackage to import modules of a sibbling
    subpackage, or parent modules, ie A.B.C could import A.D.E by doing 
    'import D.E' (this is default behavior). If up > 1, can import from 
    higher up the import tree. For instance with up=2, ie A.B.C.D could 
    import A.E.F.G by doing 'import E.F.G'. 
    
    WARNING: it looks like Python
    loads a separate copy of sibbling modules found via the modified 
    module search path; this is a problem if the sibbling modulres 
    contain globals (singletons) since more than one instance of a module
    could exist in an application. Use parentImport() in such case.'''
    import os
    newPath = pathList[0]
    for _ in range(0, up):
        newPath = os.path.join(newPath, '..')
    # py2exe requires abspath to find new path 
    pathList.append( os.path.abspath( newPath ) )


_importCache = {}

def parentImport(modName, up=2):
    '''Import a module modName from parent of current package. Default 
    assumes used within a non-init module of pubsub.utils, ie up=2.'''
    
    # see if in cache
    modObj = _importCache.get( (modName, up), None )
    if modObj is not None: 
        return modObj
    
    # not in cache, assume parent already imported
    module = globals()['__name__'].split('.')
    parentModName = '.'.join( module[:-up] )
    import sys
    parentModObj = sys.modules[parentModName]
    
    try:
        modObj = getattr(parentModObj, modName)
        _importCache[ (modName, up) ] = modObj
        return modObj
    
    except AttributeError:
        msg = 'no module named %s in %s' % (modName, parentModName)
        raise ImportError(msg)
    
