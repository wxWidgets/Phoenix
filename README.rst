=========================
wxPython Project Phoenix
=========================

.. image:: demo/bitmaps/splash.png
   :align: center


Introduction
------------

Welcome to wxPython's Project Phoenix! Phoenix is the improved next-generation
wxPython, "better, stronger, faster than he was before." This new
implementation is focused on improving speed, maintainability and
extensibility. Just like "Classic" wxPython, Phoenix wraps the wxWidgets C++
toolkit and provides access to the user interface portions of the wxWidgets
API, enabling Python applications to have a native GUI on Windows, Macs or
Unix systems, with a native look and feel and requiring very little (if any)
platform specific code.

.. note::
    This document is primarily intended for those who will be working on
    wxPython, or at least building with the source code fetched directly from
    GitHub. If that's not you then please refer to the instructions at the
    `wxPython website <https://wxpython.org/pages/downloads/>`_ about how to get
    the current release of wxPython for your platform and chosen Python
    environment.

.. contents:: **Contents**


Development at GitHub.com
-----------------------------

Development of wxPython is done with git, using
https://github.com/wxWidgets/Phoenix as the main development site.

Currently (September, 2024), only 2 developers (@swt2c, @RobinD42) can merge
pull requests, or assign others to review pull requests.


How to build wxPython Phoenix
-----------------------------

First of all, this README is intended primarily for those who want to build
wxPython from a workspace checked out from the wxPython Phoenix repository. If
you are not making changes to wxPython, or needing to build it for some
unsupported compiler or some other hardware architecture, then you probably do
not need to put yourself through the pain for building in this way. It's a
complicated build, and can sometimes be confusing even for the experts.
Instead, if the binaries available at PyPI are not what you need then you can
use pip to build from the released source archives, or from the source archives
created in the pre-release snapshot builds. See the notes about it at:

* https://wxpython.org/pages/downloads/
* https://wxpython.org/blog/2017-08-17-builds-for-linux-with-pip


Next, review the section below about prerequisites.

All aspects of the wxPython Phoenix build are managed through a series of
commands provided by the build.py script. There is also a setup.py script
available for builds using setuptools.  The setup.py script assumes that all of
the code generation steps have already been performed, and so it is suitable
for use when building from a source snapshot tarball or when using pip. The
setup.py script will delegate to build.py for the actual build, and build.py
will delegate to setup.py when using pip or building a wheel.

Using the build.py script allows for greater control over the build process
than setup.py does, including commands for performing the various
code-generation steps. So developers working on Phoenix itself or building
from a Git checkout, instead of a source snapshot tarball, should be using
the build.py script. The build.py script provides a fairly simple
command-line interface consisting of commands and options. To see the full
list run ``python build.py --help``. The most important commands are listed
below.

**Windows Users NOTE:** If you are building Phoenix on Windows and have a
non-English language installation of Microsoft Visual Studio then you may
need to set the code page in your console window in order to avoid Unicode
decoding errors. For example::

    chcp 1252
    python build.py <build commands>...

