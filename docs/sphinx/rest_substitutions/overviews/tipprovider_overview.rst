.. include:: headings.inc


.. _tipprovider overview:

==========================================
|phoenix_title|  **TipProvider Overview**
==========================================

Many "modern" Windows programs have a feature (some would say
annoyance) of presenting the user tips at program startup.

While this is probably useless to the advanced users of the program,
the experience shows that the tips may be quite helpful for the
novices and so more and more programs now do this. For a wxPython
programmer, implementing this feature is extremely easy. To show a
tip, it is enough to just call :func:`wx.ShowTip` function like this::

    if showTipsAtStartup:

        tipProvider = wx.CreateFileTipProvider("tips.txt", 0)
        wx.ShowTip(windowParent, tipProvider)
        del tipProvider


Of course, you need to get the text of the tips from somewhere - in
the example above, the text is supposed to be in the file `tips.txt`
from where it is read by the tip provider. The tip provider is just an
object of a class deriving from :class:`~wx.adv.TipProvider`.  It has
to implement one pure virtual function of the base class, `GetTip`. In
the case of the tip provider created by
:func:`wx.CreateFileTipProvider`, the tips are just the lines of the
text file.

If you want to implement your own tip provider (for example, if you
wish to hardcode the tips inside your program), you just have to
derive another class from :class:`~wx.adv.TipProvider` and pass a
pointer to the object of this class to func:`wx.ShowTip` - then you
don't need :func:`wx.CreateFileTipProvider` at all.

You will probably want to save somewhere the index of the tip last
shown - so that the program doesn't always show the same tip on
startup. As you also need to remember whether to show tips or not (you
shouldn't do it if the user unchecked "Show tips on startup" checkbox
in the dialog), you will probably want to store both the index of the
last shown tip (as returned by
:meth:`~wx.adv.TipProvider.GetCurrentTip` and the flag telling whether
to show the tips at startup at all.

In a `tips.txt` file, lines that begin with a ``#`` character are
considered comments and are automatically skipped. Blank lines and
lines only having spaces are also skipped.

You can easily add runtime-translation capacity by placing each line
of the `tips.txt` file inside the usual translation function. For
example, your `tips.txt` file would look like this::

    _("This is my first tip")
    _("This is my second tip")


Now add your `tips.txt` file into the list of files that gettext
searches for translatable strings. The tips will thus get included
into your generated .po file catalog and be translated at runtime
along with the rest of your application's translatable strings.

.. note::

   Each line in the `tips.txt` file needs to strictly begin with
   exactly the 3 characters of underscore-parenthesis-doublequote, and
   end with doublequote-parenthesis, as shown above. Also, remember to
   escape any doublequote characters within the tip string with a
   backslash-doublequote.

