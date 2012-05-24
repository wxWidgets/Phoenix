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
import wx
print("wx.version: " + wx.version())
print("pid: " + str(os.getpid()))
#print("executable: " + sys.executable); raw_input("Press Enter...")

import imp_unittest, unittest

args = sys.argv[:1] + 'discover -p test_*.py -s unittests -t .'.split() + sys.argv[1:]
unittest.main( argv=args )

