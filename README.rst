=========================
wxPython Project Phoenix
=========================

Welcome to wxPython's Project Phoenix! This project is a new implementation
of wxPython focused on improving speed, maintainability and extensibility.
Just like "Classic" wxPython it wraps the wxWidgets C++ toolkit and provides
access to the user interface portions of the wx API, enabling Python
applications to have a GUI on Windows, Macs or Unix systems with a native
look and feel and requiring very little (if any) platform specific code.

See http://wiki.wxpython.org/ProjectPhoenix for more information about this
project and information about how you can help out.


.. contents:: **Contents**


How to build Phoenix
--------------------

All aspects of the Phoenix build are managed through a series of commands
provided by the build.py script. There is also a setup.py script available
for those who are used to the standard distutils or setuptools types of
builds. The setup.py script assumes that all of the code generation steps
have already been performed, and so it is suitable for use when building from
a source snapshot tarball or when using easy_install or pip. The seup.py
script will delegate to build.py for the actual build, and build.py will
delegate to setup.py when doing setuptoolsy things like performing an install
or building an egg.

Using the build.py script allows for greater control over the build process
than setup.py does, including commands for performing the various
code-generation steps. So developers working on Phoenix itself or building
from a Subversion checkout, instead of just building it from a source
snapshot, should be using the build.py script. Build.py provides a fairly
simple command-line interface consisting of commands and options. To see the
full list run ``python build.py --help``. The most important commands are
listed below.

If you just want to do a standard setuptools-style build using setup.py and
using a full source tarball, then you can stop reading at this point. If you
want to build from a source repository checkout, or need to make changes
and/or to regenerate some of the generated source files, then please continue
reading.

Since build.py will, by default, build both wxWidgets and Phoenix you should
have both source trees checked out from Subverison (or one of the git mirrors
at github). I find that it works best when the two source trees are siblings
within the same parent folder, but other configurations can work too. If you
would rather use an already built and installed wxWidgets then that is
possible as well by changing some options, see ``python build.py --help`` for
details. However be aware that doing so will require a wxWidgets that is
**very** close to the same age as the Phoenix code, at least for the unreleased
preview snapshots. In other words, the wxWidgets build should use code from
the wxWidgets source repository within a few days of when the Phoenix code
was checked out.

On the other hand, it is probably best to just let Phoenix build and bundle
wxWidgets. The build tools will by default build wxWidgets in a way that
allows it to be bundled with the wxPython extension modules as part of the
wxPython package, meaning it can peacefully coexist with any wxWidgets
libraries you may already have installed. This bundling of the wx shared
libraries works on Windows, OSX and Linux, and probably any other unix-like
system using shared libraries based on the ELF standard. The libraries are
built in such a way that they are relocatable, meaning that they do not have
to be in a fixed location on the filesystem in order to be found by the
wxPython extension modules. This also means that you can do things like use
``easy_install`` to install an egg in one or more virtual environments, move
the wx package to a versioned folder, or even move it into your own project
if desired, all without needing to rebuild the binaries. (Assuming that
compatible Pythons are being used of course.)

The build phase of the build.py script will copy the results into the wx
folder in the Phoenix source tree. This will allow you to run and test
Phoenix directly from the source tree without installing it, if desired. You
just need to set ``PYTHONPATH`` appropriately, or you can use ``python
setup.py develop`` to install an .egg-link file in your current Python
site-packages folder that will point to the folder where you built Phoenix.
When you are finished testing you can then use the install or one of the
bdist commands like you normally would for other Python packages.



Important build.py commands
---------------------------

The following commands are required to be able to build Phoenix from scratch.
In other words, from a pristine source tree with none of the generated code 
present yet. They can be run individually or you can specify all of them on a 
single command line, in the order given. Once a command has succeded in one run 
of build.py there is no need to run that command again in a later run, unless
you've changed something which that command has the responsibility to
process.

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
  installation if desired.

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
  extension modules will be built for, such as "3.3". This allows you to run
  build.py with a different Python than what you are building for, which is
  handy for things like buildbots running in a virtualenv for one Python
  that need to be able to run builds for other versions too. 

  If build.py is still not able to find the correct Python given the M.N
  on the command line then you can specify the full path to the python
  executable you want to use with the ``--python`` option.

* **test**: Runs all of Phoenix's unittests.

* **--nodoc**: This option turns off the sphinx generator when running the
  etg scripts. If you don't plan on generating the documentation then this
  will speed up the proccessing of the etg command.

Please see the output of ``python build.py --help`` for information about
commands and options not mentioned here. And, as always, if there is any
discrepancy between this document and the source code in the build.py script,
then the source code is right. ;-)

The build.py script will download doxygen, sip and waf for your platform as
needed if they are not already in your Phoenix/bin folder. If prebuilt
versions of these tools are not available for your platform then build.py
will bail out with an error message. To continue with the build you will need
to acquire copies of the tool that will work on your platform and can then
tell build.py where to find it using an environment variable, as described in
the error message.



Project directory structure
----------------------------

There are a lot of subfolders in this directory, here is a brief
explanation to help a newbie find their way around.

* **build**: Intermediate files produced by the build process are stored 
  here. This folder should not be committed to a source repository.

* **buildtools**: This is a Python package containing modules that are used
  from build.py and setup.py and which assist with configuring and running
  the build.

* **etg**: This is where the Extractor-Tweaker-Generator scripts are stored
  (see the ProjectPhoenix link above.) These scripts are invoked by the build
  and they will read the XML files produced by Doxygen and will produce
  interface definition files for SIP.

* **etgtools**: This Python package contains modules which assist with the
  parsing of the XML files, tweaking the collection of objects produced by
  the parser, and also the backend generation of code or documentation.

* **sip/gen**: The code (.sip files) produced by the ETG scripts is placed
  in this folder.

* **sip/cpp**: The code produced when running SIP is put in this folder. It
  will be C++ source and header files, and also some extra files with
  information about the source files produced so the build knows what files
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
interface/wx/FOO.h and we are processing the XML produced for that file then
the ETG script for the classes and other items will be named etg/FOO.py and it
will produce sip/gen/FOO.sip, unit tests will be in unittests/test_FOO.py,
and so on.

In most cases more than one ETG/SIP file will be used to create a single
Python extension module. In those cases there will be one ETG script used to
bring all the others together into the single extension module (by using the
back-end generator's include feature for example.) The names of those scripts
will have a leading underscore, such as etg/_core.py, and all the scripts that
are intended to be included in that extension module should specify that name
in their MODULE variable.


Prerequisites
--------------

TBW

