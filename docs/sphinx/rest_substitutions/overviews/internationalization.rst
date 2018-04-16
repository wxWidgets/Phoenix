.. include:: headings.inc


.. _internationalization:
.. _I18N:
.. _localization:
.. _L10N:


==================================================
|phoenix_title|  **Internationalization Overview**
==================================================

"Internationalization" (often referred to as i18n) is the process to change an
application so that all user visible texts are translated to the user selected
language and that things like dates, money amounts and numbers in general are
shown in a format the user is familiar with/or used to.

The easiest way to show what is needed is by using a little code sample.


Text translation
================

Prepare the source code
-----------------------

Text translation in Python is done using gettext [1]_ , to ensure that all
wxPython labels are also translated we will use :class:`wx.Locale` and
:func:`wx.GetTranslation` .

How to prepare your source code to enable translation of texts::

    aString = _(u"This is a string which will be translated")


As you can see it is very simple, you just enclose the text with the translation
function "_()", obviously there is a bit more to it, see below.

Enabling I18N for a whole application you would do some setup in the application
file along the following lines:

.. literalinclude:: _downloads/i18nwxapp/app_base.py
   :lines: 25-27


Here we setup the "_" translation function and making it available application
by adding it to builtin.

The code required to change to a different language is as follows:

.. literalinclude:: _downloads/i18nwxapp/app_base.py
   :pyobject: BaseApp.updateLanguage


Do the actual translation work
------------------------------

You need to extract all the text strings marked by the "_" function, a little
script `geni18n.py` is in the :download:`downloadable zip file <_downloads/i18nwxapp/i18nwxapp.zip>`,
it will extract all the strings and generate a ``.pot`` file, which is put to
the locale folder.  The `geni18n.py` script will also generate the ``.mo`` files
for defined languages.

The ``.pot`` file is then provided to the translators and they use it to
generate a ``.po`` file for the language they translate too or they can also use
the ``.pot`` file to merge new/changed text strings to an existing ``.po`` file.

To do the actual translation we recommend `poEdit` [2]_ , it allows you to
create or update a translation catalog (``.po`` file) from the ``.pot`` file.


Sample application
------------------

In the :download:`downloadable zip file <_downloads/i18nwxapp/i18nwxapp.zip>`
we included a small sample application showing the above in action.

- `app_base.py` contains the initialization code
- `sampleapp.py` is the main frame/application, just run this to see things in action
- `geni18n.py` is the script to generate the ``.pot`` file and it also generates the ``.mo`` files.

.. note::
   The application has a button which displays a file dialog, as wxPython uses
   a native widget for this the text are shown in the operating system language
   and not the language which is selected in `app_base.py`.


Localization overview
=====================

"Localization", often referred to as "L10n", is the process to adapt the display
of dates and numbers to local custom.

E.g. "4/5/2012" would for an American mean April 5. 2012, but for most Europeans
it would be 4. May 2012.


Localize dates
==============

.. todo:: to be written


Localize numbers
================

.. todo:: to be written


Additional resources
====================

- http://zetcode.com/wxpython/in18/
- http://wiki.wxpython.org/Internationalization
- http://en.wikipedia.org/wiki/Internationalization_and_localization


.. rubric:: Footnotes

.. [1] gettext - http://docs.python.org/library/gettext.html
.. [2] poEdit - http://www.poedit.net/