In addition, some tasks within the build currently expect to be able to use
Cygwin on Windows (https://www.cygwin.com/) to do its work. If you have
Cygwin installed in one of the default locations (c:\\cygwin or c:\\cygwin64)
then all is well. If you have it installed somewhere else then you can set
CYGWIN_BASE in the environment and the build tool will use that for the base
dir.

On the other hand, if you just want to do a standard setuptools-style build
using setup.py and are using a full source tarball, then you can stop reading
at this point. If you want to build from a source repository checkout, or
need to make changes and/or to regenerate some of the generated source files,
then please continue reading.


Building wxWidgets
------------------

Since build.py will, by default, build both wxWidgets and Phoenix you will
need the wxWidgets code as well. The source tarballs already include both
wxWidgets and the Phoenix source code, so if you are getting your copy of the
source code that way then you are all set. If you are fetching it from GitHub
you will need to do an additional step. The git repository is set up to bring
in the wxWidgets code as a git "submodule" so after cloning the Phoenix
repository, you can get the wxWidgets source with these commands::

  $ git submodule update --init --recursive

This will clone the wxWidgets repo into: ``Phoenix/ext/wxWidgets``. Once the
submodule is updated, the build script should be able to build wxWidgets.

If you would rather use an already built and installed wxWidgets then that is
possible as well by changing some options, see ``python build.py --help`` for
details. However be aware that doing so will require a wxWidgets that is
**very** close to the same age as the Phoenix code, at least for the
unreleased preview snapshots. In other words, the wxWidgets build should use
code from the wxWidgets source repository within a few days of when the
Phoenix code was checked out. Currently the master branch of Phoenix is
tracking the master branch of wxWidgets.

On the other hand, it is probably best to just let wxPython build and bundle
wxWidgets. The build tools will by default build wxWidgets in a way that
allows it to be bundled with the wxPython extension modules as part of the
wxPython package, meaning it can peacefully coexist with any wxWidgets
libraries you may already have installed. This bundling of the wx shared
libraries works on Windows, OSX and Linux, and probably any other unix-like
system using shared libraries based on the ELF standard. The libraries are
built in such a way that they are relocatable, meaning that they do not have
to be in a fixed location on the filesystem in order to be found by the
wxPython extension modules. This also means that you can do things like use
``pip`` to install a wxPython wheel in one or more virtual environments, move
the wx package to a versioned folder, or even move it into your own project
if desired, all without needing to rebuild the binaries. (Assuming that
compatible Pythons are being used in all cases of course.)

The build phase of the build.py script will copy the results of the wxWidgets
and Phoenix builds into the wx folder in the Phoenix source tree. This will
allow you to run and test Phoenix directly from the source tree without
installing it, if desired. You just need to set ``PYTHONPATH`` appropriately,
or you can use ``python setup.py develop`` or ``pip install -e .`` to install
an .egg-link file in your current Python site-packages folder that will point
to the folder where you built wxPython Phoenix. When you are finished testing
you can then use the install or one of the bdist commands like you normally
would for other Python packages.



Important build.py commands
---------------------------

The following ``build.py`` commands are required to be able to build Phoenix
from scratch. In other words, from a pristine source tree with none of the
generated code present yet. They can be run individually or you can specify
all of them on a single command line, in the order given. Once a command has
succeeded in one run of build.py there is no need to run that command again in
a later run, unless you've changed something which that command has the
responsibility to process. Many of the commands require the results of the
earlier commands, so at least the first time you run the build you will need
to use all 4 of the commands (or their equivalents for composite commands) in
the given order.

* **dox**: Builds the XML files from the wxWidgets documentation source,
  which will be used as input for the etg command.

* **etg**: Extracts information from the dox XML files, runs hand-written
  tweaker code on the extracted data structures, and runs various generators
  on the result to produce code for the next steps. The code being run for
  each item in this step is located in the etg folder in the Phoenix source
  tree.

* **sip**: This command processes the files generated in the etg command
  and produces the C++ code that will become the Python extension modules for
  wxPython Phoenix.

* **build**: Build both wxWidgets and wxPython. There are additional
  commands if you want to build just one or the other. The results will be
  put in the Phoenix/wx folder, and can be used from there without
  installation if desired, by setting PYTHONPATH so the Phoenix/wx package
  dir is found by Python.

Some other useful commands and options are:

* **clean**: Clean up the build products produced by prior runs of
  build.py. There are additional clean commands that will let you clean up
  just portions of the build if needed.

* **touch**: Updates the timestamp on all of the etg scripts, so they will
  be forced to be run in the next build. This is useful when a change has
  been made to the wxWidgets documentation that needs to be propagated
  through the build since the etg command doesn't yet do full dependency
  checking of the input.

* **M.N**: This is the Major.Minor version number of the Python that the
  extension modules will be built for, such as "3.11". This allows you to run
  build.py with a different Python than what you are building for, which is
  handy for things like buildbots running in a virtualenv for one Python
  that need to be able to run builds for other versions too.

  If build.py is not able to find the correct Python given the M.N on the
  command line then you can specify the full path to the python executable you
  want to use with the ``--python`` option.

* **test**: Runs all of Phoenix's unittests.

* **--nodoc**: This option turns off the sphinx generator when running the
  etg scripts. If you don't plan on generating the documentation then this
  will speed up the processing of the etg command.

Please see the output of ``python build.py --help`` for information about
commands and options not mentioned here. And, as always, if there is any
discrepancy between this document and the source code in the build.py script,
then the source code is correct. ;-)

The build.py script will download doxygen, sip and waf for your platform as
needed if they are not already in your Phoenix/bin folder. If prebuilt
versions of these tools are not available for your platform then build.py
will bail out with an error message. To continue with the build you will need
to acquire copies of the tool that will work on your platform and can then
tell build.py where to find it using an environment variable, as described in
the error message.


Example build command-lines
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To do a complete build from a totally clean git workspace, you will
need to use several of the commands listed above.  For example::

    python build.py dox etg --nodoc sip build

Subsequent builds can leave out some of the commands if there were no
changes which would require those commands to be run again.  For
example, if you wanted to just rebuild the Phoenix extension modules
you could do this::

    python build.py build_py

If you've changed one of the etg files and need to regenerate and
rebuild the source affected by that change, then you can use a command
like this::

    python build.py etg --nodoc sip build build_py



Project directory structure
---------------------------

There are a lot of subfolders in this directory, here is a brief
explanation to help a newbie find their way around.

* **build**: Intermediate files produced by the build process are stored
  here. This folder should not be committed to a source repository.

* **buildtools**: This is a Python package containing modules that are used
  from build.py and setup.py and which assist with configuring and running
  the build.

* **etg**: This is where the "Extractor-Tweaker-Generator" scripts are stored.
  These scripts are invoked by the build and they will read the XML files
  produced by Doxygen and will produce interface definition files for SIP.

* **etgtools**: This Python package contains modules which assist with the
  parsing of the XML files, tweaking the collection of objects produced by
  the parser, and also the backend generation of code or documentation.

