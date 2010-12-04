import sys
import os

# make sure our development dir is on the path
if os.path.dirname(__file__):
    phoenixDir = os.path.abspath(os.path.dirname(__file__)+'/..')
else:  # run as main?
    d = os.path.dirname(sys.argv[0])
    if not d: d = '.'
    phoenixDir = os.path.abspath(d+'/..')

#if phoenixDir not in sys.path:
sys.path.insert(0, phoenixDir)

# stuff for debugging
import wxPhoenix as wx
print "pid:", os.getpid()
#print "executable:", sys.executable; raw_input("Press Enter...")

if sys.version_info < (2,7):
    # The unittest2 package has back-ported most of the new features of the
    # unittest module in Python 2.7, you can get it at PyPI.
    import unittest2
else:
    import unittest
    sys.modules['unittest2'] = unittest
    
args = sys.argv[:1] + 'discover -p test_*.py -s unittests -t .'.split() + sys.argv[1:]
unittest2.main( argv=args )

