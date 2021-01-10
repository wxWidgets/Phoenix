# The base image (v16.04 == "xenial")
FROM ubuntu:16.04

# Set environment variables
ENV DIST_NAME=ubuntu-16.04
ENV USE_DEADSNAKES=yes
ENV USER=wxpy
ENV HOME=/home/$USER
ENV PYTHONUNBUFFERED=1
ENV PATH=$HOME/bin:$PATH
ENV GTK2_OK=yes

# Update and install basic OS packages
RUN \
        mkdir -p /dist; \
        adduser --disabled-password --gecos "" ${USER}; \
        echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers; \
        apt-get update; \
        apt-get upgrade -y; \
        apt-get install -y \
                apt-utils \
                build-essential \
                software-properties-common \
                nano; \
# Install development packages needed for building wxPython
        apt-get install -y \
                freeglut3 \
                freeglut3-dev \
                libgl1-mesa-dev \
                libglu1-mesa-dev \
                libgstreamer-plugins-base1.0-dev \
                libgtk-3-dev \
                libgtk2.0-dev \
                libjpeg-dev \
                libnotify-dev \
                libsdl2-dev \
                libsm-dev \
                libtiff-dev \
                libwebkitgtk-3.0-dev \
                libwebkitgtk-dev \
                libxtst-dev; \
        apt-get clean;


# Install all available Python packages and their dev packages
RUN \
        if [ ${USE_DEADSNAKES} = yes ]; then add-apt-repository ppa:deadsnakes/ppa; apt-get update; fi; \
        apt-get install -y python3.6 python3.6-dev libpython3.6-dev python3.6-venv; \
        apt-get install -y python3.8 python3.8-dev libpython3.8-dev python3.8-venv; \
        apt-get clean;

# Set the user and group to use for the rest of the commands
USER ${USER}:${USER}

# Set the working directory
WORKDIR ${HOME}

# Create virtual environments for each Python
RUN \
        cd ${HOME}; \
        mkdir -p ${HOME}/venvs; \
        python3.6 -m venv venvs/Py36; \
        python3.7 -m venv venvs/Py37; \
        python3.8 -m venv venvs/Py38;

# Add files from host into the container
COPY scripts ${HOME}/bin

# Define default command
CMD ["/bin/bash", "-l"]

