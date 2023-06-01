Manylinux build scripts for wxPython
====================================

The code in this folder can be used to build a manylinux version of wxPython.
This means that a single wxPython wheel can be used on more than a single Linux
distro like what we've been limited to so far. This is accomplished by including
in the wheel file the shared libraries for all of the dependencies of wxWidgets.
This is primarily the GTK3 libs and all of its dependencies, although there are
some others too.

In general this works, but it's not a perfect solution. Here are some potential
issues:

* Since the wheel has its own instance of GTK and other dependent libraries, the
  wheel file is quite large compared to one created specifically for the distro
  where it will be deployed. (Around 2+ times larger.)

* The private copy of the GTK libs will not play well with GTK themes and other
  resources that are installed on the system. In fact, there may be warnings
  printed indicating that "your installation may be broken."

* In order to get new enough versions of wxWidgets' dependencies, we need to use
  the newest (at the time of this writing) version of the manylinux images,
  resulting in the platform tag being set to "manylinux_2_28". In other words,
  the version of glibc on the target system needs to be >= 2.28, and the wheels
  will not work on older systems. A newish version of Pip is also required, one
  that recognizes this platform tag.

How to build
------------

Building is simple. You need a system with docker available, and you need a
wxPython sdist to be present in the ../dist folder. This makes it easy to build
using the exact same source code that was used to build already released
versions of wxPython, and also saves the time needed for the code generation
steps. The Python invoke package is also needed.

To start a build run a command like the following:

```
$ invoke build --pythons "3.8, 3.9, 3.10"
```

The resulting manylinux wheels will be moved to ../dist when they are done.
