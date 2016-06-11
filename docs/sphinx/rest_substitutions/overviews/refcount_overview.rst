.. include:: headings.inc


.. _reference counting:

=================================================
|phoenix_title|  **Reference Counting Overview**
=================================================


Why You Shouldn't Care About It
-------------------------------

Many of the C++ objects wrapped by wxPython use a technique known as
`reference counting`, also known as `copy on write` (COW). This means
that when an object is assigned to another, no copying really takes
place. Only the reference count on the shared object data is
incremented and both objects share the same data (a very fast
operation).

But as soon as one of the two (or more) objects is modified, the data
has to be copied because the changes to one of the objects shouldn't
be seen in the others. As data copying only happens when the object is
written to, this is known as COW.

What is important to understand is that all this happens absolutely
transparently to the class users and that whether an object is shared
or not is not seen from the outside of the class - in any case, the
result of any operation on it is the same.


Object Comparison
-----------------

The ``==`` and ``!=`` operators of the reference counted classes
always do a `deep comparison`. This means that the equality operator
will return true if two objects are identical and not only if they
share the same data.


Note that wxPython follows the STL philosophy: when a comparison
operator cannot be implemented efficiently (like for e.g.
:ref:`wx.Image`\ 's ``==`` operator which would need to compare the entire
image's data, pixel-by-pixel), it's not implemented at all.  That's
why not all reference counted classes provide comparison operators.


Also note that if you only need to do a shallow comparison between two
:ref:`wx.Object` derived classes, you should not use the ``==`` and
``!=`` operators but rather the :meth:`wx.Object.IsSameAs`\ () function.


Object Destruction
------------------

When a COW object destructor is called, it may not delete the data: if
it's shared, the destructor will just decrement the shared data's
reference count without destroying it. Only when the destructor of the
last object owning the data is called, the data is really
destroyed. Just like all other COW-things, this happens transparently
to the class users so that you shouldn't care about it.


List of Reference Counted Classes
---------------------------------

The following classes in wxPython have efficient (i.e. fast)
assignment operators and copy constructors since they are
reference-counted:

- :ref:`wx.AcceleratorTable`
- :ref:`wx.adv.Animation`
- :ref:`wx.Bitmap`
- :ref:`wx.Brush`
- :ref:`wx.Cursor`
- :ref:`wx.Font`
- :ref:`wx.GraphicsBrush`
- :ref:`wx.GraphicsContext`
- :ref:`wx.GraphicsFont`
- :ref:`wx.GraphicsMatrix`
- :ref:`wx.GraphicsPath`
- :ref:`wx.GraphicsPen`
- :ref:`wx.Icon`
- :ref:`wx.Image`
- :ref:`wx.msw.Metafile`
- :ref:`wx.Palette`


Note that the list above reports the objects which are reference
counted in all ports of wxPython; some ports may use this technique
also for other classes.
