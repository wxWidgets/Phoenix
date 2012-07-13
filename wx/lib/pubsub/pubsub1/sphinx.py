'''
Sphinx autodoc requires direct import of pubsub.pubsub1.pub. 
But in that case, the pub module no longer has access to 
sibbling modules from pubsub package. By adding ".." to 
sys.path, "import something" in pubsub1/pub.py find the 
module in pubsub and sphinx autodoc works as expected. 

This module should be used from sphinx's conf.py.
'''

# add the parent folder to sys.path because Sphinx needs to import 
# pubsub1 as a module rather than via the mechanism built into pubsub
# module. 
import sys, os
sphinxExtPath = os.path.normpath( 
                    os.path.join( 
                        os.path.dirname(__file__), 
                        '..') 
                )
sys.path.append( sphinxExtPath )
