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
file to someplace already on the sys.path which contains the path to
this folder.  Or you can even copy the wx folder into the
site-packages folder in your virtualenv.


Help Phoenix find wxWidgets
---------------------------

The Phoenix extension modules need to load the dynamic libraries that contain
the wxWidgets code for the platform. In most cases the extension modules in
this snapshot already know to look in the same folder for the wxWidgets
shared libraries. This will work for Windows and Mac, and should also work
for any unix-like system based on ELF binaries, and if the expected objdump
utility was found on the build system.

For those cases where the build was not able to perform the necessary magic
required to be able to make and use relocatable shared libraries, you may
need to do a little extra to help wxPython find the wxWidgets libraries.
Check your platform's documentation for details, but it may be as simple as
setting the LD_LIBRARY_PATH variable in the environment. For example if
you're in the folder where this README is located, then you can do something
like this::

    export LD_LIBRARY_PATH=`pwd`/wx

