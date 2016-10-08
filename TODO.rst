Phoenix TODO List
=================

This is just a place for me to jot down things as I think of them.
The items are in no particular order, and the fact that something is
on this list does not mean that it will ever actually be done.
Additionally, no meaning should be attached to items being removed
from this file, it could mean that items have been done or just that
I've decided that they will not be done or no longer apply.



Checklist for all new etg files
-------------------------------
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
      version.  For example, there may be additional C methods added
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




WAF Build
---------
Add support for using the cygwin and mingw32 compilers.


Stubs for Optional Classes
--------------------------

In Classic we tend to use empty stubs for classes and etc. that are optional
and not available in a particular build of wxWidgets.  That allows the
compilations to succeed without needing to completely eliminate those wrapper
classes, and when a user tries to use one of those classes they would get a
NotImplementedError.

The big downside of that approach was that the stubs had to be maintained by
hand, which is time consuming and error prone.  However for Phoenix we have
all the info about the API so we should be able to almost completely automate
the generation of the empty stub code for those classes.  ("Almost" because
we'll need to specify which classes to do it for, and what #define flag to
check if the the feature is available in wxWidgets or if the stubs should be
compiled.)


Sphinx tweaks
-------------

The big changes are done, but here are some dangling strings that still need
to be untangled:

  * The ``chopDescription()`` function is not very smart. See if it can be made a
    little smarter and pull out the first sentence from the docstring instead
    of just the first line.

  * Convert the main.html page to a ReST file? It would probably make it a
    little easier to maintain.

  * Set max width of body sections?  I think it looks a little nicer that way,
    but we'll need to fix the floating and alignment of the sidebar to do
    it...

  * If a method is renamed it is still in the sorted list of methods at the
    position that the original name would have sorted to.  Change things to
    sort on the pyName.

  * The sphinxtools are too aggressive at ignoring content beyond a #. If the
    hash happens to be inside a string then syntax related errors can happen.
    For example:

        def SetColors(self, pen='black', fill='#A0A0A0', fill2='#E0E0E0'):
            ...




Other Dev Stuff
---------------

  * Come up with some way to implement the MustHaveApp check that
    Classic does.  It should raise an exception when something is
    created/used that should not be done before there is an application
    object.

  * Locate and/or add items for the various functions and things in Classic's
    _functions.i module.

  * Add ETG scripts for these items in Classic's core:

      * msgout
      * quantize
      * dialup  ??
      * docmdi  ??
      * docview ??
      * persist ??

  * Add a _msw module that will contain classes and such that are only
    available in the Windows port:

      * [done] axbase
      * [done] metafile
      * [] wxCHMHelpController
      * [] access
      * [] New activex classes in wx/msw/ole/activex.h ?
      * Any others?

  * Add _aui module ??  (or go with only agw aui?)

  * Add the UTF8 PyMethods from classic (see _stc_utf8_methods.py) to StyledTextCtrl

  * Reimplement the classes in the valgen, valnum and valtext headers as
    Python code, and make them visible in the core wx namespace?

  * Should the demo/version.py file be maintained in the source repository?
    Or just let it always be generated like wx/__version__.py?

  * Should demo/Main.py ignore anything in the version strings after the '-'
    when comparing?



  * Potential reference count issue with wxGridCellCoordsArray?  Code
    like this::

        theGrid.GetSelectedCells()[0][0]

    evaluates to garbage values, but this works fine::

        a = theGrid.GetSelectedCells()
        a[0]
        a[0][0]

  * In a Py3 build strings like wx.TreeCtrlNameStr are being generated as
    bytes objects, they should probably be string objects. Or not, sip's
    default might be best... See ModuleDef.addGlobalStr if I change my mind.

  * Check gui_scripts entry points.

  * wx.Window.DoEraseBackground?


  * Add tests and/or demo for DnD in DataViewCtrl. Since the DnD is done
    internally and the DataViewEvent is used for passing the data objects
    around we may need to do something to help convert the raw data to python
    DataObjects.

  * Add meaningful __hash__ methods for wx.Colour, wx.Point, etc.?
    
  * Double-check wx.PyEvent and wx.PyCommandEvent, does the __getattr__,
    etc. work with properties?  See:
    https://groups.google.com/d/msg/wxpython-dev/dMrpaKs_d0U/nVMY7lMvAwAJ

  * In test_lib_agw_persist_persistencemanager.py change the tests to be
    self-contained instead of some relying on files generated by others. This
    won't work if we want to run tests in parallel.

  * Port these modules from gizmos in wxCode to a pure-python wx.lib implementation?
      * DynamicSashWindow
      * LEDNumberCtrl
      * SplitTree ??
      * TreeListCtrl ??  (We have a treelist ctrl in dataview now)

  * The Masked controls modules and demos need some help with Py3 compatibility.

