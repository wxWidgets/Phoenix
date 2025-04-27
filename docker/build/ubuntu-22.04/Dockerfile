# The base image
FROM ubuntu:22.04

# Set environment variables
ENV DIST_NAME=ubuntu-22.04
ENV USE_DEADSNAKES=yes
ENV USER=wxpy
ENV HOME=/home/$USER
ENV PYTHONUNBUFFERED=1
ENV PATH=$HOME/bin:$PATH
ENV GTK2_OK=no
ENV DEBIAN_FRONTEND=noninteractive

# Update and install basic OS packages
RUN \
        apt-get update; \
        apt-get upgrade -y; \
        apt-get install -y \
                apt-utils \
                build-essential \
                software-properties-common \
                sudo nano; \
        echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections; \
# Set up a user, and sudo
        mkdir -p /dist; \
        adduser --disabled-password --gecos "" ${USER}; \
        echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers; \
# Set a timezone
        apt-get install -y tzdata; \
        ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime; \
        dpkg-reconfigure -f noninteractive tzdata; \
# Install development packages needed for building wxPython
        apt-get install -y \
                freeglut3 \
                freeglut3-dev \
                libgl1-mesa-dev \
                libglu1-mesa-dev \
                libgstreamer-plugins-base1.0-dev \
                libgtk-3-dev \
                libjpeg-dev \
                libnotify-dev \
                libsdl2-dev \
                libsm-dev \
                libtiff-dev \
                libwebkit2gtk-4.0-dev \
                libxtst-dev; \
        apt-get clean;

# Install all available Python packages and their dev packages
RUN \
        if [ ${USE_DEADSNAKES} = yes ]; then add-apt-repository ppa:deadsnakes/ppa; apt-get update; fi; \
        apt-get install -y python3.8 python3.8-dev libpython3.8-dev python3.8-venv; \
        apt-get install -y python3.9 python3.9-dev libpython3.9-dev python3.9-venv; \
        apt-get install -y python3.10 python3.10-dev libpython3.10-dev python3.10-venv; \
        apt-get install -y python3.11 python3.11-dev libpython3.11-dev python3.11-venv; \
        apt-get clean;

# Add files from host into the container
COPY scripts ${HOME}/bin
RUN chown -R ${USER}:${USER} ${HOME}/bin

# Set the user and group to use for the rest of the commands
USER ${USER}:${USER}

# Set the working directory
WORKDIR ${HOME}

# Create virtual environments for each Python
RUN \
        cd ${HOME}; \
        mkdir -p ${HOME}/venvs; \
        python3.8 -m venv venvs/Py38; \
        python3.9 -m venv venvs/Py39; \
        python3.10 -m venv venvs/Py310; \
        python3.11 -m venv venvs/Py311;

# Define default command
CMD ["/bin/bash", "-l"]

