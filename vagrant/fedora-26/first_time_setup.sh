#!/bin/bash

# This script is to be run after `vagrant up` failing
# with failure to setup shared folders.
#
# It downloads and installs Virtual Box Guest Additions.
#
# The commands are taken from instructions at
# https://www.vagrantup.com/docs/virtualbox/boxes.html
#
# Added Disable IPv6


if [ -s /home/vagrant/scripts/ ]  # No need to install VBoxGuestAdditions 
then
	exit 0
fi
if [ ! -s .first_time_setup_done ]  # reboot to activate new kernel
then
        echo "---------------PLEASE REBOOT FOR NEW KERNEL ----------------"
	echo "---------AND THEN RUN AGAIN 'vagrant provision'-------------"
fi

# Disable IPv6
echo "-------------------Disabling IPv6-------------------------"

echo 'net.ipv6.conf.all.disable_ipv6 = 1' >> /etc/sysctl.conf
echo 'net.ipv6.conf.default.disable_ipv6' >> /etc/sysctl.conf
echo 'net.ipv6.conf.lo.disable_ipv6 ' >> /etc/sysctl.conf
echo 'net.ipv6.conf.wlp3s0.disable_ipv6 ' >> /etc/sysctl.conf

sed -i -e 's/quiet splash/quiet splash ipv6.disable=1/g' /etc/default/grub
grub2-mkconfig -o /boot/grub2/grub.cfg

# Download, mount, install and delete VBoxGuestAdditions
echo "--Download, mount, install and delete VBoxGuestAdditions--"
dnf -y install kernel-devel wget
wget --no-verbose http://download.virtualbox.org/virtualbox/5.1.26/VBoxGuestAdditions_5.1.26.iso
sudo mkdir /media/VBoxGuestAdditions
sudo mount -o loop,ro VBoxGuestAdditions_5.1.26.iso /media/VBoxGuestAdditions
sudo sh /media/VBoxGuestAdditions/VBoxLinuxAdditions.run
rm VBoxGuestAdditions_5.1.26.iso
sudo umount /media/VBoxGuestAdditions
sudo rmdir /media/VBoxGuestAdditions
touch .first_time_setup_done
