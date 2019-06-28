#!/bin/bash
echo "Hello World, from wxPython's build container on $DIST_NAME"
echo "    User:   " $(whoami)
echo "    ~/bin:  " $(ls ~/bin)
echo "    ~/venvs:" $(ls ~/venvs)
echo "    /dist:  " $(ls /dist)
