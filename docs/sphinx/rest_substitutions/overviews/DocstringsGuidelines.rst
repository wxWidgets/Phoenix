.. include:: headings.inc

.. highlight:: rst


.. _docstrings guidelines:

==================================================
|phoenix_title|  **Phoenix Docstrings Guidelines**
==================================================

This document gives a brief introduction about the current docstrings
standards in the Phoenix project. Most of the documentation in the
Phoenix core is automatically generated by parsing the wxWidgets XML
docs; however, Phoenix has its own pure-Python functions and classes
in at least two places:

* **Core Library**: examples include :ref:`wx.CallLater` and
  :func:`wx.date2pydate`, which require manual input of the
  documentation strings. This is achieved by editing the source Python
  files located in the ``etg`` folder in the Phoenix directory tree;

* **wx.lib**: the whole of ``wx.lib`` (and its sub-folders) is made up
  of pure-Python modules, often representing owner-drawn widgets which
  are not available as wrapped modules. Again, this requires manual
  editing of the source Python files.

This document is a starting point in setting some reasonable standards
on how the pure-Python docstrings may be edited and improved to make
the overall appearance of the Phoenix documentation consistent and
pleasant.


.. _info field lists:

Info Field Lists
----------------

`Info Field Lists` refer to the various options available while
documenting a method or a function, and in particular its parameters,
keywords, return type and possibly raised Python `Exceptions`.

Inside Python object description directives, reST field lists with
these fields are recognized and formatted nicely:

* ``param``, ``parameter``, ``arg``, ``argument``, ``key``,
  ``keyword``: Description of a parameter.

* ``type``: Type of a parameter.

* ``raises``, ``raise``, ``except``, ``exception``: That (and when) a
  specific exception is raised.

* ``var``, ``ivar``, ``cvar``: Description of a variable.

* ``returns``, ``return``: Description of the return value.

* ``rtype``: Return type.


The field names must consist of one of these keywords and an argument
(except for ``returns`` and ``rtype``, which do not need an
argument). This is best explained by an example::

    .. method:: Set3StateValue(self, state):

       Sets the checkbox item to the given `state`.

       :param `state`: can be one of: ``wx.CHK_UNCHECKED`` (check is
          off), ``wx.CHK_CHECKED`` (check is on) or
          ``wx.CHK_UNDETERMINED`` (check is mixed).
       :type `state`: integer

       :returns: ``True`` if the value was successfully set, ``False``
          otherwise.
       :rtype: bool

       :raise: `Exception` when the item is not a 3-state checkbox item.

|

This will render like this:

    .. method:: Set3StateValue(self, state):

       Sets the checkbox item to the given `state`.

       :param `state`: can be one of: ``wx.CHK_UNCHECKED`` (check is
          off), ``wx.CHK_CHECKED`` (check is on) or
          ``wx.CHK_UNDETERMINED`` (check is mixed).
       :type `state`: integer

       :returns: ``True`` if the value was successfully set, ``False``
          otherwise.
       :rtype: bool

       :raise: `Exception` when the item is not a 3-state checkbox item.


|

It is also possible to combine parameter type and description, if the
type is a single word, like this::

   :param integer `state`: can be one of: ``wx.CHK_UNCHECKED`` (check
      is off), ``wx.CHK_CHECKED`` (check is on) or
      ``wx.CHK_UNDETERMINED`` (check is mixed).


In general, the standards for the ``:param`` field are the following:

1. Do not use the ``@param`` construct, as I am not sure Sphinx and
   docutils understand it;

2. Always try and define the parameter type: if the parameter is
   another Phoenix class, you can simply write this::

       :param Point `pt`: the mouse pointer location.

   Or, alternatively::

       :param `pt`: the mouse pointer location.
       :type `pt`: Point


Similarly, for the ``:return:`` and ``:rtype:`` field, you may
consider doing the following:

1. Try and put double-backticks on words like ``True``, ``False``,
   ``None`` and the various Phoenix constants (i.e.,
   ``wx.TR_DEFAULT_STYLE``);

2. If you can't guess what a method function returns, just leave the
   ``:returns:`` and ``:rtype:`` fields blank.


.. seealso:: `Sphinx Info Field List <http://sphinx.pocoo.org/domains.html#info-field-lists>`_


.. _admonitions:

Admonitions
-----------

Admonitions are specially marked "topics" that can appear anywhere an
ordinary body element can.  They contain arbitrary body
elements. Typically, an admonition is rendered as an offset block in a
document, sometimes outlined or shaded, with a title matching the
admonition type. For example::

    .. warning:: I am a warning.


Will render as:

.. warning:: I am a warning.

|

