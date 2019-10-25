#!/bin/bash

# Set up and update package repos
yum -y install yum-utils
yum -y install https://centos7.iuscommunity.org/ius-release.rpm
yum -y update


# Install necessary development tools, libs, etc.
yum -y group install development

yum -y install gtk2 gtk2-devel gtk3 gtk3-devel \
    webkitgtk webkitgtk-devel webkitgtk3 webkitgtk3-devel \
    libjpeg-turbo-devel libpng-devel libtiff-devel \
    SDL SDL-devel gstreamer gstreamer-devel gstreamer-plugins-base-devel \
    freeglut freeglut-devel libnotify libnotify-devel libSM-devel


# Install all available Python packages and their dev packages
yum -y install python python-tools python-devel python-virtualenv
yum -y install python35u python35u-tools python35u-devel
yum -y install python36u python36u-tools python36u-devel


# Set up virtual environments for each Python where the Phoenix builds will be
# done. Set them to the vagrant user so the venvs can be updated by pip later.
mkdir venvs
virtualenv --python=python2.7 venvs/Py27
pyvenv-3.5 venvs/Py35
python3.6 -m venv venvs/Py36
chown -R vagrant:vagrant venvs
