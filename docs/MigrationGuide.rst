========================================
wxPython Project Phoenix Migration Guide
========================================

wxPython's Project Phoenix is a new incarnation of the wxPython
toolkit in which everything that existed before will be cast into the
flames in the hopes that that which emerges from the ashes will be
better, brighter, stronger and faster than before.  For more details
about why and how, please see the ProjectPhoenix_ pages in the
wiki.

.. _ProjectPhoenix: http://wiki.wxpython.org/ProjectPhoenix

This document will describe some of the incompatibilities that
programmers will run into when migrating code from Classic wxPython to
the Phoenix.  For some types of changes there won't be any attempt to
document the nitty gritty details of the differences, but rather the
general patterns of the changes will be documented.  Most programmers
should then be able to work out the details for themselves.

Please note that throughout this document and elsewhere in the project, as
well as community discussions and such, you may see the term "**Classic**"
used by itself. This refers to the original implementation of wxPython.
Likewise, a standalone "**Phoenix**" or "**Project Phoenix**" will generally
refer to this new implementation of wxPython.


Version Numbers
---------------

The version numbers for wxPython are no longer kept in sync with the wxWidgets
version number. In the past the common version number was used to indicate
exactly which version of wxWidgets should be used for the wxPython build. Now
wxWidgets is a git submodule, and the linked version is included in the
wxPython source tarball, so there is no longer any need to use the matching
version numbers to implicitly specify the version of the wxWidgets source to
use.

This means that wxPython can go back to a 3-component version number and follow
the common conventions used by 99% of the other software projects out there.
The 3 components are commonly called MAJOR, MINOR and RELEASE. Since wxPython
Phoenix is a major upgrade over wxPython Classic then we will start out with a
new MAJOR version number to help communicate that this isn't just a little
update from previous releases.

Additional flags will be appended to the version number in a manner that is
compliant with Python's PEP-440_. This includes syntax for alpha, beta,
release candidate releases, post-release builds, development snapshots, etc.
See ``buildtools/version.py`` in the Phoenix source tree for more details.

.. _PEP-440: https://www.python.org/dev/peps/pep-0440/


Overloaded Functions
--------------------

In order to support more than one of the versions of an overloaded C++
function or class method in Classic wxPython, we had to rename all but one of
them.  For example, for the C++ ``wxWindow::SetSize`` method we have
``SetSize``, ``SetDimensions``, ``SetRect`` and ``SetSizeWH``.  One of the
features of the new tools used for Project Phoenix is that we no longer need
to do that and instead we can have just one function or method in the Python
API and the proper version of the C++ function or method is chosen at runtime
based on the number and types of parameters passed to the function. So in most
cases the renamed versions of the overloaded functions have been removed and
you can call the function with the same name as the C++ API.

This also includes the default constructor for all widget classes, used for
the 2-phase create. Previously they were renamed to be the class name with
"Pre" prepended to it.  For example, ``wx.PreWindow()``, ``wx.PreFrame()``,
etc.  Now in the Phoenix build of wxPython that is no longer necessary and you
can just call the class with no parameters like normal.

For those renamed items that are more commonly used in the old Classic
wxPython I'll add some aliases that will issue a ``DeprecationWarning`` for
the first release or two after we switch over to the Phoenix version of the
code, and then remove them in a later release.


FindWindow Methods
------------------

One instance of undoing the renames for overloading done in Classic that may
be not make as much sense as the others is the ``wx.Window.FindWindow``
methods.  This is because there are new methods in Phoenix that have the same
names as some of the renames in Classic, so we can't just leave a deprecated
alias in place that will direct the programmer to use the overloaded version
of the method instead of the renamed version.

So we now have the following FindWindow-related methods and static methods
available in the ``wx.Window`` class:

These are non-static and do a recursive search in ``self``::

    wx.Window.FindWindow(self, id)
    wx.Window.FindWindow(self, name)

These are ``staticmethods`` that either search all windows in the application,
or the subtree rooted at ``parent`` if it is given::

    wx.Window.FindWindowById(id, parent=None)
    wx.Window.FindWindowByLabel(label, parent=None)
    wx.Window.FindWindowByName(name, parent=None)

