Extractor, Tweaker, Generator Scripts
=====================================

What is this stuff?
-------------------

This directory contains Extractor-Tweaker-Generator (ETG) scripts which are
used to drive the process of converting the wxWidgets Doxygen XML files into
the files that will be fed to the bindings generator tool (SIP).

They are each standalone Python scripts (although some refer to others) which
process the incoming XML for one or more wxWidgets classes, (that is the
"extractor" part). That XML data is converted to a hierarchy of objects that
describe the various components of the API (classes, methods, parameters,
etc.)

Since C++ and Python are different then there are some things which do not
match perfectly when implementing wrappers of API elements, and we need to do
some adaptation of the API to make things work. This is the "tweaker" part of
these scripts, and is typically the bulk of the content of the scripts.  The
objects created by the extractor have methods that help facilitate these
tweaks, and it is also possible to add new elements as well, when appropriate.

The last thing these scripts do is hand off the tweaked objects to the active
generators which will traverse the object tree and generate code as needed.


Checklist for all new etg files
-------------------------------

    * Use the bin/make-new-etg-file.py script to create a new boilerplate etg
      and unittest files for you. In simplest cases all you'll do after that is
      add the class names to be processed, and add some unittest code for it.

    * Use a filename that matches the wxWidgets/interface/wx file name
      that the classes and other stuff is being loaded from.  This
      means that there will be lots of very small files in etg, but it
      will help to find the interface header source to compare what is
      being declared there with what is being generated, and to better
      understand what may need tweaked in the etg script file.

    * Read the corresponding interface file and ensure that all classes
      declared in it are listed in the ITEMS list in the etg file,
      unless the class should not be wrapped for some reason.  Other
      items from the interface file will be included automatically.

    * Do not list classes from other interface files in the etg file.

    * Check for any extras added to each class in Classic wxPython and
      evaluate whether the same extras should be added to the Phoenix
      version.  For example, there may be additional methods added
      on to the class with %extend or %pythoncode that need to be
      carried over to Phoenix, such as __nonzero__, etc.  Also look
      for methods where Classic indicates that ownership should be
      transferred, or other special directives.

    * Check for backwards compatibility issues with Classic wxPython
      and document in the MigrationGuide. Compatibility issues
      resulting from not renaming all the overloads can probably be
      left undocumented, we'll probably be adding some of them back as
      deprecated methods eventually, and the programmers should be
      able to figure out the rest once they've started porting some
      code.

    * For window classes check if there are other virtual methods
      besides those added in addWindowVirtuals() that should be
      unignored.

    * UNITTESTS!  Create a unit test script in the unittests folder
      using the same base file name.  It should at least check that
      every non-abstract class can be constructed, and should also
      have tests for things that are added or tweaked in the etg
      script.  Other things that needed no tweaks are ok to be left
      untested for the time being, although porting over some of the
      the old unittest code from Classic would also be a good idea, but
      priority should be given to testing those things that had to be
      tweaked or added.

