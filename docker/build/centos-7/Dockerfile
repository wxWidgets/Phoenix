# The base image
FROM centos:7

# Set environment variables
ENV DIST_NAME=centos-7
ENV USER=wxpy
ENV HOME=/home/$USER
ENV PYTHONUNBUFFERED=1
ENV PATH=$HOME/bin:$PATH
ENV GTK2_OK=yes


# Update and install basic OS packages
RUN \
        yum -y install https://repo.ius.io/ius-release-el7.rpm \
                https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm; \
        yum -y update; \
        yum -y group install development; \
        yum -y install sudo nano which; \
# Set up a user, and etc.
        mkdir -p /dist; \
        adduser -m ${USER}; \
        echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers; \
# Install development packages needed for building wxPython
        yum -y install \
                freeglut-devel \
                gstreamer1-devel \
                gstreamer1-plugins-base-devel \
                gtk2-devel \
                gtk3-devel \
                libjpeg-turbo-devel \
                libnotify \
                libnotify-devel \
                libpng-devel \
                libSM-devel \
                libtiff-devel \
                libXtst-devel \
                SDL-devel \
                webkitgtk-devel \
                webkitgtk3-devel \
                webkitgtk4-devel; \
# Install all available Python packages and their dev packages
        yum -y install python python-tools python-devel python-virtualenv; \
        yum -y install python36u python36u-tools python36u-devel; \
# Clean up the yum caches
        yum clean all;

# Set the user and group to use for the rest of the commands
USER ${USER}:${USER}

# Set the working directory
WORKDIR ${HOME}

# Create virtual environments for each Python
RUN \
        cd ${HOME}; \
        mkdir -p ${HOME}/venvs; \
        python3.6 -m venv venvs/Py36;

# Add files from host into the container
COPY scripts ${HOME}/bin

# Define default command
CMD ["/bin/bash", "-l"]