And these extra module-level helper functions added in Classic are still
available in Phoenix::

    wx.FindWindowById(id, parent=None)
    wx.FindWindowByLabel(label, parent=None)
    wx.FindWindowByName(name, parent=None)




Static Methods
--------------

In the distant past when SWIG was generating wrapper code for C++ static
methods it would create a standalone function named ``ClassName_MethodName``
for it. When Python added support for static methods then SWIG was able to use
that to make a real ``staticmethod`` named ``ClassName.MethodName``, but it still
generated the standalone function named with the underscore, for
compatibility. That underscore version of the static methods is now gone, and
you will get an ``AttributeError`` in existing code that is using them. To fix
the problem simply change the underscore to a dot, for example you should
change this::

    c = wx.SystemSettings_GetColour(wx.SYS_COLOUR_MENUTEXT)

to this::

    c = wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUTEXT)

You can also make this change in your existing code that is using pre-Phoenix
versions of wxPython, in order to help you prepare for the transition.




Unicode and Auto-Converting Strings
-----------------------------------

Starting with the wxPython 2.9 release series, there are no longer separate
ansi/Unicode builds of wxPython.  All wxPython builds are now essentially the
same as the old Unicode builds. This means that all string objects (in Python
2.7) or bytes objects (Python 3+) passed to wx API functions or methods are
converted to Unicode before calling the C++ function or method.  By default
Classic wxPython would use the encoding specified by the locale that was
current at the time of the import of the wx module.

However using the default locale could sometimes cause issues because
it meant that slightly different encodings could be used on different
platforms, even in the same locale, or the program could end up using
an encoding in a different locale that the developer has not tested
their code with.

Project Phoenix takes this Unicode simplification one step further by
stipulating that only the utf-8 encoding will be used for
auto-converting string/bytes objects to the Unicode objects that will be
passed on to the wx APIs.  If you need to deal with text using a
different encoding then you will need to convert it to Unicode
yourself before passing the text to the wx API.  For the most part this
should not be much of a problem for well written programs that support
Unicode because they will typically only convert to/from Unicode when
reading/writing text to a file or database, and will use Unicode objects
throughout the rest of the code.  The common exception to this is that
string-literals are often used in the code for specifying labels,
etc. for UI elements.  If your text for the string literals in your
code are all ascii or utf-8 then you should not need to make any
changes at all.  If you have literals with some other encoding then
you'll need to deal with them one way or another, either change the
encoding of your source file to utf-8, or convert the literals from
your encoding to Unicode before passing the text to the wx API.

In Python 3.x, where strings are already Unicode objects, most of the above
confusion goes away, however if you have bytes objects then the same rules of
auto-converting only from utf-8 will still apply.


Font, Pen, and Brush Styles
---------------------------

The following aliases are currently added for backwards compatibility,
but will be removed in a future release.  You should migrate any code
that is using the old names to use the new ones instead::

            wx.DEFAULT    = wx.FONTFAMILY_DEFAULT
            wx.DECORATIVE = wx.FONTFAMILY_DECORATIVE
            wx.ROMAN      = wx.FONTFAMILY_ROMAN
            wx.SCRIPT     = wx.FONTFAMILY_SCRIPT
            wx.SWISS      = wx.FONTFAMILY_SWISS
            wx.MODERN     = wx.FONTFAMILY_MODERN
            wx.TELETYPE   = wx.FONTFAMILY_TELETYPE

            wx.NORMAL = wx.FONTWEIGHT_NORMAL
            wx.LIGHT  = wx.FONTWEIGHT_LIGHT
            wx.BOLD   = wx.FONTWEIGHT_BOLD

            wx.NORMAL = wx.FONTSTYLE_NORMAL
            wx.ITALIC = wx.FONTSTYLE_ITALIC
            wx.SLANT  = wx.FONTSTYLE_SLANT

            wx.SOLID       = wx.PENSTYLE_SOLID
            wx.DOT         = wx.PENSTYLE_DOT
            wx.LONG_DASH   = wx.PENSTYLE_LONG_DASH
            wx.SHORT_DASH  = wx.PENSTYLE_SHORT_DASH
            wx.DOT_DASH    = wx.PENSTYLE_DOT_DASH
            wx.USER_DASH   = wx.PENSTYLE_USER_DASH
            wx.TRANSPARENT = wx.PENSTYLE_TRANSPARENT

            wx.STIPPLE_MASK_OPAQUE = wx.BRUSHSTYLE_STIPPLE_MASK_OPAQUE
            wx.STIPPLE_MASK        = wx.BRUSHSTYLE_STIPPLE_MASK
            wx.STIPPLE             = wx.BRUSHSTYLE_STIPPLE
            wx.BDIAGONAL_HATCH     = wx.BRUSHSTYLE_BDIAGONAL_HATCH
            wx.CROSSDIAG_HATCH     = wx.BRUSHSTYLE_CROSSDIAG_HATCH
            wx.FDIAGONAL_HATCH     = wx.BRUSHSTYLE_FDIAGONAL_HATCH
            wx.CROSS_HATCH         = wx.BRUSHSTYLE_CROSS_HATCH
            wx.HORIZONTAL_HATCH    = wx.BRUSHSTYLE_HORIZONTAL_HATCH
            wx.VERTICAL_HATCH      = wx.BRUSHSTYLE_VERTICAL_HATCH



