#!/bin/bash
echo "Hello World, from wxPython's build container on $DIST_NAME"
echo "    User:   " $(whoami)
echo "    ~/bin:  " $(ls ~/bin)
echo "    ~/venvs:" $(ls ~/venvs)
echo "    /dist:  " $(ls /dist)
echo "  GTK2_OK:  " $GTK2_OK
echo ""

if [ -x /usr/bin/lsb_release ]; then
        /usr/bin/lsb_release -a
fi
if [ -e /etc/redhat-release ]; then
        cat /etc/redhat-release
fi

echo ""
