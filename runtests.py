import sys, os

if sys.version_info < (2,7):
    # The unittest2 package has back-ported most of the new features of the
    # unittest module in Python 2.7, you can get it at PyPI.
    import unittest2
else:
    import unittest
    sys.modules['unittest2'] = unittest
    
args = sys.argv[:1] + 'discover -p test_*.py -s unittests -t .'.split() + sys.argv[1:]
unittest2.main( argv=args )
