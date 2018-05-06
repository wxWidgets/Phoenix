#!/bin/bash

# Set up and update package repos
add-apt-repository ppa:deadsnakes/ppa
apt update

# Install necessary development tools, libs, etc.
apt install -y build-essential dpkg-dev
apt install -y aptitude mc

apt install -y libgtk2.0-dev libgtk-3-dev
apt install -y libjpeg-dev libtiff-dev \
	libsdl1.2-dev libgstreamer-plugins-base1.0-dev \
	libnotify-dev freeglut3 freeglut3-dev libsm-dev \
	libwebkitgtk-dev libwebkitgtk-3.0-dev


# Install all available Python packages and their dev packages
apt install -y python2.7 python2.7-dev libpython2.7-dev python-virtualenv
apt install -y python3.6 python3.6-dev libpython3.6-dev python3.6-venv
apt install -y python3.7 python3.7-dev libpython3.7-dev python3.7-venv

# Set up virtual environments for each Python where the Phoenix builds will be
# done. set them to the vagrant user so the venv's can be updated by pip later.
mkdir venvs
virtualenv --python=python2.7 venvs/Py27
python3.6 -m venv venvs/Py36
python3.7 -m venv venvs/Py37

chown -R vagrant:vagrant venvs

