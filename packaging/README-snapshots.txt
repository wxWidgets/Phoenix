wxPython Phoenix Snapshot Builds
================================

This directory contains a set of snapshot builds for the wxPython Phoenix
project. Each time there is a successful daily build from the buildbot the
results are uploaded here, in addition to the source and documentation
tarballs. Currently binaries for Windows and OSX are included, for a few
versions of Python. The source tarball can be used to build wxPython Phoenix
for other platforms. See Phoenix/README.rst in the source tarball for more
information.


File naming conventions:
------------------------

 - Files with the "*.whl" extension are binary wheel files
   (https://wheel.readthedocs.org/en/latest/). See below for more info.

 - Files with the "*.tar.gz" extension are compressed tar archives of the
   Phoenix and wxWidgets source code.

 - The "*-docs-*.tar.gz" files are compressed archives of the documentation.

 - The bulk of the filename follows the convensions for naming wheels
   (https://www.python.org/dev/peps/pep-0427/#file-name-convention). For
   example:

      wxPython_Phoenix-3.0.3.dev1549+fa6f31f-cp33-cp33m-macosx_10_6_intel.whl

   means:

   - This is the wxPython_Phoenix package

   - It is version 3.0.3.dev1549+fa6f31f (a development version, with
     the build number derived from the source control system.)

   - It is built for CPython version 3.3

   - It is built for the macosx operating system

   - It is built for OSX version 10.6 or greater

   - It is built for Intel processors.


Installing Wheels
-----------------

The *.whl binaries in this directory are provided using Python's "wheel"
format, which is an archive format with some extra meta-data that can
be used by some Python tools to track installs, do uninstalls, etc.
In addition to the tools provided by the wheel package, the commonly
used pip command can also be used to install, upgrade and uninstall
wheels.  It can also be used to automatically download the correct
version of a wheel for you from PyPi, and then install it.  With a
little extra help it can do the same for prerelease versions of
software wheels like what is available here, with a command like
this:

    pip install -U --pre \
        -f https://wxpython.org/Phoenix/snapshot-builds/ \
        wxPython_Phoenix

NOTE: if there isn't a binary here for the latest version of Phoenix
that matches your Python version, then the command above will download
the latest version of the source and will try to build Phoenix for
you.  This will not be successfull if you do not have appropriate
development tools and dependent libraries installed.

To install a specific binary from this site you can append the version
number to the command, like this:

    pip install -U --pre \
        -f https://wxpython.org/Phoenix/snapshot-builds/ \
        wxPython_Phoenix==3.0.3.dev1641+76cf834

There are also snapshot builds available for a few of the common Linux
distributions, located under the following folder:

    https://wxpython.org/Phoenix/snapshot-builds/linux/


Wheels for Linux
----------------

Since there are various options for distro and wx port (GTK2 or GTK3) then the
files can not all be located in the same folder like we can do for the Windows
and OSX builds.  This just simply means that you'll need to drill down a
little further to find the URL to give to pip.  For example, to get the GTK3
Phoenix builds for Ubuntu 16.04 (and 16.10, LinuxMint 18, and probably others)
you can use a pip command like this:

    pip install -U --pre \
        -f https://wxpython.org/Phoenix/snapshot-builds/linux/gtk3/ubuntu-16.04 \
        wxPython_Phoenix


Getting Pip
-----------

If you don't already have pip then you can install it with commands
like this:

    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py

See https://pip.pypa.io/en/latest/index.html for more info.


Happy Hacking!
Robin
