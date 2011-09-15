import sys

if sys.version_info < (2,7):
    # The unittest2 package has back-ported most of the new features of the
    # unittest module in Python 2.7, you can get it at PyPI.
    import unittest2
    sys.modules['unittest'] = unittest2
    
else:
    import unittest
