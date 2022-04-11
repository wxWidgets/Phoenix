# The base image
FROM fedora:29

# Set environment variables
ENV DIST_NAME=fedora-29
ENV USER=wxpy
ENV HOME=/home/$USER
ENV PYTHONUNBUFFERED=1
ENV PATH=$HOME/bin:$PATH
ENV GTK2_OK=no

# Update and install basic OS packages
RUN \
        dnf -y update; \
        dnf -y group install "Development Tools"; \
        dnf -y install gcc-c++ sudo nano; \
# Set up a user, and etc.
        mkdir -p /dist; \
        adduser -m ${USER}; \
        echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers; \
# Install development packages needed for building wxPython
        dnf install -y \
                freeglut-devel \
                gstreamer1-devel \
                gstreamer1-plugins-base-devel \
                gtk3-devel \
                libjpeg-turbo-devel \
                libnotify-devel \
                libpng-devel \
                libSM-devel \
                libtiff-devel \
                libXtst-devel \
                SDL-devel \
                webkit2gtk3-devel; \
# Install all available Python packages and their dev packages
        dnf -y install python2 python2-tools python2-devel python2-virtualenv; \
        dnf -y install python3 python3-tools python3-devel; \
        dnf -y install python36; \
# Clean up dnf caches
        dnf clean all;


# Set the user and group to use for the rest of the commands
USER ${USER}:${USER}

# Set the working directory
WORKDIR ${HOME}

# Create virtual environments for each Python
RUN \
        cd ${HOME}; \
        mkdir -p ${HOME}/venvs; \
        python3.6 -m venv venvs/Py36; \
        python3.7 -m venv venvs/Py37;

# Add files from host into the container
COPY scripts ${HOME}/bin

# Define default command
CMD ["/bin/bash", "-l"]

