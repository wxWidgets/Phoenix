Doodle
------

This little sample is a doodle application.  It shows you how to draw
on a canvas, deal with mouse events, popup menus, update UI events,
and much more.

    doodle.py	    A class for the main drawing window.  You can also
                    run it directly to see just this window.


    superdoodle.py  Takes the DoodleWindow from doodle.py and puts it
                    in a more full featured application with a control
                    panel, and the ability to save and load doodles.

    setup.py        This sample also shows you how to make your
                    applications automatically self-update when new
		    releases are available.  There is a bit of code in
                    the superdoodle module to use the softwareupdate
                    module from the library, but the real magic
                    happens here in the distutils setup module.
