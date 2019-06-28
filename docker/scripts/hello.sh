#!/bin/bash
echo "Hello World, from wxPython's build container on $DIST_NAME"
echo "    User:   " $(whoami)
echo "    ~/bin:  " $(ls ~/bin)
echo "    ~/venvs:" $(ls ~/venvs)
echo "    /dist:  " $(ls /dist)
echo ""

if [ -x /usr/bin/lsb_release ]; then
        /usr/bin/lsb_release -a
fi
