How to use the Phoenix snapshot build
=====================================

Hello, and welcome to the Phoenix snapshot build. If you are not
interested in Phoenix or do not know what Phoenix is, you may want to
exit the plane now and find a ticketing agent to help you get to the
correct package.

This tarball is basically a dump of the 'wx' package after a build has
been done, probably by one of the buildbot's build slaves. To use it
instead of Classic wxPython you will need to do a little tweaking to
your environment, which we will describe here. There are likely other
solutions that would work just as well, feel free to use something
else if you prefer.


Virtualenv
----------

One of the easiest ways to try out new Python modules without
impacting those that are already installed for other projects is to
use the virtualenv (or similar) tool to create a new stock python
environment with only the additional packages that you need, plus this
Phoenix test snapshot.  We highly recommend the use of such a tool to
avoid unexpected interactions with other packages.


Help Python find Phoenix
------------------------

All the usual suspects apply here.  You can simply add this folder to
your PYTHONPATH environment variable.  Or you can add a phoenix.pth
file to some place already on the sys.path which contains the path to
this folder.  Or you can even copy the wx folder into the
site-packages folder in your virtualenv.


Help Phoenix find wxWidgets
---------------------------

The Phoenix extension modules need to load the dynamic libraries that
contain the wxWidgets code for the platform.  For the Windows platform
nothing extra should be needed because the system will automatically
look for the DLLs in the same folder that the extension modules are
located in.

For Unix-like systems like Linux or OSX the locations that are
searched for the dynamic libraries can be controlled by setting
environment variables, DYLD_LIBRARY_PATH for OSX or LD_LIBRARY_PATH
for the others.  Basically you just need to set that variable to the
path of the wx package, for example if you're on a Mac and currently
in the folder where this README is located, then you can do something
like this::

    export DYLD_LIBRARY_PATH=`pwd`/wx

The phoenix_environ.sh shell script included with this build can help
you do that, just be sure to use the "source" command so the variables
in the current shell's environment will be modified.

It is also possible to embed the path that the dynamic library should
be loaded from directly into the extension module.  For now at least
this is left as an exercise for the reader.  For OSX look at the man
pages for the otool and install_name_tool commands.  For the other
unix-like platforms look at chrpath.
