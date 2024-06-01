# Lightweight Python image.
FROM python:3.9-slim

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    sudo \
    libjpeg-dev \
    libpng-dev \
    libglfw3 && \
    rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /workspace

COPY requirements.txt /workspace/

# Setup torch GPU
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install your own python packages
RUN pip install --no-cache-dir -r requirements.txt

# Start a bash shell, do override this with a scheduling command.
CMD ["/bin/bash"]
