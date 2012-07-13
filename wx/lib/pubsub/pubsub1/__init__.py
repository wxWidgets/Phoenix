'''
This __init__ file is present to help with certain non-standard uses
of pubsub1:

1. so that sphinx's autodoc extension can find the pubsub1 documentation
2. so that py2exe can find the pub module when v1 API is used (pubsub1/pub.py 
   gets included in the library only if pubsub1 is a package)

Otherwise, the pubsub.pubsub1 is not a package but merely a folder that
holds the pub.py module for v1 API. Pubsub is designed so that, other than 
the two above cases, pubsub/pubsub1/pub.py will appear as pubsub.pub when 
pubsub.setupv1 is used (ie v1 API). 

:copyright: Copyright 2006-2009 by Oliver Schoenborn, all rights reserved.
:license: BSD, see LICENSE.txt for details.

'''