wx.PyDeadObjectError --> RuntimeError
-------------------------------------

Classic wxPython tracks when the C++ part of some types of objects (pretty
much just window types) is destroyed and then replaces the proxy object's
class with one that raises a ``wx.PyDeadObjectError exception``. SIP takes
care of that for us now in a much better way, so that custom hack is no longer
present in Phoenix, however a ``RuntimeError`` is the exception that is raised
now. The ``wx.Window`` class has a ``__nonzero__`` method that tests if the
C++ object has been deleted, so you can still test the window with an ``if``
or other conditional statement to see if it is safe to use, like this::

    if someWindow:
        someWindow.doSomething()



wx.PyAssertionError --> wx.wxAssertionError
-------------------------------------------

This is the exception raised when one of the ``wxASSERT`` (or similar)
statements in the wx C++ code fails. Since it is a wxWidgets assertion and not
a wxPython assertion the name was changed to make that a little more clear. A
compatibility alias exists so using ``wx.PyAssertionError`` will still work,
but you should migrate those uses to ``wx.wxAssertionError`` if possible.




The 'wx' namespace and submodules reorganized
---------------------------------------------

Some reorganization of what classes and functions goes in which internal wx
extension module has been done. In Classic the organization of the extension
modules was somewhat haphazard and chaotic. For example there were 5 separate
modules whose contents were loaded into the main "wx" package namespace and
several others that needed to be imported separately. However since there was
not much organization of the core the C++ wxadv and wxhtml DLLs would need to
be distributed with any applications built with a bundling tool even if the
application did not use any of those classes.

For Phoenix the location of the wrapper code for the classes and functions
will attempt to follow the same organization that wxWidgets uses for putting
those same classes and functions into DLLs or shared libraries. This means
that some things that were formerly in the core wx package namespace are no
longer there. They will have to be used by importing a wx submodule. Most of
them will be in the ``wx.adv`` module. One nice advantage of doing this is that
if your application is not using any of these lesser used classes then you
will not have to bundle the new modules (nor the associated wx DLLs) with
your application when you use py2exe or other executable builder.


wx.ListCtrl
-----------

In ``wx.ListItem`` and ``wx.ListEvent`` the ``"m_"`` properties are no longer
public. Instead use the associated getter/setter methods or the auto-generated
properties that are using them.



wx.TreeCtrl
-----------

The ``GetItemData`` and ``SetItemData`` now behave just like ``GetItemPyData``
and ``SetItemPyData`` did in Classic wxPython.  In other words, instead of
needing to create and use instances of ``wx.TreeItemData`` to associate Python
data objects with tree items, you just use the Python objects directly.  It
will also work when passing the data objects directly to the ``AppendItem``,
``InsertItem``, etc. methods.  (If anybody was actually using the
``wx.TreeItemData`` objects directly before and are unable to adapt then
please let Robin know.)  The ``[G|S]etItemPyData`` members still exist, but
are now deprecated aliases for ``[G|S]etItemData``.



wx.DragImage
------------

