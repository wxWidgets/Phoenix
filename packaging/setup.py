#----------------------------------------------------------------------
# Name:        setup.py
# Purpose:     Distutils build script for wxPython (phoenix)
#
# Author:      Robin Dunn
#
# Created:     27-Mar-2013
# Copyright:   (c) 2013-2016 by Total Control Software
# License:     wxWindows License
#----------------------------------------------------------------------
#---------------------------------------------------------------------------
# This setup file is placed in the root folder of the source dist tarball,
# and will be used to help do automated builds from tools like easy_install
# or pip.  These tools expect to find at least the setup.py in the root
# folder, so let's accommodate them...
#---------------------------------------------------------------------------

import sys, os, glob

# Restructure the content of the tarball so things like pip or easy_install
# know how to build stuff. To be compatible with those tools the main source
# dir needs to be the root, so move all of Phoenix/* here.
SRC = 'Phoenix'
if os.path.exists(SRC) and os.path.isdir(SRC):
    items = os.listdir(SRC)
    for item in items:
        os.rename(os.path.join(SRC, item), item)
    os.rmdir(SRC)

# Somewhere along the way (probably when pip untars the source tar file) any
# executable permissions set on files in the tarball gets lost. Some of them
# will break our build if they are not executable, so turn them back on.
for wc in ['wxWidgets/configure',
           'wxWidgets/src/stc/gen_iface.py',
           'bin/waf-*', ]:
    for item in sorted(glob.glob(wc)):
        os.chmod(item, 0o755)


# Now execute the real setup.py that was copied here in order to do whatever
# command was trying to be done before.
if sys.version_info < (3,):
    execfile('setup.py')
else:
    with open('setup.py', 'r') as f:
        source = f.read()
    exec(source)

