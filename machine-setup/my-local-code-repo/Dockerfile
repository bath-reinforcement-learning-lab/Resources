FROM nvidia/cuda:12.6.2-runtime-ubuntu22.04

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    sudo \
    libjpeg-dev \
    git \
    vim \
    libpng-dev \
    libglfw3 && \
    rm -rf /var/lib/apt/lists/*

# Install Python 3.10
RUN apt-get update && apt-get install -y python3.10 python3.10-dev python3-pip

# Set up working directory
WORKDIR /workspace

COPY requirements.txt /workspace/

# Setup torch GPU, no need to specify --index-url, probably https://download.pytorch.org/whl/nvidia-cuda-runtime-cu12/
RUN pip install torch torchvision torchaudio

# Install your own python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set python 3.10 as the default python
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Start a bash shell, do override this with a scheduling command.
CMD ["/bin/bash"]
