#!/bin/bash

# Set up and update package repos
dnf -y update
dnf -y install yum-utils


# Install necessary development tools, libs, etc.
dnf -y group install "Development Tools"
dnf -y install gcc-c++

dnf -y install gtk2 gtk2-devel gtk3 gtk3-devel \
    webkitgtk webkitgtk-devel webkitgtk3 webkitgtk3-devel \
    libjpeg-turbo-devel libpng-devel libtiff-devel \
    SDL SDL-devel gstreamer gstreamer-devel gstreamer-plugins-base-devel \
    freeglut freeglut-devel libnotify libnotify-devel libSM-devel


# Install all available Python packages and their dev packages
dnf -y install python python-tools python-devel python2-virtualenv
#dnf -y install python34 python34-tools python34-devel
dnf -y install python3 python3-tools python3-devel

# Set up virtual environments for each Python where the Phoenix builds will be
# done. set them to the vagrant user so the venv's can be updated by pip later.
mkdir venvs
virtualenv --python=python2.7 venvs/Py27
#pyvenv-3.4 venvs/Py34
pyvenv-3.5 venvs/Py35
chown -R vagrant:vagrant venvs
