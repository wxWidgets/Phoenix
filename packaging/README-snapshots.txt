wxPython Phoenix Snapshot Builds
================================

This directory contains a (nearly) daily set of snapshot builds for
the wxPython Phoenix project. Each time there is a successful daily
build from the buildbot the results are uploaded here, in addition to
the source and documentation tarballs.  Currently binaries for Windows
and OSX are included, for a few versions of Python.  The source
tarball can be used to build wxPython Phoenix for other platforms.
See Phoenix/README.rst in the source tarball for more information.

The binaries in this directory are provided using Python's "wheel"
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
        -f http://wxpython.org/Phoenix/snapshot-builds/ \
        wxPython_Phoenix

NOTE: if there isn't a binary here for the latest version of Phoenix
that matches your Python version, then the command above will download
the latest version of the source and will try to build Phoenix for
you.  This will not be successfull if you do not have appropriate
development tools and dependent libraries installed.

To install a specific binary from this site you can append the version
number to the command, like this:

    pip install -U --pre \
        -f http://wxpython.org/Phoenix/snapshot-builds/ \
        wxPython_Phoenix==3.0.3.dev78269

If you don't already have pip then you can install it with commands
like this:

    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py

See https://pip.pypa.io/en/latest/index.html for more info.

Happy Hacking!
Robin
