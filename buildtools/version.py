#----------------------------------------------------------------------
# Name:        buildtools.version
# Purpose:     wxPython version numbers used in the build.  This can be
#              considered the master copy of the version digits.
#
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010-2017 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------


VER_MAJOR        = 3      # Matches wxWidgets MAJOR version number
VER_MINOR        = 0      # Matches wxWidgets MINOR version number
VER_RELEASE      = 4      # wxPython RELEASE number for the given wxWidgets
                          # MAJOR.MINOR version.

VER_FLAGS        = "a1"     # wxPython release flags

# The VER_FLAGS value is appended to the version number constructed from the
# first 3 components and should be set according to the following patterns.
# These should help us to better follow the PEP-0440 notions of version
# numbers, where public version identifiers are supposed to conform to the
# following scheme:
#
#      [N!]N(.N)*[{a|b|rc}N][.postN][.devN]
#
#
#   ""             for final release builds
#
#   "aN"           for official alpha releases
#   "bN"           for official beta releases
#   "rcN"          for release candidate releases
#
#   ".postN"       for numbered post releases, such as when there are
#                  minor packaging or documentation issues that can be fixed
#                  with no code changes.
#
#   ".postNaN"     for an alpha (or beta or rc) build of a numbered post
#                  release
#
#   ".dev12345"    for daily snapshot builds, by default this is automatically
#                  pulled from the REV.txt file made by the setrev command,
#                  if it exists, and is appended to VER_FLAGS
#
#
# See also:
#   http://www.python.org/dev/peps/pep-0440/
