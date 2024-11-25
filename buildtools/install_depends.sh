#!/bin/sh
#
# This script is used by CI jobs to install the dependencies
# before building wxWidgets but can also be run by hand if necessary (but
# currently it only works for the OS versions used by the CI builds).
#
# WX_EXTRA_PACKAGES environment variable may be predefined to contain extra
# packages to install (in an OS-specific way) in addition to the required ones.

set -e

SUDO=sudo

case $(uname -s) in
    Linux)
        # Debian/Ubuntu
        if [ -f /etc/apt/sources.list ]; then
            run_apt() {
                echo "-> Running apt-get $@"

                # Disable some (but not all) output.
                $SUDO apt-get -q -o=Dpkg::Use-Pty=0 "$@"

                rc=$?
                echo "-> Done with $rc"

                return $rc
            }

            codename=$(lsb_release --codename --short)

            run_apt update || echo 'Failed to update packages, but continuing nevertheless.'

            extra_deps=""
            case "$codename" in
                focal|jammy)
                    extra_deps="$extra_deps libwebkit2gtk-4.0-dev"
                    ;;
                noble)
                    extra_deps="$extra_deps libwebkit2gtk-4.1-dev"
                    ;;
            esac

            pkg_install="\
                    freeglut3-dev \
                    libcurl4-openssl-dev \
                    libexpat1-dev \
                    libgl1-mesa-dev \
                    libglu1-mesa-dev \
                    libgtk-3-dev \
                    libjpeg-dev \
                    libnotify-dev \
                    libsdl2-dev \
                    libsm-dev \
                    libtiff-dev \
                    libxtst-dev \
                    libunwind-dev \
                    libgstreamer1.0-dev \
                    libgstreamer-plugins-base1.0-dev"

            pkg_install="$pkg_install ${WX_EXTRA_PACKAGES}"

            for pkg in $extra_deps; do
                if $(apt-cache pkgnames | grep -q $pkg) ; then
                    pkg_install="$pkg_install $pkg"
                else
                    echo "Not installing non-existent package $pkg"
                fi
            done

            if ! run_apt install -y $pkg_install; then
                exit 1
            fi
        fi
esac
