# The base image
FROM fedora:41

# Set environment variables
ENV DIST_NAME=fedora-41
ENV USER=wxpy
ENV HOME=/home/$USER
ENV PYTHONUNBUFFERED=1
ENV PATH=$HOME/bin:/usr/bin:$PATH
ENV GTK2_OK=no

# Update and install basic OS packages
RUN \
        dnf -y update; \
        dnf -y group install "Development Tools"; \
        dnf -y install gcc-c++ sudo nano which; \
# Set up a user, and etc.
        mkdir -p /dist; \
        adduser -m -s /usr/bin/bash ${USER}; \
        echo "${USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers; \
        mkdir -p ${HOME}/bin; \
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
                SDL2-devel \
                webkit2gtk3-devel;

RUN \
# Install all available Python packages and their dev packages
        dnf -y install python3 python3-devel; \
        dnf -y install python3.14 python3.14-devel;

RUN \
# Clean up dnf caches
        dnf clean all;

# Set the working directory
WORKDIR ${HOME}

# Create virtual environments for each Python
RUN \
        cd ${HOME}; \
        mkdir -p ${HOME}/venvs; \
        python3.13 -m venv ${HOME}/venvs/Py313; \
        python3.14 -m venv ${HOME}/venvs/Py314; \
        chown -R ${USER}:${USER} ${HOME};

# Add files from host into the container
COPY ./scripts/* ${HOME}/bin

# Set the user and group to use for the rest of the commands
USER ${USER}:${USER}

# Define default command
CMD ["/usr/bin/bash", "-l"]

