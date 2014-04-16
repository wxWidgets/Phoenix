#----------------------------------------------------------------------
# Name:        buildtools.version
# Purpose:     wxPython version numbers used in the build.  This can be
#              considered the master copy of the version digits.
#
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------


VER_MAJOR        = 3      # The first three must match wxWidgets
VER_MINOR        = 0
VER_RELEASE      = 1
VER_FLAGS        = ""     # wxPython release flags

# Set the VER_FLAGS component according to the following patterns. These
# should help us to better conform to the setuptools and/or PEP-0386 notions
# of version numbers.  
#
#   ""             for final release builds
#
#   "-1"           for numbered post releases, such as when there are 
#                  additional wxPython releases for the same wxWidgets 
#                  release.  TBD: use - or .post or ? 
#
#   ".dev12345"    for daily snapshot builds, by default this is automatically
#                  pulled from the REV.txt file made by the setrev command,
#                  if it exists, and is appended to VER_FLAGS
#
#   "a1"           for official alpha releases
#   "b1"           for beta relases
#   "rc1"          for release candidate releases
#
#   "-1a1"         For alpha releases of a numbered post release, (betas, etc. 
#                  of numbered post releases can be done the same way)
#
# See also:
#
#   http://pythonhosted.org/setuptools/setuptools.html
#   http://www.python.org/dev/peps/pep-0386/