Currently, the `sphinx_generator` tool recognizes the following
admonitions:

1. ``.. note::`` or ``:note:`` : simple annotations to make a
   particular comment/sentence stand out against the rest of the
   documentation strings for a particular class, method or function;

2. ``.. warning::`` : this admonition normally indicates a problem or
   a severe limitation of a method, class or function. In the Phoenix
   world, this may also indicate that a particular widget is not
   supported under one or more platforms;

3. ``.. wxdeprecated::`` : used to mark deprecated methods, classes or
   functions. Please avoid using ``.. deprecated``. ;

4. ``.. availability::`` : normally employed to make the user
   understand on which platform(s) a particular functionality is
   supported/available;

5. ``.. seealso::`` or ``:see:`` : added primarily to facilitate the
   browsing of the docs, this admonition should be employed every time
   you think a user may be interested in seeing a related/similar
   method or a function providing an alternative implementation;

6. ``.. todo::`` : used to mark incomplete methods/functions, or
   simply as a remainder for the user and the developer that some more
   functionality needs to be added.

You can put pretty much anything inside an admonition section, as long
as it is properly indented. The recommendation is to implement it like
this::

    .. note::

       The class :ref:`wx.TreeCtrl` can be used to display a tree, with these notes:

       - The note contains all indented body elements
         following.
       - It includes this bullet list.


|

Which will render as follows:

.. note::

   The class :ref:`wx.TreeCtrl` can be used to display a tree, with these notes:

   - The note contains all indented body elements
     following.
   - It includes this bullet list.



In addition to the aforementioned admonitions, you can also use the
default Sphinx directives like ``.. versionadded::`` and
``.. versionchanged::``, to highlight the fact that some method,
function or class has been added/modified starting with a particular
Phoenix version.


.. seealso:: `Sphinx Paragraph-level markup <http://sphinx.pocoo.org/markup/para.html>`_


.. _contributing samples:

Contributing Samples
--------------------

.. highlight:: python

If you wish to contribute a (short) sample to be included in the
documentation, please follow these conventions:

1. Name the snippet of code like ``wxmodule.classname.methodname.INTEGER.py``,
   i.e. if you wish to contribute 2 snippets about the
   :meth:`wx.CheckBox.SetValue` method, please name your snippet files
   like this:

   * ``wx.CheckBox.SetValue.1.py``
   * ``wx.CheckBox.SetValue.2.py``


2. At the very top of the snippet file (on the first line), put your
   name, or your alias, or anything you use as internet name preceded
   by a double-hash, i.e.:

   ``##Andrea Gavana``


   So that your source code looks more or less like this::

       ##Chris Barker
       #!/usr/bin/env python
       """
       A simple test of the GridBagSizer
       http://wiki.wxpython.org/index.cgi/WriteItYourself
       """

       # Whatever code here...
       def SendSizeEvent(self):
           self.AdjustMySize()



.. highlight:: rst

This snippet will end up in the snippets `contrib` folder, to
differentiate it from the snippets automatically generated when
parsing the wxWidgets C++ XML documentation.

Please keep the snippets as short as possible: they don't need to be
fully-runnable and self contained applications, they are simply meant
to show a particular/clever/unusual way of using a method, a class or
a function.

Please do submit the sample snippets to the
`wxWidgets/Phoenix Github repository <https://github.com/wxWidgets/Phoenix>`_
as PR (Pull Request).  The snippets should be placed in the source
tree in this folder:

    ``Phoenix/docs/sphinx/rest_substitutions/snippets/python/contrib``


.. _contributing screenshots:

Contributing Screenshots
------------------------

Currently Phoenix is relatively short of widgets screenshots,
especially on Linux/Mac platforms.

If you wish to contribute a screenshot of a widget to be included in
the documentation, please follow these conventions:

- If the widget is a class belonging to the main `wx` namespace,
  use the full class name in lower case (i.e., `wx.Frame` ==>
  `wx.frame.png`);

- If it belongs to a sub-namespace (i.e., `wx.dataview`, `wx.aui`,
  `wx.html` and so on), it should be named this way (examples):

  1) `wx.dataview.DataViewCtrl` ==> `wx.dataview.dataviewctrl.png`
  2) `wx.aui.AuiManager` ==> `wx.aui.auimanager.png`


Please submit the screenshots to the
`wxWidgets/Phoenix Github repository <https://github.com/wxWidgets/Phoenix>`_
as a PR (Pull Request). The screenshots should be placed in the
source tree in this folder:

    ``Phoenix/trunk/docs/sphinx/_static/images/widgets/fullsize``

Please make sure to put your images in the appropriate sub-folder,
depending on the platform you chose to take the screenshots on.

