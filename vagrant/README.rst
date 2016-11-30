Phoenix builds on various Linux distros with Vagrant
====================================================

Vagrant (https://www.vagrantup.com/) is a tool that enables creating and using
automated, relatively lightweight virtual environments.  Vagrant and the
Vagrant community provide several base images that are essentially simplistic
bare-bones installs of various operating systems, that can be thought of as a
bare canvas ready for provisioning with the needs of whatever applications
they will be used for.

For Phoenix, this means that we can automate the creation and provisioning of
virtual Linux machines with all the packages installed that are needed for
building Phoenix.  The subfodlers located in this folder contain the Vagrant
configurations and a bootstrap script for all of the Linux distros that we
currently support.


Setup
-----

The following steps should be followed to set up a computer to be a Vagrant
host:

  1. Install VirtualBox: https://www.virtualbox.org/wiki/Downloads

  2. Install vagrant: https://www.vagrantup.com/downloads.html

  3. Install the vagrant-vbguest plugin to keep the VirtualBox Guest Additions
     package installed and up to date. See: https://github.com/dotless-de/vagrant-vbguest
     and run::

         vagrant plugin install vagrant-vbguest


Building
--------

TBW...
