# The base image
FROM centos:8

# Set environment variables
ENV DIST_NAME=centos-8
ENV USER=wxpy
ENV HOME=/home/$USER
ENV PYTHONUNBUFFERED=1
ENV PATH=$HOME/bin:$PATH
ENV GTK2_OK=no


# Update and install basic OS packages
RUN \
#        yum -y install https://centos8.iuscommunity.org/ius-release.rpm; \
#        yum install \
#               https://repo.ius.io/ius-release-el8.rpm \
#               https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm; \
#        dnf config-manager --set-enabled PowerTools; \
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
                gtk3-devel \
                libjpeg-turbo-devel \
                libnotify \
                libnotify-devel \
                libpng-devel \
                libSM-devel \
                libtiff-devel \
                libXtst-devel \
                SDL-devel \
                webkit2gtk3-devel; \
# Install all available Python packages and their dev packages
        yum -y install python3 python3-tools python3-devel; \
        yum -y install python38  python38-devel; \
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
        python3.6 -m venv venvs/Py36; \
        python3.8 -m venv venvs/Py38;

# Add files from host into the container
COPY scripts ${HOME}/bin

# Define default command
CMD ["/bin/bash", "-l"]