Phoenix is now providing both ``wx.DragImage`` and ``wx.GenericDragImage``
classes. Classic wxPython only provided ``wx.DragImage``, but it was actually
using ``wx.GenericDragImage`` internally for all platforms. ``wx.DragImage``
will now be a native implementation on Windows, and will still be the generic
version where a native implementation is not available. If you would rather
use the generic implementation on Windows too then switch to using the
``wx.GenericDragImage`` class name.


2-Phase Create
--------------

In Classic wxPython we had to do some fancy footwork to make use of
wxWidget's 2-Phase Create scheme for creating instances of a C++ widget
class, but delaying the creation of the UI object until later. (This is
needed for things like setting extended style flags that can not be set after
creation, or with class factories like XRC.) The old trickery should no
longer be needed, and instead you can write code that is much more sane. For
example, instead of Classic code like this::

    class MyDialog(wx.Dialog):
        def __init__(self, parent, ID, title):
            pre = wx.PreDialog()
            pre.SetExtraStyle(wx.FRAME_EX_CONTEXTHELP)
            pre.Create(parent, ID, title)
            self.PostCreate(pre)                           # 4

In Phoenix that should now be done like this::

    class MyDialog(wx.Dialog):
        def __init__(self, parent, ID, title):
            wx.Dialog.__init__(self)                       # 1
            self.SetExtraStyle(wx.FRAME_EX_CONTEXTHELP)    # 2
            self.Create(parent, ID, title)                 # 3


