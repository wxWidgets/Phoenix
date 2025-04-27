# The base image (v11 == "bullseye")
FROM debian:bullseye

# Set environment variables
ENV DIST_NAME=debian-11
ENV USER=wxpy
ENV HOME=/home/$USER
ENV PYTHONUNBUFFERED=1
ENV PATH=$HOME/bin:$PATH
ENV GTK2_OK=no

# Update and install basic OS packages
RUN \
        apt-get update; \
        apt-get upgrade -y; \
        apt-get install -y \
                apt-utils \
                build-essential \
                software-properties-common \
                sudo nano; \
# Set up a user, and etc.
        mkdir -p /dist; \
        adduser --disabled-password --gecos "" ${USER}; \
        echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers; \
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
        apt-get install -y python3.9 python3.9-dev libpython3.9-dev python3.9-venv; \
        apt-get clean;


# Set the user and group to use for the rest of the commands
USER ${USER}:${USER}

# Set the working directory
WORKDIR ${HOME}

# Create virtual environments for each Python
RUN \
        cd ${HOME}; \
        mkdir -p ${HOME}/venvs; \
        python3.9 -m venv venvs/Py39;

# Add files from host into the container
COPY scripts ${HOME}/bin

# Define default command
CMD ["/bin/bash", "-l"]