* **ext**: This folder holds the source for external projects used by
  Phoenix, (currently just wxWidgets) as git submodules. This allows Phoenix
  to use a specific revision of the code in the other projects and not depend
  on the developer fetching the correct version of the code on their own.

  When you first checkout the Phoenix source using git you will need to tell
  git to also fetch the submodules, like this::

    cd Phoenix
    git submodule init
    git submodule update --recursive

* **sip/gen**: The code (.sip files) produced by the ETG scripts is placed
  in this folder.

* **sip/cpp**: The code produced when running SIP is put in this folder. It
  will be C++ source and header files, and also some extra files with
  information about the source files produced, so the build knows what files
  to compile.

* **sip/siplib**: This is a copy of the SIP runtime library. We have our
  own copy so it can be included with the wxPython build as an extension
  module with a unique name (``wx.siplib``) and to not require a runtime
  dependency on SIP being installed on the target system. 3rd party
  extensions that want to integrate with wxPython should ensure that the
  sip.h they ``#include`` is the one in this folder.

* **src**: This folder is for any other source code (SIP, C++, Python, or
  anything else) that is edited by hand instead of being generated by some
  tool.

* **wx**: This is the top of the wxPython package. For an in-place build the
  extension modules and any associated files will be put into this folder.
  Subfolders contain pure-python subpackages of the wx package, such as
  wx.lib, etc.



Naming of files
---------------

To help keep things a little easier when looking for things that need to be
worked on, the file names in the Phoenix project will mirror the names of the
files in the wxWidgets interface headers folder. For example, if there is a
``interface/wx/FOO.h`` and we are processing the XML produced for that file
then the ETG script for the classes and other items will be named
``etg/FOO.py`` and it will produce ``sip/gen/FOO.sip``, unit tests will be in
``unittests/test_FOO.py``, and so on.

In most cases more than one ETG/SIP file will be used to create a single
Python extension module. In those cases there will be one ETG script used to
bring all the others together into the single extension module (by using the
back-end generator's include feature for example.) The names of those scripts
will have a leading underscore, such as ``etg/_core.py``, and all the scripts
that are intended to be included in that extension module should specify that
name in their MODULE variable.


Prerequisites
-------------

The following are some tips about what is required to build Phoenix for
yourself. There are likely some other things that may not have been mentioned
here, if you find something else that should be mentioned then please submit
a PR for updating this document.


**Windows**

All the source code needed for wxWidgets and wxPython Phoenix are included in
the wxWidgets and Phoenix source trees. In addition to a stock Python
installation you will also need a copy Visual Studio 2015. It may be possible
to build using Mingw32, but there will need to be some changes made to the
build scripts to support that.

You may also want to get a copy of the MS SDK in order to have newer
definitions of the Windows API.

If you want to build Phoenix with debug info then you will need to first
build a debug version of Python, and then use that Python (python_d.exe) to
build Phoenix.


**Linux**

On Ubuntu the following development packages and their dependencies should be
installed in order to build Phoenix. Other debian-like distros will probably
also have these or similarly named packages available, or newer versions of
Ubuntu might have evolved somewhat and require changes from this list.
Extrapolate other package names accordingly for other linux distributions or
other unixes.

* dpkg-dev
* build-essential
* python3-dev
* freeglut3-dev
* libgl1-mesa-dev
* libglu1-mesa-dev
* libgstreamer-plugins-base1.0-dev
* libgtk-3-dev
* libjpeg-dev
* libnotify-dev
* libpng-dev
* libsdl2-dev
* libsm-dev
* libtiff-dev
* libwebkit2gtk-4.0-dev
* libxtst-dev

If you are building for GTK2 then you'll also need these packages and
their dependencies:

* libgtk2.0-dev
* libwebkitgtk-dev


If you use a custom built python in a non standard location, You need to
compile python with the --enable-shared option.

**Mac OSX**

Like the Windows platform all the source and libs you need for building
Phoenix on OSX are included in the wxWidgets and Phoenix source trees, or
by default on the system. In addition you will need to get the Xcode
compiler and SDKs, if you don't already have it, from
https://developer.apple.com/ (free registration required). You should
also install the command line tools for your version of Xcode and OSX.
This can usually be done from within Xcode or via a separate installer
package.

Also like on Windows, using the same or similar compiler that was used to
build Python usually helps things to work better and have a better chance
for success.

If all else fails it is not too hard to build Python yourself using
whatever Xcode you have installed, and then use that Python when building
Phoenix.


Help and Helping
----------------

Please use  `GitHub issues <https://github.com/wxWidgets/Phoenix/issues>`_
to report bugs.  Discussions about Python usage happen at
`Discuss wxPython <https://discuss.wxpython.org/>`_.


Latest Snapshot Builds
----------------------

You can find snapshots of the latest wxPython Phoenix build files,
including source snapshots, wheels files for Windows and Mac, and etc. at:
https://wxpython.org/Phoenix/snapshot-builds/.  These files are built at most
once per day, on any day that has had a commit to the master branch.


.. image:: docs/phoenix-fire-md.png
   :width: 100%