Notice that we are (#1) calling the base class ``__init__`` like usual, but
passing no parameters so the default C++ constructor will be invoked. Next
(#2, #3) we use ``self`` instead of ``pre`` because ``self`` is now a legitimate
instance of ``wx.Dialog``, and (#4) there is no longer any need to call
``PostCreate`` to do its black magic for us because there is no longer a rogue
instance that needs to be transplanted into ``self``.



wx.Image and Python Buffer Objects
----------------------------------

``wx.Image`` is now using the new buffer APIs for the constructors and methods
which accept any object supporting the buffer protocol.  These are methods
which allow you to set the raw RGB or Alpha data in the image in one step.  As
a consequence of using the new APIs the objects passed must also implement the
new buffer interface in order to be compatible.

``GetData`` and ``GetAlpha`` now return a copy of the image data as a
``bytearray`` object instead of a string object.  This means that since
``bytearrays`` are mutable you can do things like make changes to the data and
then use it in the ``SetData`` of another image.

``GetDataBuffer`` and ``GetAlphaBuffer`` now return ``memoryview`` objects,
which allow direct access to the RGB and Alpha buffers inside the image. Just
as in Classic you should not use those ``memoryview`` buffers after the
``wx.Image`` has been destroyed.  Using the returned ``memoryview`` object you
can manipulate the RGB or Alpha data inside the ``wx.Image`` without needing
to make a copy of the data.

Just as in Classic the ``SetDataBuffer`` and ``SetAlphaBuffer`` methods allow
you to tell the ``wx.Image`` to use memory buffers in other objects (such as a
numpy array) as its RGB or Alpha data, as long as the other object supports
the new buffer protocol.



wx.DropSource
-------------

We don't (yet) have an easy way to support different APIs per platform in the
wx class constructors, so ``wx.DropSource`` (which optionally takes parameters
that should be a ``wx.Icon`` on wxGTK or a ``wx.Cursor`` on the other
platforms) has been changed to not accept the cursor/icon in the constructors.
Instead you'll have to call either ``SetCursor`` or ``SetIcon`` depending on
the platform.



wx.DataObject and derived classes
---------------------------------

The ``wx.DataObject`` and ``wx.DataObjectSimple`` classes can now be
subclassed in Python.  ``wx.DataObject`` will let you provide complex
multi-format data objects that do not need to copy the data until one of the
formats is requested from the clipboard or a DnD operation.
``wx.DataObjectSimple`` is a simplification that only deals with one data
format, (although multiple objects can still be provided with
``wx.DataObjectComposite``.)

Python buffer objects are used for transferring data to/from the clipboard or
DnD partner.  Anything that supports the buffer protocol can be used for
setting or providing data, and a ``memoryview`` object is created for the APIs
where the data object should fetch from or copy to a specific memory location.
 Here is a simple example::

        class MyDataObject(wx.DataObjectSimple):
            def __init__(self, value=''):
                wx.DataObjectSimple.__init__(self)
                self.SetFormat(wx.DataFormat("my data format"))
                self.myData = bytes(value)

            def GetDataSize(self):
                return len(self.myData)

            def GetDataHere(self, buf):
                # copy our local data value to buf
                assert isinstance(buf, memoryview)
                buf[:] = self.myData
                return True

            def SetData(self, buf):
                # copy from buf to our local data value
                assert isinstance(buf, memoryview)
                self.myData = buf.tobytes()
                return True



Multiple Inheritance
--------------------

The SIP tool currently does not support having more than one wrapped C++ class
as the base classes of a Python class.  In most cases this is not a problem
because in wxPython you're more likely to use multiple inheritance with simple
mix-in classes or similar constructs than needing to inherit from more than
one wrapped C++ class.

However there is at least one use case where that can be a problem, and that
is with the ComboCtrl's ``wx.ComboPopup`` class.  In wxWidgets and also in
Classic you're encouraged to use ``wx.ComboPopup`` as a mix-in class combined
with the widget class that is going to be your popup window for the
``wx.ComboCtrl``.  This can not currently be done with Phoenix in the same
way, but you can also use a widget class with a ``wx.ComboPopup`` in a has-a
relationship rather than an is-a relationship.  See
``samples/combo/combo1.py`` for an example.



XRC
---

The "``LoadOnFoo``" methods of the ``XmlResource`` class were renamed
overloads of the corresponding "``LoadFoo``" methods. Since we no longer need
to rename overloaded methods the "``LoadOn``" version has been removed and you
should just use the "``LoadFoo``" version instead. These methods are used to
load some XRC content onto an existing window, such as a ``wx.Frame``, instead
of creating a new ``wx.Frame`` for the content.



wx.PyEvent and wx.PyCommandEvent
--------------------------------

Unlike most other ``wx.Py*`` classes these two still exist in Phoenix, and are
still the base classes that you should use when creating your own custom event
classes. For the most part they work just like they did in Classic, and they
take care of ensuring that any Python attributes that you assign to instances
of the class will still be there when the event is delivered to an event
handler. There is one main difference from Classic however, and that is that
those attributes are now stored in a dictionary object owned by the C++
instance, instead of being stored directly in the Python instance's
dictionary. In most cases this won't matter to you at all, but if your derived
class has a ``__getattr__`` method (or ``__setattr__``, or ``__delattr__``)
then you will need to get the attributes from that other dictionary instead.
You can get a reference to that dictionary using ``_getAttrDict()``. For
example::

    def __getattr__(self, name):
        d = self._getAttrDict()
        if name in d:
            return d[name]
        return doSomethingElse(name)



MakeModal
---------

Since it is usually not a good idea to make arbitrary top-level windows be
modal, (you should normally just use a ``wx.Dialog`` instead,) the
``wx.Frame.MakeModal`` method has been removed. The recommended alternative is
to use the ``wx.WindowDisabler`` class instead, but if you prefer the
semantics of having a method to call to turn on or off the modalness of a
window then you can add a method like this to your classes to give you a way
to do it::

    def MakeModal(self, modal=True):
        if modal and not hasattr(self, '_disabler'):
            self._disabler = wx.WindowDisabler(self)
        if not modal and hasattr(self, '_disabler'):
            del self._disabler



The wxversion module
--------------------

The ``wxversion`` module is gone, and will not be coming back.  The old way of
handling multi-version installs and choosing between them was a giant hack in
my opinion, and I regretted doing it shortly after it was implemented.  However
since there wasn't any other way that made sense at the time, and since some
people were using it already, it got left in the distribution.  But one of the
purposes of the Phoenix project is to remove as many of the hacks and cruft
from Classic as possible, so wxversion is gone.

These days there are **much** better ways to handle the things that the old
multi-versioning and version selection features that the ``wxversion`` module
provided.  Since wxPython Phoenix is built by default to be self-contained and
relocatable on all of the platforms, then unlike Classic there is no problem
with installing it in Python virtual environments.  So if you need to have
multiple versions of wxPython on your system, then create a virtual
environment for each project and install the version that each needs in their
environments.  If you have code that requires a specific version or range of
versions of wxPython then define the dependency in your ``setup.py`` file or a
``requirements.txt`` file and let ``pip`` take care of the details.  I'm
confident that you'll be much happier with this approach.



Property Grid
-------------

In Classic, custom classes derived from ``wx.propgrid.PGProperty`` could
specify which editor to use by providing a ``GetEditor`` method that returned a
string.  This method does not exist in C++, and was hacked in to the Python
wrapper classes in order to remove or simplify other wrapper related problems.

Those problems are no longer present in Phoenix and so it is easiest to go
back to the way C++ handles selecting the cell editor and avoid needing to
awkwardly kludge things together in order to maintain full compatibility.  If
you have a property class that implements the ``GetEditor`` method then adding
the following method to your property class will enable the propgrid to fetch
the editor instance properly::

    def DoGetEditorClass(self):
        return wx.propgrid.PropertyGridInterface.GetEditorByName(self.GetEditor())



wx.gizmos
---------

The ``wx.gizmos`` module in Classic was a set of wrappers around some
3rd-party C++ classes. Unfortunately that code has started rotting a little
since it has been unmaintained for a while. Instead of perpetuating this
problem into Phoenix the C++ wrappers have been tossed out and some of the
more commonly used classes from wx.gizmos has been ported to pure Python code,
which now lives in the ``wx.lib.gizmos`` package. There is also a temporary
``wx.gizmos`` module provided in order to provide the class names at the old
location too in order to ease transitioning to the new package. Please migrate
your code to use ``wx.lib.gizmos`` as ``wx.gizmos`` will likely go away in a
future release.

Please note that the new ``TreeListCtrl`` class is actually a thin wrapper
around AGW's ``HyperTreeList`` class since it was already a near perfect
superset of the old TreeListCtrl features and API. One compatibility
difference that may arise is that like most widgets in the AGW library the
style flags have been split into 2 parameters, ``style`` and ``agwSgtyle``,
but it should be a simple matter of changing existing code to pass the
tree-specific style flags in the ``agwStyle`` parameter, and wxWidgets common
style flags in the ``style`` parameter.


wx.lib.pubsub is deprecated
---------------------------

Although it originally started as part of this project, for a long time the
content of the ``wx.lib.pubsub`` package has been coming from a fork of the
original, called PyPubSub. It's all the same code, but with just a different
access path. However, now that Python 2.7 support in PyPubSub is no longer being
maintained in the latest versions, it is now time for wxPython to disconnect
itself in order to not have to remain on the older version. This means that
``wx.lib.pubsub`` is now deprecated.

Switching to the official PyPubSub is simple however, just install the package::

    pip install -U PyPubSub==3.3.0

And then change your import statements that are importing
``wx.lib.pubsub.whatever``, to just import ``pubsub.whatever`` instead. If you
are using Python3 and would like the newest version of PyPubSub then you can
drop the version number from the pip command above.


wx.html.HtmlWindow.OnOpeningURL
-------------------------------

In wxPython Classic the return value of ``wx.html.HtmlWindow.OnOpeningURL`` and
``wx.html.HtmlWindowInterface.OnHTMLOpeningURL`` could be either a value from the
``wx.html.HtmlOpeningStatus`` enumeration, or a string containing the URL to
redirect to.

In Phoenix this has been changed to a simpler wrapper implementation which
requires that both an enum value and a string be returned as a tuple. For
example::

    def OnHTMLOpeningURL(self, urlType, url):
        if urlType == wx.html.HTML_URL_IMAGE and url != self.otherURL:
            return (wx.html.HTML_REDIRECT, self.otherURL)
        return (wx.html.HTML_OPEN, "")


wx.NewId is deprecated
----------------------

:func:`wx.NewId` has been used forever in wxWidgets and wxPython to generate an
ID for use as the ID for controls, menu items, and similar things. It's really
quite a stupid implementation however, in that it simply increments a counter
and returns that value. There is no way for it to check if the ID is already in
use, for example if the programmer used some static numbers for IDs, or if the
counter wrapped around the max integer value and started over at the min integer
value.

So a few years ago the wxWidgets team implemented a reference counting scheme
for the ID values, and started using it internally. In a more recent release the
``wx.NewId`` function was deprecated. Then, even more recently, when code
was added to Phoenix's generator tools to automatically deprecate things that
are marked as deprecated in wxWidgets, then it became deprecated for us too.

The recommended alternative to ``wx.NewId`` is to just use ``wx.ID_ANY`` when
creating your widgets or other items with IDs. That will use the reference
counted ID scheme internally and the ID will be reserved until that item is
destroyed. In those cases where you would prefer to have items with the same ID,
or to reuse ID values for some other reason, then you should use the
:func:`wx.NewIdRef` function instead. It returns a :class:`wx.WindowIDRef`
object that can be compared with each other, sorted, used as a dictionary key,
converted to the actual integer value of the ID, etc.


wx.WS_EX_VALIDATE_RECURSIVELY is obsolete
-----------------------------------------

The wx.WS_EX_VALIDATE_RECURSIVELY extended style flag is obsolete, as it is
now the default (and only) behavior. The style flag has been added back into
wxPython for compatibility, but with a zero value. You can just stop using it
in your code with no change in behavior.


Parameter name changes in radial gradient methods
-------------------------------------------------

The parameter names for the ``wx.GraphicsContext`` methods for creating radial
gradients have changed in wxPython 4.1 to be a little more understandable. If
you are passing these values via their keyword names then you will need to
change your code. The prior C++ method signatures looked like this::

    virtual wxGraphicsBrush
    CreateRadialGradientBrush(wxDouble xo, wxDouble yo,
                              wxDouble xc, wxDouble yc,
                              wxDouble radius,
                              const wxGraphicsGradientStops& stops);

And they now look like this::

    virtual wxGraphicsBrush
    CreateRadialGradientBrush(wxDouble startX, wxDouble startY,
                              wxDouble endX, wxDouble endY,
                              wxDouble radius,
                              const wxGraphicsGradientStops& stops,
                              const wxGraphicsMatrix& matrix = wxNullGraphicsMatrix);



Possible Locale Mismatch on Windows
-----------------------------------

On the Windows platform, prior to Python 3.8, it appears that Python did not do
any initialization of the process locale settings, at least for the "en_US"
based locales. For example, in Python 3.7::

    >>> import locale
    >>> locale.getdefaultlocale()
    ('en_US', 'cp1252')
    >>> locale.getlocale()
    (None, None)

And in Python 3.8::

    >>> import locale
    >>> locale.getdefaultlocale()
    ('en_US', 'cp1252')
    >>> locale.getlocale()
    ('English_United States', '1252')

Now, when you add in the wxWidgets class wxLocale, then it can get even more
confusing on Windows. It seems that this boils down to wxWidgets setting the
locale using a Windows-specific name like "en-US" (with a hyphen instead of an
underscore). Since Python's locale module does not recognize this as a
legitimate locale alias, then calling `locale.getlocale()` after a `wx.Locale`
has been created will result in a `ValueError` exception.

So wxPython has added code in the `wx.App` class to try and set up the locale so
both Python and wxWidgets are set to equivalent settings. This is still somewhat
experimental however, and the implementation in wxPython 4.1.0 is still
problematic in some cases. If you have problems with it then you can disable or
change this code by overriding the `wx.App.InitLocale` method in a derived
class. It can either just do nothing, or you can implement some alternative
locale setup code there.

There will be a new implementation of `InitLocale` in 4.1.1 which should be
simpler and less likely to still have problems. But you'll still be able to
override `InitLocale` if needed.



Sizer item flags validation
---------------------------

Starting with wxPython 4.1, wxWidgets is now validating the flags passed
when adding items to a sizer, to ensure that they are the correct flags for
the type of the sizer. If the given flags do not make sense, for example using
horizontal alignment flags in a horizontal box sizer, then a wxAssertionError
error is raised.



CheckListCtrlMixin Redundancy
-----------------------------

The wx.lib.mixins.listCtrl.CheckListCtrlMixin is now obsolete because
wx.ListCtrl has new functionality which does pretty much the same thing. In
fact there is some overlap in method names which may trip up some use cases.
It is advised to drop the use of CheckListCtrlMixin and just use the
wx.ListBox functionality. You will need to call EnableCheckBoxes to turn it on,
and you may need to change some event handlers or overloaded methods.



.. toctree::
   :maxdepth: 2
   :hidden:


