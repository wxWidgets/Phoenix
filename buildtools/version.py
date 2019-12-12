#----------------------------------------------------------------------
# Name:        buildtools.version
# Purpose:     wxPython project name and version numbers used in the
#              build.  This can be considered the master copy of the
#              version digits and project name.
#
# Author:      Robin Dunn
#
# Created:     3-Nov-2010
# Copyright:   (c) 2010-2018 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------

# Master copy of the project name
PROJECT_NAME     = 'wxPython'


# The version numbers for wxPython are no longer kept in sync with the
# wxWidgets version number. In the past the common version number was used to
# indicate which version of wxWidgets should be used for the wxPython build.
# Now wxWidgets is a git submodule, and the linked version is included in the
# wxPython source tarball. That said, we should still bump up the MAJOR and
# MINOR numbers each time there is a corresponding bump in the wxWidgets
# version numbers.
VER_MAJOR        = 4
VER_MINOR        = 1
VER_RELEASE      = 0

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
#                  pulled from the REV.txt file made by the setrev build command,
#                  if it exists, and is appended to VER_FLAGS
#
#
# See also:
#   http://www.python.org/dev/peps/pep-0440/


# The version numbers of wxWidgets to be used in the build
wxVER_MAJOR        = 3
wxVER_MINOR        = 1
wxVER_RELEASE      = 4  # only used when wxVER_MINOR is an odd value

