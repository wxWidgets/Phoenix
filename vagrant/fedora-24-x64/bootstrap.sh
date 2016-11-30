#!/bin/bash

# Set up and update package repos
dnf -y update
dnf -y install yum-utils


# Install necessary development and other packages
dnf -y group install "Development Tools"

dnf -y install gtk2 gtk2-devel gtk3 gtk3-devel \
    webkitgtk webkitgtk-devel webkitgtk3 webkitgtk3-devel \
    libjpeg-turbo-devel libpng-devel libtiff-devel \
    SDL SDL-devel gstreamer gstreamer-devel gstreamer-plugins-base-devel \
    freeglut freeglut-devel libnotify libnotify-devel


# Install all available Python packages and their dev packages
dnf -y install python python-tools python-devel python-virtualenv
#dnf -y install python34 python34-tools python34-devel
dnf -y install python3 python3-tools python3-devel


# Set up virtual environments for each Python where the Phoenix builds will be done
virtualenv --python=python2.7 Py27
#pyvenv-3.4 Py34
pyvenv-3.5 Py35


