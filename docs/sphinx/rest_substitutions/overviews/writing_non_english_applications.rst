.. include:: headings.inc


.. _writing non-english applications:

=====================================================
|phoenix_title|  **Writing Non-English Applications**
=====================================================

This article describes how to write applications that communicate with the
user in a language other than English. Unfortunately many languages use
different charsets under Unix and Windows (and other platforms, to make the
situation even more complicated). These charsets usually differ in so many
characters that it is impossible to use the same texts under all platforms.

The wxPython library provides a mechanism that helps you avoid distributing
many identical, only differently encoded, packages with your application
(e.g. help files and menu items in iso8859-13 and windows-1257). Thanks to
this mechanism you can, for example, distribute only iso8859-13 data and it
will be handled transparently under all systems.

Please read the :ref:`Internationalization <internationalization>` page which
describes the locales concept.

.. todo:: to be written (do we want to write it?!?!)

